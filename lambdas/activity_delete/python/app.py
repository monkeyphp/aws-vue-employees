#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key

# This function is used to delete the specified Activity.

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
            "statusCode": 404,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*",
            },
            'body': json.dumps({
                'message': f'Activity {activity_id} could not be located'
            })
        }

    deleted = delete_activity(activity)

    if not deleted:
        return {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': "*",
            },
            'body': json.dumps({
                'message': f'Activity {activity_id} could not be deleted'
            })
        }

    return {
        "statusCode": 204,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
        }
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
        if not item:
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


def delete_activity(activity: dict) -> bool:
    """ Delete the supplied Activity.
    """
    try:
        activity_id = activity.get('activity_id')
        deleted_activity = activity.copy()
        deleted_activity['deleted'] = datetime.now().replace(microsecond=0).isoformat()

        item = {
            'pkey': f'ACTIVITY-{activity_id}',
            'skey': 'DELETED_ACTIVITY',
        }

        created = deleted_activity.get('created', None)
        if created:
            item['created'] = created

        name = deleted_activity.get('name', None)
        if name:
            item['name'] = name

        code = deleted_activity.get('code', None)
        if code:
            item['code'] = code

        description = deleted_activity.get('description', None)
        if description:
            item['description'] = description

        worked = deleted_activity.get('worked', False)
        item['worked'] = worked

        key = {
            'pkey': f'ACTIVITY-{activity_id}',
            'skey': 'ACTIVITY'
        }

        with table.batch_writer() as batch:
            batch.put_item(Item=item)
            batch.delete_item(Key=key)
        return True
    except ClientError as ce:
        logger.critical(ce)
        return False


# if __name__ == '__main__':
#     response = lambda_handler({
#         'pathParameters': {
#             'activity_id': 'holiday'
#         }
#     }, {})
#     print(response)
