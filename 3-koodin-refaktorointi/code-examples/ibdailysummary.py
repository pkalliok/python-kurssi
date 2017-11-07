from datetime import timedelta
import pandas as pd
import utils
import geo
import units
import datetime
from dateutil import tz
import logging
logger = logging.getLogger('root')


def parse_ib_daily_activity(seasons, ib_activity, ais, day):
    next_day = day + timedelta(days = 1)

    if ib_activity.empty:
        return None
    daily_activities = ib_activity[ib_activity.apply(lambda ac: (ac['endtime_tz'].to_datetime().date() >= day)
                                                              & (ac['starttime_tz'].to_datetime().date() < next_day), axis=1)]

    tz_day_start = datetime.datetime(day.year, day.month, day.day, tzinfo=utils.SELECTED_TIME_ZONE)
    utc_day_start = tz_day_start.astimezone(tz.gettz('UTC'))

    tz_day_end = datetime.datetime(day.year, day.month, day.day, tzinfo=utils.SELECTED_TIME_ZONE) + timedelta(days = 1)
    utc_day_end = tz_day_end.astimezone(tz.gettz('UTC'))

    # TODO find another way to suppress SettingWithCopyWarning
    daily_activities.is_copy = False

    daily_activities['starttime'] = daily_activities['starttime'].apply(lambda x: max(x, utc_day_start))
    daily_activities['endtime'] = daily_activities['endtime'].apply(lambda x: min(x, utc_day_end))

    df = pd.DataFrame()
    for src in daily_activities['activity_src'].unique():
        ib_activities = daily_activities[daily_activities['activity_src'] == src]
        mmsi = ib_activities.iloc[0]['ib_mmsi']
        summary = count_ib_summary(src, ib_activities, ais, mmsi)
        s = get_season_details(seasons, src, day)

        if s is None:
            logger.info('No season found for src {src} on {day}'.format(src=src, day=day))
            continue
        else:
            summary.update(s)

        df = df.append(summary, ignore_index=True)
    return df


def get_season_details(seasons, src, day):
    season = seasons[(seasons['ib_src'] == src) & (seasons['starttime'] <= day) & (seasons['endtime'] >= day)]

    if len(season) != 1:
        return None

    return {'ib_season_id': season.iloc[0]['id'],
            'ib_season_src': season.iloc[0]['src'],
            'day': day}


def count_ib_summary(src, ac, ais, ib_mmsi):
    move_duration, move_distance = count_duration_and_distance(ais, ib_mmsi, ac[ac['activity_type'] == 'MOVE'][['starttime', 'endtime']])
    assist_duration, assist_distance = count_duration_and_distance(ais, ib_mmsi, to_merged_time_interval(ac[ac['activity_type'].isin(['LED', 'TOW'])][['starttime', 'endtime']]))
    tow_duration, tow_distance = count_duration_and_distance(ais, ib_mmsi, ac[ac['activity_type'] == 'TOW'][['starttime', 'endtime']])
    loc_duration, loc_distance = count_duration_and_distance(ais, ib_mmsi, ac[ac['activity_type'] == 'LOC'][['starttime', 'endtime']])

    total_duration = move_duration + assist_duration + loc_duration
    total_distance = move_distance + assist_distance + loc_distance

    vessels_assisted = len(ac[ac['activity_type'].isin(['LED', 'TOW'])].groupby(['vessel_id', 'vessel_src']))
    vessels_towed = len(ac[ac['activity_type'] == 'TOW'].groupby(['vessel_id', 'vessel_src']))

    return {
        'ib_src': src,
        'total_duration': units.sec_to_hours(total_duration),
        'total_distance': units.meters_to_nm(total_distance),
        'assist_duration': units.sec_to_hours(assist_duration + loc_duration),
        'assist_distance': units.meters_to_nm(assist_distance + loc_distance),
        'tow_duration': units.sec_to_hours(tow_duration),
        'tow_distance': units.meters_to_nm(tow_distance),
        'vessels_assisted': vessels_assisted,
        'vessels_towed': vessels_towed
    }


def process_ibdailysummary(season, ib_activity, ais, start_day, end_day):
    result = pd.DataFrame()

    day = start_day
    while day <= end_day:
        daily_activity = parse_ib_daily_activity(season, ib_activity, ais, day)
        logger.debug("ibdailysummary for day={day}, N={N}".format(day=day, N=len(daily_activity)))
        if daily_activity is not None:
            result = pd.concat([result, daily_activity])
        day = day + timedelta(days = 1)
    return result


def store_ibdailysummary(conn, ibdailysummary):
    logger.debug("Delete existing ibdailysummaries")
    cursor = conn.cursor()
    cursor.execute('delete from reporting.ibdailysummary')
    conn.commit()

    logger.debug("Insert {N} ibdailysummaries".format(N=len(ibdailysummary)))
    insertSql = 'insert into reporting.ibdailysummary(ib_src, ib_season_id, ib_season_src, day, total_duration, assist_duration, tow_duration, total_distance, assist_distance, tow_distance, vessels_assisted, vessels_towed, offhire_duration, wait_duration) values \n';

    i = 0
    for index, row in ibdailysummary.iterrows():
        val = "({ib_src}, {ib_season_id}, {ib_season_src}, convert(date, '{day}', 104), {total_duration}, {assist_duration}, {tow_duration}, {total_distance}, {assist_distance}, {tow_distance}, {vessels_assisted}, {vessels_towed}, {offhire_duration}, {wait_duration})".format(
            ib_src = row['ib_src'],
            ib_season_id = row['ib_season_id'],
            ib_season_src = row['ib_season_src'],
            day = row['day'].strftime('%d.%m.%Y'),
            total_duration = row['total_duration'],
            assist_duration = row['assist_duration'],
            tow_duration = row['tow_duration'],
            total_distance = row['total_distance'],
            assist_distance = row['assist_distance'],
            tow_distance = row['tow_distance'],
            vessels_assisted = row['vessels_assisted'],
            vessels_towed = row['vessels_towed'],
            offhire_duration = 0,
            wait_duration = 0
        )
        sql = insertSql + val
        cursor.execute(sql)
        conn.commit()


def count_duration_and_distance(ais, mmsi, intervals):
    if len(intervals) == 0:
        return 0, 0

    return sum(intervals.apply(lambda interval: interval_duration(interval), axis=1)), \
           sum(intervals.apply(lambda interval: interval_distance(ais, mmsi, interval), axis=1))


def interval_duration(interval):
    return (interval['endtime'] - interval['starttime']).seconds


def interval_distance(ais, mmsi, interval):
    return geo.calculate_path_distance(ais[(ais['mmsi'] == mmsi) & (ais['timestamp'] >= interval['starttime']) & (ais['timestamp'] < interval['endtime'])][['lat', 'lon']])


def to_merged_time_interval(activities):
    if len(activities) == 0:
        return activities

    merged = []
    intervals = [tuple(x) for x in activities.sort_values(by=['starttime', 'endtime']).to_records(index=False)]

    t_old = intervals[0]
    for t in intervals[1:len(intervals)]:
        if t_old[1] >= t[0]:
            t_old = (min(t_old[0], t[0]), max(t_old[1], t[1]))
        else:
            merged.append(t_old)
            t_old = t

    merged.append(t_old)

    df = pd.DataFrame(merged)
    df.columns = ['starttime', 'endtime']
    return df
