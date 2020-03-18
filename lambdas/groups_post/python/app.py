#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from datetime import timezone
from dateutil.parser import parse
import uuid

# This function is used to create a new Group.

# ```python
# group = {
#   'group_id': 'all',
#   'name': 'ALL',
#   'parent_group_id': None,
#   'description': 'The default ALL group'
# }
# ```

# ```bash
# curl -d '{"name": "Test", "description": "Test Group"}'  https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/groups | python -m json.tool
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

    # @todo clean the supplied name
    name = name.strip()

    group_id = body.get('group_id', name)
    group_id = group_id.lower().replace(' ', '-').replace('/', '-')

    # by default - groups are added to the `all` group
    parent_group_id = body.get('parent_group_id', 'all')

    created = datetime.now().replace(microsecond=0).isoformat()
    group = {
        'name': name,
        'group_id': group_id,
        'created': created,
        'parent_group_id': parent_group_id
    }

    description = body.get('description', None)
    if description:
        group['description'] = description

    # if this is the 'all' group - remove the parent_group_id
    if group['group_id'] == 'all':
        del group['parent_group_id']

    saved = save_group(group)
    if not saved:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                "message": f"Group could not be saved"
            })
        }

    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Location': f"/groups/{group_id}"
        },
        'body': json.dumps(group)
    }


def save_group(group: dict) -> bool:
    """ Function that saves the supplied Group.
    """
    try:
        group_id = group.get('group_id')
        name = group.get('name')

        item = {
            'pkey': f'GROUP-{group_id}',
            'skey': 'GROUP',
            'name': name,
        }

        created = group.get('created', None)
        if created:
            item['created'] = created

        parent_group_id = group.get('parent_group_id', None)
        if parent_group_id:
            item['parent_group_id'] = parent_group_id

        description = group.get('description', None)
        if description:
            item['description'] = description

        condition_expression = Attr('pkey').not_exists()
        table.put_item(
            Item=item,
            ConditionExpression=condition_expression
        )
        return True
    except ClientError as ce:
        logger.critical(ce)
        return False


# if __name__ == '__main__':
#     print(lambda_handler({
#         'body': json.dumps({
#             'name': 'All',
#             'description': 'All Group',
#         })
#     }, {}))
#     print(lambda_handler({
#         'body': json.dumps({
#             'name': 'Stores',
#             'description': 'All Stores Group',
#         })
#     }, {}))
