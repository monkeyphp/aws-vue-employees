#!/usr/bin/env python
import boto3
import os
import logging
import json
from decimal import Decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# This function is used to return the Timesheets for the specified Employee

# ```bash
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000/timesheets | python -m json.tool
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
                "message": f"An Employee Id is required"
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
    timesheets = get_employee_timesheets(employee_id)
    if timesheets is False:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"Timesheets for {employee_id} could not be located"
            })
        }

    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Expose-Headers': "*"
        },
        "body": json.dumps(timesheets, cls=CustomJsonEncoder)
    }


def get_employee_timesheets(employee_id: str) -> [list, bool]:
    """ Return a list of Timesheets for the specified Employee.
        Timesheets are keyed by `date`.
    """
    try:
        key_condition_expression = Key('pkey').eq(f"EMPLOYEE-{employee_id}") & Key('skey').begins_with('TIMESHEET-')
        select = 'ALL_ATTRIBUTES'
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            Select=select
        )
        timesheets = []
        items = response.get('Items', [])
        for item in items:
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

            timesheets.append(timesheet)
        return timesheets
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
#         }
#     }, {})
#
#     print(response['body'])
