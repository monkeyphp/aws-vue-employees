#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# This function is used to update the Contract.

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
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"An Activity Id is required"
            })
        }

    employee_id = path_parameters.get('employee_id', None)
    if not employee_id:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"An Employee id is required"
            })
        }

    start_date = path_parameters.get('start_date', None)
    if not start_date:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"A start date is required"
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

    contract = {
        'employee_id': employee_id,
        'start_date': start_date,
    }

    weekly_hours = body.get('weekly_hours', None)
    if weekly_hours:
        contract['weekly_hours'] = weekly_hours

    hourly_rate = body.get('hourly_rate', None)
    if hourly_rate:
        contract['hourly_rate'] = hourly_rate

    updated_contract = update_contract(contract)
    if updated_contract is False:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Contract {start_date} could not be updated"
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(updated_contract)
    }


def update_contract(contract: dict) -> [dict, bool]:
    """ Update the Contract by updating or removing attributes.
    """
    try:
        employee_id = contract.get('employee_id')
        start_date = contract.get('start_date')

        key = {
            'pkey': f'EMPLOYEE-{employee_id}',
            'skey': f'CONTRACT-{start_date}'
        }

        update_expressions = {
            'SET': [],
            'REMOVE': [],
        }
        expression_attribute_values = {}
        expression_attribute_names = {}

        # weekly_hours and hourly_rate
        weekly_hours = contract.get('weekly_hours', None)
        if weekly_hours:
            update_expressions['SET'].append('#weekly_hours = :weekly_hours')
            expression_attribute_names['#weekly_hours'] = 'weekly_hours'
            expression_attribute_values[':weekly_hours'] = weekly_hours
        else:
            update_expressions['REMOVE'].append('weekly_hours')

        hourly_rate = contract.get('hourly_rate', None)
        if weekly_hours:
            update_expressions['SET'].append('#hourly_rate = :hourly_rate')
            expression_attribute_names['#hourly_rate'] = 'hourly_rate'
            expression_attribute_values[':hourly_rate'] = hourly_rate
        else:
            update_expressions['REMOVE'].append('hourly_rate')

        # create the update expression string
        update_expression = ' '.join(
            action + ' ' + ', '.join(values)
            for action, values in update_expressions.items()
            if values
        )
        return_values = 'ALL_NEW'

        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues=return_values
        )
        logger.critical("#RESPONSE")
        logger.critical(response)

        attributes = response.get('Attributes', None)
        if not attributes:
            return False

        created = attributes.get('created', None)
        if created:
            contract['created'] = created
        return contract
    except ClientError as ce:
        logger.critical(ce)
        return False



