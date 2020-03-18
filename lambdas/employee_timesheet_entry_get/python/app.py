#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from datetime import datetime, timezone
from dateutil.parser import parse

# This function is used to retrieve a specific Entry.

# ```
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000/timesheets/2020-01-01/entries/13:00 | python -m json.tool
# ```

# logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# env
TABLE_NAME = os.getenv('TABLE_NAME')

# cached resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    path_parameters = event.get('pathParameters', None)
    if not path_parameters:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"An Employee id is required"
            })
        }

    employee_id = path_parameters.get('employee_id', None)
    if not employee_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"An Employee id is required"
            })
        }

    date = path_parameters.get('date')
    if not date:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"A date is required"
            })
        }

    time = path_parameters.get('time')
    if not time:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"A date is required"
            })
        }

    entry = get_employee_timesheet_entry(employee_id, date, time)
    if not entry:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Entry {date} {time} could not be located"
            })
        }

    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(entry)
    }


def get_employee_timesheet_entry(employee_id: str, date: str, time: str) -> [dict, bool]:
    """ Return the Timesheet Entry identified by the supplied employee_id, date and time. """
    try:
        key = {
            'pkey': f"EMPLOYEE-{employee_id}",
            'skey': f'ENTRY-{date} {time}',
        }
        response = table.get_item(Key=key)
        item = response.get('Item', None)
        if item is None:
            return False

        pkey = item.get('pkey')
        skey = item.get('skey')

        # date = parse(skey).strftime('%Y-%m-%d %H:%M')

        date = item.get('date', None)
        start_time = item.get('start_time', None)
        finish_time = item.get('finish_time', None)
        activity_id = item.get('activity_id', None)

        entry = {
            'employee_id': pkey.replace('EMPLOYEE-', '', 1),
            'date': date,
            'start_time': start_time,
            'finish_time': finish_time,
            'activity_id': activity_id
        }

        created = item.get('created', None)
        if created:
            entry['created'] = created
        return entry
    except ClientError as ce:
        logger.critical(ce)
        return False
