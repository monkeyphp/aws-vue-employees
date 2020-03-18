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

# this function is used to delete the specified Group.

# @todo - handle moving the (sub) Groups and Employees to another Group.

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

    if group_id == 'all':
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({
                "message": f"Group {group_id} could not be deleted"
            })
        }

    # group = get_group(group_id)
    # if not group:
    #     return {
    #         'statusCode': 404,
    #         'body': json.dumps({
    #             "message": f"Group {group_id} could not be located"
    #         })
    #     }

    deleted = delete_group(group_id)
    if not deleted:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"Group {group_id} could not be deleted"
            })
        }

    return {
        'statusCode': 204,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        }
    }


def get_group(group_id: str) -> [bool, dict]:
    ...


def delete_group(group_id: str) -> bool:
    """ Delete the Group identified by the supplied group_id.
    """
    try:
        key = {
            'pkey': 'GROUP-' + group_id,
            'skey': 'GROUP'
        }
        table.delete_item(Key=key)
        return True
    except ClientError as ce:
        logger.critical(ce)
        return False


if __name__ == '__main__':
    print(lambda_handler({
        'pathParameters': {
            'group_id': 'all',
        }
    }, {}))