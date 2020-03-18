#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# This function is used to return a list of the Employees for the specified Group.

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
                "message": f"A Group id is required"
            })
        }

    group_id = path_parameters.get('group_id', None)
    if not group_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"A Group id is required"
            })
        }

    employees = get_group_employees(group_id)
    if employees is False:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Employees for Group {group_id} could not be located"
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(employees)
    }


def get_group_employees(group_id: str) -> [list, bool]:
    """ Return a list of the Employees that have been added to the specified group_id.
    """
    try:
        key_condition_expression = Key('parent_group_id').eq(f'{group_id}') \
                                   & Key('pkey').begins_with('EMPLOYEE-')
        index_name = 'gsi-1'
        select = 'ALL_ATTRIBUTES'
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            IndexName=index_name,
            Select=select,
        )

        employees = []
        items = response.get('Items', [])
        for item in items:
            employee = {
                'employee_id': item.get('pkey').replace('EMPLOYEE-', '', 1),
                'parent_group_id': item.get('parent_group_id')
            }

            created = item.get('created', None)
            if created:
                employee['created'] = created

            name = item.get('name', None)
            if name:
                employee['name'] = name

            employees.append(employee)
        return employees
    except ClientError as ce:
        logger.critical(ce)
        return False


if __name__ == '__main__':
    response = lambda_handler({
        'pathParameters': {
            'group_id': 'projects',
        }
    }, {})

    print(response['body'])
