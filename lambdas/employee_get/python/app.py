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

# this function is used to retrieve the specified Employee.

# ```bash
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000 | python -m json.tool
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

    employee = get_employee(employee_id)
    if not employee:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Employee {employee_id} could not be located"
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(employee)
    }


def get_employee(employee_id: str) -> [dict, bool]:
    """ Return the Employee identified by employee_id """
    try:
        key = {
            'pkey': f"EMPLOYEE-{employee_id}",
            'skey': 'EMPLOYEE',
        }
        response = table.get_item(Key=key)
        item = response.get('Item', None)
        if not 'item':
            return False
        employee = {
            'employee_id': item.get('pkey').replace('EMPLOYEE-', '', 1)
        }
        created = item.get('created', None)
        if created:
            employee['created'] = created

        name = item.get('name', None)
        if name:
            employee['name'] = name

        parent_group_id = item.get('parent_group_id', None)
        if parent_group_id:
            employee['parent_group_id'] = parent_group_id

        return employee
    except ClientError as ce:
        logger.critical(ce)
        return False
