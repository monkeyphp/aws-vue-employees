#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# This function is used to retrieve the specified Activity.

# ```
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/activities/worked | python -m json.tool
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
                "message": f"An Activity Id is required"
            })
        }

    activity_id = path_parameters.get('activity_id', None)
    if not activity_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"An Activity Id is required"
            })
        }

    activity = get_activity(activity_id)
    if not activity:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Activity {activity_id} could not be located"
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(activity)
    }


def get_activity(activity_id: str) -> [dict, bool]:
    """ Return the Activity identified by activity_id """
    try:
        key = {
            'pkey': f"ACTIVITY-{activity_id}",
            'skey': 'ACTIVITY',
        }
        response = table.get_item(Key=key)
        item = response.get('Item', None)
        if not 'item':
            return False

        activity = {
            'activity_id': item.get('pkey').replace('ACTIVITY-', '', 1)
        }

        code = item.get('code', None)
        if code:
            activity['code'] = code

        created = item.get('created', None)
        if created:
            activity['created'] = created

        name = item.get('name', None)
        if name:
            activity['name'] = name

        description = item.get('description', None)
        if description:
            activity['description'] = description

        worked = item.get('worked', False)
        activity['worked'] = worked

        return activity
    except ClientError as ce:
        logger.critical(ce)
        return False
