from __future__ import absolute_import
import unittest
from reporting import ibdailysummary
import utils
import os
import pandas as pd
from datetime import timedelta, date
from dateutil import parser
from pandas.util.testing import assert_frame_equal

class Test(unittest.TestCase):
    """Unit tests for ibdailyibdailysummary."""

    def setUp(self):
        data_dir = resolve_data_dir()
        self.seasons = pd.read_csv(data_dir + "/seasons.csv", sep = ';', parse_dates = ['starttime', 'endtime'])
        self.ib_activities = pd.read_csv(data_dir + "/activities.csv", sep = ';', parse_dates = ['starttime', 'endtime'])

        self.ib_activities = utils.preprocess_ib_activity_data(self.ib_activities)
        self.ais = pd.read_csv(data_dir + "/observations.csv", sep = ';', parse_dates = ['timestamp'])

    def test_count_activity_distance(self):
        ac = self.ib_activities[self.ib_activities['activity_id'] == 25017680].iloc[0]
        distance = ibdailysummary.interval_distance(self.ais, ac['ib_mmsi'], ac[['starttime', 'endtime']])
        self.assertEqual(6730, distance)

    def test_count_interval_distance(self):
        ac = self.ib_activities[self.ib_activities['activity_id'] == 25017680].iloc[0]
        distance = ibdailysummary.interval_distance(self.ais, ac['ib_mmsi'], ac[['starttime', 'endtime']])
        self.assertEqual(6730, distance)

        ac2 = self.ib_activities[self.ib_activities['activity_id'] == 25017256].iloc[0]
        distance2 = ibdailysummary.interval_distance(self.ais, ac2['ib_mmsi'], ac2[['starttime', 'endtime']])
        self.assertEqual(35147, distance2)

        acs = self.ib_activities

        acs = acs[(acs['activity_id']  == 25017680) | (self.ib_activities['activity_id'] == 25017256)]
        distance_sum = sum(acs.apply(lambda ac:  ibdailysummary.interval_distance(self.ais, ac['ib_mmsi'], ac[['starttime', 'endtime']]), axis=1))
        self.assertEqual(distance_sum, distance + distance2)

    def test_parse_ib_daily_activity_no_season(self):
        df = ibdailysummary.parse_ib_daily_activity(self.seasons, self.ib_activities, self.ais, date(2017, 3, 30))

    def test_parse_ib_daily_activity(self):
        df = ibdailysummary.parse_ib_daily_activity(self.seasons, self.ib_activities, self.ais, date(2017, 3, 30))
        self.assertEqual(3, len(df))
        self.assertEqual(3.25, df[df['ib_src'] == 16]['assist_duration'].values[0])
        self.assertEqual(2.33, df[df['ib_src'] == 17]['tow_duration'].values[0])

    def test_to_merged_time_interval_single(self):
        ac = pd.DataFrame(
            {'starttime': [parser.parse('2017-04-01 12:00:00.000')],
             'endtime': [parser.parse('2017-04-01 12:20:00.000')]})[['starttime', 'endtime']]

        merged = ibdailysummary.to_merged_time_interval(ac)
        assert_frame_equal(ac, merged)

    def test_to_merged_time_interval_continuous(self):
        assert_frame_equal(pd.DataFrame(
            {'starttime': [parser.parse('2017-04-01 12:00:00.000')],
             'endtime':   [parser.parse('2017-04-01 12:40:00.000')]})[['starttime', 'endtime']],
                           ibdailysummary.to_merged_time_interval(pd.DataFrame(
                               {'starttime': [parser.parse('2017-04-01 12:00:00.000'),
                                              parser.parse('2017-04-01 12:20:00.000')],
                                'endtime':   [parser.parse('2017-04-01 12:20:00.000'),
                                              parser.parse('2017-04-01 12:40:00.000')]})[['starttime', 'endtime']]))

    def test_to_merged_time_interval_discrete(self):
        merged = ibdailysummary.to_merged_time_interval(pd.DataFrame(
            {'starttime': [parser.parse('2017-04-01 12:00:00.000'),
                           parser.parse('2017-04-01 12:20:00.000')],
             'endtime':   [parser.parse('2017-04-01 12:15:00.000'),
                           parser.parse('2017-04-01 13:00:00.000')]})[['starttime', 'endtime']])

        assert_frame_equal(pd.DataFrame(
            {'starttime': [parser.parse('2017-04-01 12:00:00.000'),
                           parser.parse('2017-04-01 12:20:00.000')],
             'endtime':   [parser.parse('2017-04-01 12:15:00.000'),
                           parser.parse('2017-04-01 13:00:00.000')]})[['starttime', 'endtime']],
                           merged)

    def test_to_merged_time_interval_discrete_combined(self):
        merged = ibdailysummary.to_merged_time_interval(pd.DataFrame(
            {'starttime': [parser.parse('2017-04-01 12:00:00.000'),
                           parser.parse('2017-04-01 12:20:00.000'),
                           parser.parse('2017-04-01 11:55:00.000')],
             'endtime':   [parser.parse('2017-04-01 12:15:00.000'),
                           parser.parse('2017-04-01 13:00:00.000'),
                           parser.parse('2017-04-01 13:05:00.000')]})[['starttime', 'endtime']])

        assert_frame_equal(pd.DataFrame(
            {'starttime': [parser.parse('2017-04-01 11:55:00.000')],
             'endtime':   [parser.parse('2017-04-01 13:05:00.000')]})[['starttime', 'endtime']],
                           merged)

    def test_overlapping_lead_and_tow(self):
        df = ibdailysummary.parse_ib_daily_activity(self.seasons, self.ib_activities, self.ais, date(2017, 4, 1))
        self.assertEqual(0.33, df[df['ib_src'] == 24]['tow_duration'].values[0])
        self.assertEqual(0.42, df[df['ib_src'] == 24]['assist_duration'].values[0])

        self.assertEqual(2.35, df[df['ib_src'] == 24]['tow_distance'].values[0])

        # lead and tow overlap
        self.assertEqual(3.63, df[df['ib_src'] == 24]['assist_distance'].values[0])


    #@unittest.skip("temp skip")
    def test_day_change(self):
        starttime = parser.parse('2017-04-10 20:00:00.000') # EET 23:00
        endtime = parser.parse('2017-04-11 03:00:00.000') # EET 6:00

        src = 100
        mmsi = 265068000
        ac = pd.DataFrame({'activity_src': [src], 'ib_mmsi':[25017680], 'activity_type': ['LED'],
                           'starttime': [starttime], 'endtime': [endtime],
                           'vessel_id': [123], 'vessel_src': [5]})

        seasons = pd.DataFrame({'id': [123], 'src': [456], 'ib_src': [src], 'starttime': parser.parse('2017-04-01 00:00:00.000'), 'endtime': parser.parse('2017-05-01 00:00:00.000')})

        ac = utils.preprocess_ib_activity_data(ac)
        apr10 = ibdailysummary.parse_ib_daily_activity(seasons, ac, self.ais, date(2017, 4, 10))
        self.assertEqual(apr10['assist_duration'].values[0], 1)

        apr11 = ibdailysummary.parse_ib_daily_activity(seasons, ac, self.ais, date(2017, 4, 11))
        self.assertEqual(apr11['assist_duration'].values[0], 6)

        self.assertEqual(apr10['assist_duration'].values[0] + apr11['assist_duration'].values[0], (endtime - starttime).seconds / 3600)


def resolve_data_dir():
    if os.path.isdir("data"):
        return "data"
    if os.path.isdir("../data"):
        return "../data"
    raise Exception("Can not resolve data directory")
