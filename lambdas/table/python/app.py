#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from datetime import datetime
from datetime import timezone
from dateutil.parser import parse
import uuid

# logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# env
TABLE_NAME = os.getenv('TABLE_NAME')

# cached resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    logger.debug('#EVENT')
    logger.debug(event)

    if 'Records' not in event:
        raise Exception('Records not supplied')

    records = event.get('Records', [])
    logger.debug(records)
    return True
    # for record in records:
    #     processed = process_record(record)
    # return True


# # routing function
# def process_record(record: dict) -> bool:
#     dynamodb = event.get('dynamodb', {})
#     keys = dynamodb.get("Keys", {})
#     pkey = keys.get('pkey', {})
#     pkey = pkey.get('S', None)
#
#     skey = keys.get('skey', {})
#     skey = skey.get('S', None)
#
#     if pkey.startswith('TIMESHEETENTRY'):
#         return process_timesheet_entry_record(record)
#
#     return True


# def process_timesheet_entry_record(record: dict) -> bool:
#     event_name = record.get('eventName', None) # REMOVE | INSERT | MODIFY
#     if not event_name:
#         logger.critical('eventName is not set')
#         return False
#
#     dynamodb = event.get('dynamodb', {})
#     keys = dynamodb.get("Keys", {})
#
#     pkey = keys.get('pkey', {}) # TIMESHEET-1000
#     pkey = pkey.get('S', None)
#
#     skey = keys.get('skey', {}) # 2019-12-21 09:00
#     skey = skey.get('S', None)
#
#     employee_id = pkey.replace('TIMESHEETENTRY-', '', 1)
#     date = parse(skey).strftime('%Y-%m-%d')
#
#     timesheet = get_timesheet(employee_id, date)
#     if not timesheet:
#         timesheet = {
#             'employee_id': employee_id,
#             'timesheet_id': date,
#             'date': date,
#         }
#
#     # retrieve the timesheets entries for the aggregate date
#     timesheet_entries = get_timesheet_entries(employee_id, date)
#     activities = {}
#
#     for timesheet_entry in timesheet_entries:
#         activity = timesheet_entry.get('activity')
#         duration = timesheet_entry.get('duration', 0)
#         if not duration:
#             continue
#
#         if activity not in activities:
#             activities[activity] = duration
#             continue
#
#         activities[activity] = (activities[activity] + duration)
#
#     for key, value in activities.items():
#         timesheet[key] = value
#
#     saved = save_timesheet(timesheet)
#     if not saved:
#         logger.critical(f'Timesheet could not be saved')
#         return False
#
#     return True
#
#
# def get_timesheet(employee_id: str, date: str) -> [dict, bool]:
#     try:
#         key = {
#             'pkey': f'EMPLOYEE-{employee_id}',
#             'skey': f'TIMESHEET-{date}'
#         }
#         response = table.get_item(Key=key)
#
#         item = response.get('Item', None)
#         if item is None:
#             return False
#
#         timesheet = {
#             'employee_id': item.get('pkey').replace('EMPLOYEE-', '', 1),
#             'timesheet_id': item.get('skey').replace('TIMESHEET-', '', 1),
#         }
#
#         return {}
#     except ClientError as ce:
#         logger.critical(ce)
#
#
# def save_timesheet(timesheet: dict) -> [bool]:
#     try:
#
#     except ClientError as ce:
#         logger.critical(ce)
#         return False
#
# def get_timesheet_entries(employee_id, date) -> list:
#     try:
#         key_condition_expression = Key('pkey').eq(f"TIMESHEET-{employee_id}")  # & Key('skey').begins_with('CONTRACT-')
#         select = 'ALL_ATTRIBUTES'
#         response = table.query(
#             KeyConditionExpression=key_condition_expression,
#             Select=select
#         )
#
#         timesheets = []
#         items = response.get('Items', [])
#         for item in items:
#             timesheet = {
#                 'employee_id': item.get('pkey').replace('TIMESHEET-', '', 1),
#                 'timesheet_id': item.get('skey')
#             }
#
#             created = item.get('created', None)
#             if created:
#                 timesheet['created'] = created
#
#             date = item.get('date', None)
#             if date:
#                 timesheet['date'] = date
#
#             start_time = item.get('start_time', None)
#             if start_time:
#                 timesheet['start_time'] = start_time
#
#             finish_time = item.get('finish_time', None)
#             if finish_time:
#                 timesheet['finish_time'] = finish_time
#
#             activity = item.get('activity', None)
#             if activity:
#                 timesheet['activity'] = activity
#
#             timesheets.append(timesheet)
#
#         return timesheets
#     except ClientError as ce:
#         logger.critical(ce)
#         return []
#
#
#
#
#
#
#     # locate the `EMPLOYEE-1000 | TIMESHEET-2020-01-01` record
#
#
#     approximate_creation_datetime = dynamodb.get('ApproximateCreationDateTime', None)
#     event_id = record.get('eventID', None)
#     event_version = record.get('eventVersion', None)
#     event_source = record.get('eventVersion', None)
#     aws_region = record.get('awsRegion', None)
#
# # Employees
# # Timesheets
# # EmployeeGroups
# pkey | skey | worked
#
# EMPLOYEE-1000 | TIMESHEET-2020-01-01 | 8 | 0.5
# EMPLOYEE-1000 | TIMESHEET-2020-01-02 | 8 | 0.5
# EMPLOYEE-1000 | TIMESHEET-2020-01-03 | 7 | 0.5
#
#
# # REMOVED RECORD
# event = {
#     'Records': [
#         {
#             'eventID': 'f8ae99923a5a6fdae517ade8ebfb8a61',
#             'eventName': 'REMOVE',
#             'eventVersion': '1.1',
#             'eventSource': 'aws:dynamodb',
#             'awsRegion': 'eu-west-2',
#             'dynamodb': {
#                 'ApproximateCreationDateTime': 1578580811.0,
#                 'Keys': {
#                     'pkey': {'S': 'TIMESHEET-1000'}
#                     'skey': {'S': '2019-12-21 09:00'},
#                 },
#                 'OldImage': {
#                     'start_time': {'S': '09:00'},
#                     'activity': {'S': 'work'},
#                     'date': {'S': '2019-12-21'},
#                     'created': {'S': '2020-01-08 15:39:57.207253+00:00'},
#                     'skey': {'S': '2019-12-21 09:00'},
#                     'pkey': {'S': 'TIMESHEET-1000'},
#                     'finish_time': {'S': '17:00'}
#                 },
#                 'SequenceNumber': '39554300000000003909780734',
#                 'SizeBytes': 172,
#                 'StreamViewType': 'NEW_AND_OLD_IMAGES'
#             },
#             'eventSourceARN': 'arn:aws:dynamodb:eu-west-2:015607038551:table/employees-table/stream/2020-01-09T14:16:17.304'
#         }
#     ]
# }
#
# # NEW RECORD
# event = {
#     'Records': [
#         {
#             'eventID': 'ca44f428b2304fd4a4dc1af09228cad0',
#             'eventName': 'INSERT',
#             'eventVersion': '1.1',
#             'eventSource': 'aws:dynamodb',
#             'awsRegion': 'eu-west-2',
#             'dynamodb': {
#                 'ApproximateCreationDateTime': 1578579891.0,
#                 'Keys': {
#                     'skey': {'S': 'EMPLOYEE'},
#                     'pkey': {'S': 'EMPLOYEE-2000'}
#                 },
#                 'NewImage': {
#                     'created': {'S': '2020-01-09 14:24:51.566966+00:00'},
#                     'name': {'S': 'New Employee'},
#                     'skey': {'S': 'EMPLOYEE'},
#                     'pkey': {'S': 'EMPLOYEE-2000'}
#                 },
#                 'SequenceNumber': '39554000000000003909610583',
#                 'SizeBytes': 113,
#                 'StreamViewType': 'NEW_AND_OLD_IMAGES'
#             },
#             'eventSourceARN': 'arn:aws:dynamodb:eu-west-2:015607038551:table/employees-table/stream/2020-01-09T14:16:17.304'
#         }
#     ]
# }
#
# # MODIFIED RECORD
# event = {
#     'Records': [
#         {
#             'eventID': '86388ea1cd136fc7cb27d7de20491375',
#             'eventName': 'MODIFY',
#             'eventVersion': '1.1',
#             'eventSource': 'aws:dynamodb',
#             'awsRegion': 'eu-west-2',
#             'dynamodb': {
#                 'ApproximateCreationDateTime': 1578580593.0,
#                 'Keys': {
#                     'skey': {'S': 'EMPLOYEE'},
#                     'pkey': {'S': 'EMPLOYEE-2001'}
#                 },
#                 'NewImage': {
#                     'created': {'S': '2020-01-09 14:31:08.834401+00:00'},
#                     'name': {'S': 'UPDATED NEW EMPLOYEE'},
#                     'skey': {'S': 'EMPLOYEE'},
#                     'pkey': {'S': 'EMPLOYEE-2001'}
#                 },
#                 'OldImage': {
#                     'created': {'S': '2020-01-09 14:31:08.834401+00:00'},
#                     'name': {'S': 'ANOTHER NEW EMPLOYEE'},
#                     'skey': {'S': 'EMPLOYEE'},
#                     'pkey': {'S': 'EMPLOYEE-2001'}
#                 },
#                 'SequenceNumber': '39554200000000003909739370',
#                 'SizeBytes': 213,
#                 'StreamViewType': 'NEW_AND_OLD_IMAGES'
#             },
#             'eventSourceARN': 'arn:aws:dynamodb:eu-west-2:015607038551:table/employees-table/stream/2020-01-09T14:16:17.304'
#         }
#     ]
# }




