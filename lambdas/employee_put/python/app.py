#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

# This function is used to update an Employee

# ```bash
# curl -XPUT -d '{"name": "Harry Henderson"}' https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/2002 | python -m json.tool
# `

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

    # default the group to the `all` group
    parent_group_id = body.get('parent_group_id', 'all')

    employee = {
        'employee_id': employee_id,
        'name': name,
        'parent_group_id': parent_group_id,
    }

    updated_employee = update_employee(employee)
    if updated_employee is False:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Employee {employee_id} could not be updated"
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(updated_employee)
    }


def update_employee(employee: dict) -> [dict, bool]:
    try:
        employee_id = employee.get('employee_id')

        key = {
            'pkey': f'EMPLOYEE-{employee_id}',
            'skey': 'EMPLOYEE',
        }

        update_expressions = {
            'SET': [],
            'REMOVE': [],
        }
        expression_attribute_values = {}
        expression_attribute_names = {}

        # name should always be supplied
        name = employee.get('name')
        update_expressions['SET'].append('#name = :name')
        expression_attribute_names['#name'] = 'name'
        expression_attribute_values[':name'] = name

        # parent_group_id should always be supplied
        parent_group_id = employee.get('parent_group_id')
        update_expressions['SET'].append('#parent_group_id = :parent_group_id')
        expression_attribute_names['#parent_group_id'] = 'parent_group_id'
        expression_attribute_values[':parent_group_id'] = parent_group_id

        update_expression = ' '.join(
            action + ' ' + ', '.join(values)
            for action, values in update_expressions.items()
            if values
        )
        return_values = 'ALL_NEW'
        condition_expression = Attr('pkey').exists()

        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues=return_values,
            ConditionExpression=condition_expression
        )

        attributes = response.get('Attributes', None)
        if not attributes:
            return False

        created = attributes.get('created', None)
        if created:
            employee['created'] = created

        return employee
    except ClientError as ce:
        logger.critical(ce)
        return False


# if __name__ == '__main__':
#     response = lambda_handler(
#         {
#             "pathParameters": {
#                 "employee_id": "1000",
#             },
#             "body": json.dumps({'name': 'Andrew Alberts'})
#         },
#         {}
#     )
#     print(response)
