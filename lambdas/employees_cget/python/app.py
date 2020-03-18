#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# This function is used to retrieve the Employees.

# ```bash
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees | python -m json.tool
# ```

# employee = {
#     'employee_id': '414d407f-a96e-47a0-a294-90706d54302e',
#     'name': 'Albert Andrews',
#     'created': '2020-01-01 13:45:34',
#     'parent_group_id': 'all',
# }

# logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# env
TABLE_NAME = os.getenv('TABLE_NAME', 'employees-table')

# cached resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    employees = get_employees()
    if employees is False:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "message": f"Employees could not be located"
            })
        }
    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(employees)
    }


def get_employees() -> [list, bool]:
    """ Return a list of Employees """
    try:
        key_condition_expression = Key('skey').eq("EMPLOYEE")
        index_name = 'gsi-0'
        select = 'ALL_ATTRIBUTES'
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            IndexName=index_name,
            Select=select
        )
        employees = []
        items = response.get('Items', [])
        for item in items:
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

            employees.append(employee)
        return employees
    except ClientError as ce:
        logger.critical(ce)
        return False
