#!/usr/bin/python

import utils
import argparse
import datetime
from reporting import ibdailysummary
import pymssql
import log
logger = log.log_config('root')


def parse_args():
    parser = argparse.ArgumentParser(description='IBNext reporting')
    parser.add_argument('-S', '--server', help='MS SQL Server instance (e.g. 10.30.30.101)', required=True)
    parser.add_argument('-p', '--port', help='Port (1433)', required=True)
    parser.add_argument('-d', '--database', help='Db to use (ibnext)', required=True)
    parser.add_argument('-U', '--username', help='Db username (ibnext)', required=True)
    parser.add_argument('-P', '--password', help='Db password (ibnext)', required=True)
    parser.add_argument('-s', '--start-day', help='Start day (2016-11-01)', required=True)
    parser.add_argument('-e', '--end-day', help='End day (2017-05-31)', required=True)
    args = vars(parser.parse_args())
    return args


def main():
    logger.info('Update reporting schema data')

    args = parse_args()
    conn = pymssql.connect(server=args['server'], port=args['port'], database=args['database'], user=args['username'], password=args['password'])
    ib_activities, seasons, observations = utils.read_data(conn)

    start_day = datetime.datetime.strptime(args['start_day'], '%Y-%m-%d').date()
    end_day = datetime.datetime.strptime(args['end_day'], '%Y-%m-%d').date()

    logger.info("Process ibdailysummary from {start_day} to {end_day}".format(start_day=start_day, end_day=end_day))
    summary = ibdailysummary.process_ibdailysummary(seasons, ib_activities, observations, start_day, end_day)
    ibdailysummary.store_ibdailysummary(conn, summary)


if __name__ == "__main__":
    main()
