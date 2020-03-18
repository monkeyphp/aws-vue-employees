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

# @link https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-sort-keys.html
# This lambda function is used to handle `/employees/1/contracts` [POST] requests.

# ```bash
# curl -d '{"start":"2020-01-19","weekly_hours":"32","hourly_rate":"896"}' https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000/contracts
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
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*",
            },
            'body': json.dumps({
                "message": f"An Employee id is required"
            })
        }

    employee_id = path_parameters.get('employee_id', None)
    if not employee_id:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*",
            },
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
    start_date = body.get('start_date', None)
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

    try:
        # @link https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        start_date = parse(start_date).strftime('%Y-%m-%d')
    except ValueError as ve:
        logger.critical(ve)
        return {
            'statusCode': 400,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"The supplied start {start_date} is invalid"
            })
        }

    created = str(datetime.now(timezone.utc))
    contract = {
        'start_date': start_date,
        'employee_id': employee_id,
        'created': created,
    }

    weekly_hours = body.get('weekly_hours', None)
    if weekly_hours:
        contract['weekly_hours'] = weekly_hours

    hourly_rate = body.get('hourly_rate', None)
    if hourly_rate:
        contract['hourly_rate'] = hourly_rate

    saved = save_contract(contract)
    if not saved:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*",
            },
            'body': json.dumps({
                "message": f"Contract could not be saved"
            })
        }

    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Location': f"/employees/{employee_id}/contracts/{start_date}"
        },
        'body': json.dumps(contract)
    }


def save_contract(contract: dict) -> bool:
    try:
        employee_id = contract.get('employee_id')
        start_date = contract.get('start_date')

        item = {
            'pkey': f"EMPLOYEE-{employee_id}",
            "skey": f"CONTRACT-{start_date}"
        }

        if 'created' in contract:
            item['created'] = contract['created']

        if 'weekly_hours' in contract:
            item['weekly_hours'] = contract['weekly_hours']

        if 'hourly_rate' in contract:
            item['hourly_rate'] = contract['hourly_rate']

        response = table.put_item(Item=item)
        return True
    except ClientError as ce:
        logger.critical(ce)
        return False
