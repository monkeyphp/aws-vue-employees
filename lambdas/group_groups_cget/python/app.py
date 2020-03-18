#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# This function is used to return a list of the Groups that belong to the specified Group.

# ```bash
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/groups/all/groups | python -m json.tool
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

    groups = get_groups(group_id)
    if groups is False:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Groups for Group {group_id} could not be located"
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(groups)
    }


def get_groups(group_id: str) -> [list, bool]:
    try:
        key_condition_expression = Key('parent_group_id').eq(f'{group_id}') \
                                   & Key('pkey').begins_with('GROUP-')
        index_name = 'gsi-1'
        select = 'ALL_ATTRIBUTES'
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            IndexName=index_name,
            Select=select,
        )

        groups = []
        items = response.get('Items', [])
        for item in items:
            group = {
                'group_id': item.get('pkey').replace('GROUP-', '', 1),
                'parent_group_id': item.get('parent_group_id')
            }
            groups.append(group)
        return groups
    except ClientError as ce:
        logger.critical(ce)
        return False
