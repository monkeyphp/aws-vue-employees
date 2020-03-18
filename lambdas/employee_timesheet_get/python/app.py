#!/usr/bin/env python
import boto3
import os
import logging
import json
from decimal import Decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# This function is used to return the specified Timesheet for the specified Employee.
# The date and employee_id of the Timesheet are required values.
# - employee_id: the id of the Employee
# - date: in YYYY-MM-DD format (ISO 8601)

# ```bash
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000/timesheets/2020-01-03 | python -m json.tool
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
    timesheet = get_employee_timesheet(employee_id, date)
    if timesheet is False:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"Timesheet could not be located"
            })
        }

    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Expose-Headers': "*"
        },
        "body": json.dumps(timesheet, cls=CustomJsonEncoder)
    }


def get_employee_timesheet(employee_id: str, date: str) -> [dict, bool]:
    """ Return the Timesheet specified by the supplied employee_id and date.
    """
    try:
        key = {
            'pkey': f"EMPLOYEE-{employee_id}",
            'skey': f'TIMESHEET-{date}'
        }
        response = table.get_item(Key=key)
        item = response.get('Item', None)

        if item is None:
            return False

        timesheet = {
            'employee_id': item.get('pkey').replace('EMPLOYEE-', '', 1),
            'date': item.get('skey').replace('TIMESHEET-', '', 1)
        }

        # created
        created = item.get('created', None)
        if created:
            timesheet['created'] = created

        # not_worked
        not_worked = item.get('not_worked', None)
        if not_worked:
            timesheet['not_worked'] = not_worked

        # worked
        worked = item.get('worked', None)
        if worked:
            timesheet['worked'] = worked

        # total
        total = item.get('total', None)
        if total:
            timesheet['total'] = total

        # entries
        entries = item.get('entries', [])
        if entries:
            timesheet['entries'] = entries

        return timesheet
    except ClientError as ce:
        logger.critical(ce)
        return False


# https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)


# if __name__ == '__main__':
#     response = lambda_handler({
#         'pathParameters': {
#             'employee_id': '001',
#             'date': '2020-01-31',
#         }
#     }, {})
#
#     print(response['body'])
