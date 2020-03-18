#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timezone

# This function is used to POST an Activity to the api.
#
# Accepted values:
# - name: The name of the Activity
# - code: The client supplied code for the Activity. This will be auto-generated if not supplied.
# - description: The description for the Activity.


# ```bash
# curl -d '{}'  https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/activities | python -m json.tool
# curl -d '{"name": "time in lieu"}'  https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/activities | python -m json.tool
# curl -d '{"name": "Worked", "code": "W"}'  https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/activities | python -m json.tool
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
                "message": f"A name value is required"
            })
        }

    code = body.get('code', None)
    if code is None:
        code = name.lower().replace(' ', '-').replace('/', '-')

    # generate the activity_id
    activity_id = name.lower().replace(' ', '-').replace('/', '-')

    # store dates in isoformat
    # created = str(datetime.now(timezone.utc))
    # created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    created = datetime.now().replace(microsecond=0).isoformat()

    activity = {
        'activity_id': activity_id,
        'name': name,
        'code': code,
        'created': created,
    }

    description = body.get('description', None)
    if description:
        activity['description'] = description

    worked = body.get('worked', False)
    activity['worked'] = worked

    saved = save_activity(activity)
    if not saved:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"Activity could not be saved"
            })
        }

    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Location': f"/activities/{activity_id}"
        },
        'body': json.dumps(activity)
    }


def save_activity(activity: dict) -> bool:
    """ Save the Activity """
    try:
        activity_id = activity.get('activity_id')
        name = activity.get('name')
        created = activity.get('created')

        item = {
            'pkey': f'ACTIVITY-{activity_id}',
            'skey': 'ACTIVITY',
            'name': name,
            'created': created,
        }

        code = activity.get('code', None)
        if code:
            item['code'] = code

        description = activity.get('description', None)
        if description:
            item['description'] = description

        worked = activity.get('worked', False)
        item['worked'] = worked

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
#     response = lambda_handler(
#         {"body": json.dumps({"name": "Test"})},
#         {}
#     )
#     print(response['body'])

#     print(lambda_handler(
#         {"body": json.dumps({"name": "Break", "code": "B"})},
#         {}
#     ))
#     print(lambda_handler(
#         {"body": json.dumps({"name": "Holiday", "code": "H", "description": "On holiday"})},
#         {}
#     ))

