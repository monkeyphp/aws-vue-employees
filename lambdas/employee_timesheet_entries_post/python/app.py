#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from datetime import datetime, date, time, timezone
from dateutil.parser import parse
from decimal import Decimal

# This function is used to handle POST requests for adding Timesheets to an Employee.
# When an Entry is submitted - we will create/update the Timesheet for the Entry.

# ```bash
# curl -d '{"start_time": "09:00", "finish_time": "17:30", "activity_id": "working"}' https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000/timesheets/2020-01-01/entries | python -m json.tool
# curl -d '{"start_time": "13:00", "finish_time": "13:30", "activity_id": "lunch"}' https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000/timesheets/2020-01-01/entries | python -m json.tool
# ```

# logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# env
TABLE_NAME = os.getenv('TABLE_NAME', 'employees-table')

# cached resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    path_parameters = event.get('pathParameters', None)
    if not path_parameters:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"An Employee Uuid is required"
            })
        }

    employee_id = path_parameters.get('employee_id', None)
    if not employee_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"An Employee Id is required"
            })
        }

    date = path_parameters.get('date', None)
    if not date:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"A date is required"
            })
        }

    try:
        # @link https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        date = parse(date).strftime('%Y-%m-%d')
    except ValueError as ve:
        logger.critical(ve)
        return {
            'statusCode': 400,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"The supplied date {date} is invalid"
            })
        }

    if 'body' not in event:
        raise Exception('No body supplied')

    body = event.get('body', None)
    if body is None:
        return {
            'statusCode': 400,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"A body is required"
            })
        }
    body = json.loads(body)

    start = body.get('start', None)
    if start is None:
        return {
            'statusCode': 400,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"A start is required"
            })
        }

    finish = body.get('finish', None)
    if finish is None:
        return {
            'statusCode': 400,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"A finish is required"
            })
        }

    activity_id = body.get('activity_id', None)
    if activity_id is None:
        return {
            'statusCode': 400,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"An Activity Id is required"
            })
        }

    created = str(datetime.now(timezone.utc))
    duration = calculate_duration(start, finish)
    duration = Decimal(duration)

    entry = {
        'employee_id': employee_id,
        'date': date,
        'start': start,
        'finish': finish,
        'activity_id': activity_id,
        'created': created,
        'duration': duration,
    }

    logger.debug('#ENTRY')
    logger.debug(entry)

    saved = save_employee_timesheet_entry(entry)
    if not saved:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"Entry could not be saved"
            })
        }

    # experimental - perhaps we should use a Stream lambda to do this work
    timesheet = {
        'employee_id': employee_id,
        'date': date,
        'created': created,
    }

    entries = get_employee_timesheet_entries(employee_id, date)
    logger.debug('#ENTRIES')
    logger.debug(entries)

    activities = {}
    for entry in entries:
        activity_id = entry.get('activity_id', None)
        if activity_id is None:
            continue
        duration = entry.get('duration', None)
        if duration is None:
            continue
        if activity_id not in activities:
            activities[activity_id] = duration
            continue
        activities[activity_id] = (activities[activity_id] + duration)

    timesheet['activities'] = activities
    save_employee_timesheet(timesheet)

    # Decimals cannot be cast using json :(
    entry['duration'] = str(entry['duration'])

    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Location': f"/employees/{employee_id}/timesheets/{date}/entries/{start}"
        },
        'body': json.dumps(entry)
    }


def calculate_duration(start: str, finish: str) -> float:
    """ Calculate the number of minutes between supplied start and finish time.
        We assume that both times are on the same day.
    """
    start_time = time.fromisoformat(start)
    finish_time = time.fromisoformat(finish)
    delta = datetime.combine(date.min, finish_time) - datetime.combine(date.min, start_time)
    seconds = delta.seconds
    if start_time > finish_time:
        seconds = -(86400 - seconds)
    return seconds / 60


def save_employee_timesheet_entry(entry: dict) -> bool:
    """ Save the supplied Employee Timesheet Entry.
    """
    try:
        employee_id = entry.get('employee_id')
        date = entry.get('date')
        start = entry.get('start')

        pkey = f'EMPLOYEE-{employee_id}'
        skey = f'ENTRY-{date} {start}'

        item = {
            'pkey': pkey,
            'skey': skey,
            'date': date,
            'start': start,
        }

        created = entry.get('created', None)
        if created:
            item['created'] = created

        finish = entry.get('finish', None)
        if finish:
            item['finish'] = finish

        activity_id = entry.get('activity_id', None)
        if activity_id:
            item['activity_id'] = activity_id

        duration = entry.get('duration', None)
        if duration:
            item['duration'] = duration

        response = table.put_item(Item=item)
        return True
    except ClientError as ce:
        logger.critical(ce)
        return False


def get_employee_timesheet_entries(employee_uuid: str, date) -> [list, bool]:
    """ Return a list of Employee Timesheet Entries.
        The optional date parameter is used to filter the Entries to a specific date.
    """
    try:
        key_condition_expression = Key('pkey').eq(f"EMPLOYEE-{employee_uuid}") & \
                                   Key('skey').begins_with(f'ENTRY-{date}')

        select = 'ALL_ATTRIBUTES'
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            Select=select
        )
        entries = []
        items = response.get('Items', [])
        for item in items:
            # date = parse(skey).strftime('%Y-%m-%d %H:%M')
            entry = {
                'employee_id': item.get('pkey').replace('EMPLOYEE-', '', 1),
            }
            created = item.get('created', None)
            if created:
                entry['created'] = created

            date = item.get('date', None)
            if date:
                entry['date'] = date

            start = item.get('start', None)
            if start:
                entry['start'] = start

            finish = item.get('finish', None)
            if finish:
                entry['finish'] = finish

            activity_id = item.get('activity_id', None)
            if activity_id:
                entry['activity_id'] = activity_id

            duration = item.get('duration', None)
            if duration:
                entry['duration'] = duration

            entries.append(entry)
        return entries
    except ClientError as ce:
        logger.critical(ce)
        return False


def save_employee_timesheet(timesheet: dict) -> bool:
    """ Save the supplied Timesheet.
    """
    try:
        employee_id = timesheet.get('employee_id')
        date = timesheet.get('date')

        item = {
            'pkey': f'EMPLOYEE-{employee_id}',
            'skey': f'TIMESHEET-{date}'
        }

        created = timesheet.get('created', None)
        if created:
            item['created'] = created

        activities = timesheet.get('activities', None)
        if activities:
            item['activities'] = activities

        response = table.put_item(Item=item)

        logger.debug('#RESPONSE')
        logger.debug(response)

        return True
    except ClientError as ce:
        logger.critical(ce)
        return False


# if __name__ == '__main__':
#     print(lambda_handler(
#         {
#             'pathParameters': {
#                 'employee_id': '1000',
#                 'date': '2020-01-01',
#             },
#             'body': json.dumps({
#                 'start': '09:00',
#                 'finish': '13:00',
#                 'activity_id': 'worked',
#             })
#         },
#         {}
#     ))
#     print(lambda_handler(
#         {
#             'pathParameters': {
#                 'employee_id': '1000',
#                 'date': '2020-01-01',
#             },
#             'body': json.dumps({
#                 'start': '13:00',
#                 'finish': '13:30',
#                 'activity_id': 'break',
#             })
#         },
#         {}
#     ))


