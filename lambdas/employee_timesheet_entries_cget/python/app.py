#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from datetime import datetime, timezone
from dateutil.parser import parse

# This function is used to retrieve the Entries for the specified Employee and Timesheet date.

# ```bash
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000/timesheets/2020-01-01/entries | python -m json.tool
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
    entries = get_employee_timesheet_entries(employee_id, date)
    if entries is False:
        return {
            'statusCode': 500,
            'body': json.dumps({
                "message": f"Timesheet Entries could not be located"
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(entries)
    }


def get_employee_timesheet_entries(employee_id: str, date=None) -> list:
    """ Return a list of Employee Timesheet Entries.
        The optional date parameter is used to filter the Entries to a specific date.
    """
    try:
        skey = f'ENTRY-'
        if date is not None:
            skey = f'ENTRY-{date}'
        key_condition_expression = Key('pkey').eq(f"EMPLOYEE-{employee_id}") & Key('skey').begins_with(skey)

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
                entry['duration'] = str(duration)

            entries.append(entry)
        return entries
    except ClientError as ce:
        logger.critical(ce)
        return False
