#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key,Attr
from datetime import datetime
from datetime import timezone
from dateutil.parser import parse

# this function is used to update the specified Group.

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

    group = {
        'group_id': group_id,
        'name': name,
    }

    description = body.get('description', None)
    if description:
        group['description'] = description

    # parent group defaults to `all`
    parent_group_id = body.get('parent_group_id', 'all')
    group['parent_group_id'] = parent_group_id
    # unless the group_id is 'all'
    if group_id == 'all':
        del group['parent_group_id']

    updated_group = update_group(group)
    if updated_group is False:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Group {group_id} could not be updated"
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(updated_group)
    }


def update_group(group: dict) -> [bool, dict]:
    try:
        group_id = group.get('group_id')
        key = {
            'pkey': f'GROUP-{group_id}',
            'skey': 'GROUP'
        }

        update_expressions = {
            'SET': [],
            'REMOVE': []
        }

        expression_attribute_values = {}
        expression_attribute_names = {}

        # name should always be supplied
        name = group.get('name')
        update_expressions['SET'].append('#name = :name')
        expression_attribute_names['#name'] = 'name'
        expression_attribute_values[':name'] = name

        # description
        description = group.get('description', None)
        if description:
            update_expressions['SET'].append('#description = :description')
            expression_attribute_names['#description'] = 'description'
            expression_attribute_values[':description'] = description
        else:
            update_expressions['REMOVE'].append('description')

        # parent_group_id is required if group_id is NOT 'all'
        if group_id != 'all':
            parent_group_id = group.get('parent_group_id')
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
            group['created'] = created

        return group
    except ClientError as ce:
        logger.critical(ce)
        return False


if __name__ == '__main__':
    print(lambda_handler({
        'pathParameters': {
            'group_id': 'foo',
        },
        'body': json.dumps({
            'description': 'All Group',
            'name': 'All',
            'parent_group_id': 'all',
        }),
    }, {}))
