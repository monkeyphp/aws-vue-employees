#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# This function is used to return a list of the Groups.

# ```bash
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/groups | python -m json.tool
# ```

# logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# env
TABLE_NAME = os.getenv('TABLE_NAME', 'employees-table')

# cached resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    groups = get_groups()
    if groups is False:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"Groups could not be located"
            })
        }

    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Expose-Headers': "*"
        },
        "body": json.dumps(groups)
    }


def get_groups():
    try:
        key_condition_expression = Key('skey').eq("GROUP")
        index_name = 'gsi-0'
        select = 'ALL_ATTRIBUTES'
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            IndexName=index_name,
            Select=select
        )
        groups = []
        items = response.get('Items', [])
        for item in items:

            group = {
                'group_id': item.get('pkey').replace('GROUP-', '', 1)
            }

            created = item.get('created', None)
            if created:
                group['created'] = created

            name = item.get('name', None)
            if name:
                group['name'] = name

            description = item.get('description', None)
            if description:
                group['description'] = description

            parent_group_id = item.get('parent_group_id', None)
            if parent_group_id:
                group['parent_group_id'] = parent_group_id

            groups.append(group)
        return groups
    except ClientError as ce:
        logger.critical(ce)
        return False


# if __name__ == '__main__':
#     print(lambda_handler({}, {}))
