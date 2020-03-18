#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError

# This function is used to delete a specific Entry

# ```
# curl -XDELETE https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000/timesheets/2020-01-01/entries/13:00 | python -m json.tool
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

    deleted = delete_employee_timesheet_entry(employee_id, date, time)
    if not deleted:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Entry {date} {time} could not be deleted"
            })
        }

    return {
        'statusCode': 204,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        }
    }


def delete_employee_timesheet_entry(employee_id, date, time) -> bool:
    """ Delete the specified Entry """
    try:
        key = {
            'pkey': f"EMPLOYEE-{employee_id}",
            'skey': f'ENTRY-{date} {time}',
        }
        table.delete_item(Key=key)
        return True
    except ClientError as ce:
        logger.critical(ce)
        return False