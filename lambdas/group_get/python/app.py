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

# this function is used to retrieve the specified Group.

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

    group = get_group(group_id)
    if not group:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Group {group_id} could not be located"
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(group)
    }


def get_group(group_id: str) -> [dict, bool]:
    """ Return the Group identified by the supplied group_id.
    """
    try:
        key = {
            'pkey': f"GROUP-{group_id}",
            'skey': 'GROUP',
        }
        response = table.get_item(Key=key)

        item = response.get('Item', None)
        if not 'item':
            return False

        group = {
            'group_id': item.get('pkey').replace('GROUP-', '', 1)
        }

        name = item.get('name', None)
        if name:
            group['name'] = name

        description = item.get('description', None)
        if description:
            group['description'] = description

        parent_group_id = item.get('parent_group_id', None)
        if parent_group_id:
            group['parent_group_id'] = parent_group_id

        created = item.get('created', None)
        if created:
            group['created'] = created

        return group
    except ClientError as ce:
        logger.critical(ce)
        return False


if __name__ == '__main__':
    print(lambda_handler({
        'pathParameters': {
            'group_id': 'stores'
        }
    }, {}))
