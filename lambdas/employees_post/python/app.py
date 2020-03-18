#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timezone

# This function is used for posting an Employee

# ```bash
# curl -d '{"name": "Harry Horlicks", "employee_id": "2002"}' https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees | python -m json.tool
# ```

# employee = {
#     'employee_id': '1000'
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

    name = body.get('name', None)
    if name is None:
        return {
            'statusCode': 400,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"A name is required"
            })
        }

    employee_id = body.get('employee_id', None)
    if employee_id is None:
        return {
            'statusCode': 400,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"An employee id is required"
            })
        }

    # default the group to the `all` group
    parent_group_id = body.get('parent_group_id', 'all')
    created = str(datetime.now(timezone.utc))
    employee = {
        'employee_id': employee_id,
        'created': created,
        'name': name,
        'parent_group_id': parent_group_id
    }

    try:
        save_employee(employee)
    except ClientError as ce:
        response = ce.response
        error = response.get('Error')
        code = error.get('Code')
        if code == 'ConditionalCheckFailedException':
            error = f"An Employee with id {employee_id} already exists"
        else:
            error = f"Employee could not be saved"
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*",
            },
            'body': json.dumps({
                "error": error
            })
        }

    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Location': f"/employees/{employee_id}"
        },
        'body': json.dumps(employee)
    }


def save_employee(employee: dict) -> bool:
    """ Save the Employee """
    try:
        employee_id = employee.get('employee_id')
        item = {
            'pkey': f'EMPLOYEE-{employee_id}',
            'skey': 'EMPLOYEE',
        }

        name = employee.get('name', None)
        if name:
            item['name'] = name

        created = employee.get('created', None)
        if created:
            item['created'] = created

        parent_group_id = employee.get('parent_group_id', None)
        if parent_group_id:
            item['parent_group_id'] = parent_group_id

        condition_expression = Attr('pkey').not_exists()
        table.put_item(
            Item=item,
            ConditionExpression=condition_expression
        )
        return True
    except ClientError as ce:
        logger.critical(ce)
        raise ce
