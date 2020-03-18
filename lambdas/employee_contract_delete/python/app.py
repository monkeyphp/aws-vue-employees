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

# This function is used to delete a Contract

# ```bash
# curl -XDELETE https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/1000/contracts/2020-01-19 | python -m json.tool
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
    start_date = path_parameters.get('start_date', None)
    if not start_date:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"A start_date is required"
            })
        }

    contract = get_employee_contract(employee_id, start_date)
    if contract is False:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"Contract could not be located"
            })
        }

    deleted = delete_employee_contract(contract)
    if not deleted:
        return {
            'statusCode': 500,
            'body': json.dumps({
                "message": f"Contract could not be deleted"
            })
        }

    return {
        "statusCode": 204,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Expose-Headers': "*"
        }
    }


def get_employee_contract(employee_id: str, start_date: str) -> [dict,bool]:
    try:
        key = {
            'pkey': f"EMPLOYEE-{employee_id}",
            'skey': f"CONTRACT-{start_date}"
        }
        response = table.get_item(Key=key)
        item = response.get('Item', None)
        if item is None:
            return False
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
        return contract
    except ClientError as ce:
        logger.critical(ce)
        return False


def delete_employee_contract(contract: dict) -> bool:
    try:
        employee_id = contract.get('employee_id')
        start_date = contract.get('start_date')
        deleted_contract = contract.copy()
        deleted_contract['deleted'] = str(datetime.now(timezone.utc))

        item = {
            'pkey': f'EMPLOYEE-{employee_id}',
            'skey': f'DELETED_CONTRACT-{start_date}',
        }
        created = deleted_contract.get('created', None)
        if created:
            item['created'] = created

        weekly_hours = deleted_contract.get('weekly_hours', None)
        if weekly_hours:
            item['weekly_hours'] = weekly_hours

        hourly_rate = deleted_contract.get('hourly_rate', None)
        if hourly_rate:
            item['hourly_rate'] = hourly_rate

        key = {
            'pkey': f"EMPLOYEE-{employee_id}",
            'skey': f'CONTRACT-{start_date}',
        }
        with table.batch_writer() as batch:
            batch.put_item(Item=item)
            batch.delete_item(Key=key)
        return True
    except ClientError as ce:
        logger.critical(ce)
        return False
