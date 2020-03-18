#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# @link https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-sort-keys.html
# This lambda function is used to retrieve the Contracts for an Employee.

# ```bash
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000/contracts | python -m json.tool
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
    contracts = get_employee_contracts(employee_id)
    if contracts is False:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"Contracts could not be located"
            })
        }
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Expose-Headers': "*"
        },
        "body": json.dumps(contracts)
    }


def get_employee_contracts(employee_id: str) -> [list, bool]:
    """ Return a list of Contracts that have been added to the specified employee_id.
    """
    try:
        key_condition_expression = Key('pkey').eq(f"EMPLOYEE-{employee_id}") & Key('skey').begins_with('CONTRACT-')
        select = 'ALL_ATTRIBUTES'
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            Select=select
        )
        contracts = []
        items = response.get('Items', [])
        for item in items:
            contract = {
                'employee_id': item.get('pkey').replace('EMPLOYEE-', '', 1),
                'start_date': item.get('skey').replace('CONTRACT-', '', 1)
            }
            created = item.get('created', None)
            if created:
                contract['created'] = created

            weekly_hours = item.get('weekly_hours', None)
            if weekly_hours:
                contract['weekly_hours'] = weekly_hours

            hourly_rate = item.get('hourly_rate', None)
            if hourly_rate:
                contract['hourly_rate'] = hourly_rate

            contracts.append(contract)
        return contracts
    except ClientError as ce:
        logger.critical(ce)
        return False
