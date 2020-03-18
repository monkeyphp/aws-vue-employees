#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# This function is used to retrieve a list of Activities that can be used to record
# what the Employee was doing during a Timesheet Entry.

# ```bash
# curl https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/activities | python -m json.tool
# ```

# ```bash
# python app.py | python -m json.tool
# ```

# activity = {
#     'activity_id': 'worked',
#     'name': 'Worked',
#     'code': 'W',
#     'description': 'The Employee was working',
#     'worked': true,
#     'created': '2020-01-01T13:45:34',
# }

# logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# env
TABLE_NAME = os.getenv('TABLE_NAME', 'employees-table')

# cached resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    activities = get_activities()
    if activities is False:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"Activities could not be located"
            })
        }
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
        },
        "body": json.dumps(activities)
    }


def get_activities() -> [list, bool]:
    """ Return a list of Activities. """
    try:
        key_condition_expression = Key('skey').eq("ACTIVITY")
        index_name = 'gsi-0'
        select = 'ALL_ATTRIBUTES'
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            IndexName=index_name,
            Select=select
        )
        activities = []
        items = response.get('Items', [])
        for item in items:
            activity = {
                'activity_id': item.get('pkey').replace('ACTIVITY-', '', 1)
            }
            name = item.get('name', None)
            if name:
                activity['name'] = name

            code = item.get('code', None)
            if code:
                activity['code'] = code

            created = item.get('created', None)
            if created:
                activity['created'] = created

            description = item.get('description', None)
            if description:
                activity['description'] = description

            worked = item.get('worked', False)
            activity['worked'] = worked

            activities.append(activity)
        return activities
    except ClientError as ce:
        logger.critical(ce)
        return False


# if __name__ == '__main__':
#     response = lambda_handler({}, {})
#     print(response['body'])
