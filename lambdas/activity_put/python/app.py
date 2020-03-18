#!/usr/bin/env python
import boto3
import os
import logging
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# This function is used to update the specified Activity.

# ```
# curl -XPUT -d '{"name": "working"}' https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/activities/worked | python -m json.tool
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
                "message": f"An Activity id is required"
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

    code = body.get('code', None)
    if code is None:
        code = name.lower().replace(' ', '-').replace('/', '-')

    activity = {
        'activity_id': activity_id,
        'name': name,
        'code': code,
    }

    description = body.get('description', None)
    if description:
        activity['description'] = description

    worked = body.get('worked', False)
    activity['worked'] = worked

    updated_activity = update_activity(activity)
    if updated_activity is False:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Activity {activity_id} could not be updated"
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(updated_activity)
    }


def update_activity(activity: dict) -> [dict, bool]:
    """ Update the activity by updating or removing attributes. """
    try:
        activity_id = activity.get('activity_id')

        key = {
            'pkey': f'ACTIVITY-{activity_id}',
            'skey': 'ACTIVITY',
        }

        update_expressions = {
            'SET': [],
            'REMOVE': [],
        }
        expression_attribute_values = {}
        expression_attribute_names = {}

        # name and code should always be supplied
        name = activity.get('name')
        update_expressions['SET'].append('#name = :name')
        expression_attribute_names['#name'] = 'name'
        expression_attribute_values[':name'] = name

        code = activity.get('code')
        update_expressions['SET'].append('#code = :code')
        expression_attribute_names['#code'] = 'code'
        expression_attribute_values[':code'] = code

        # description is optional so we might need to remove
        description = activity.get('description', None)
        if description:
            update_expressions['SET'].append('#description = :description')
            expression_attribute_names['#description'] = 'description'
            expression_attribute_values[':description'] = description
        else:
            update_expressions['REMOVE'].append('description')

        # worked is a boolean (defaults to False)
        worked = activity.get('worked', False)
        update_expressions['SET'].append('#worked = :worked')
        expression_attribute_names['#worked'] = 'worked'
        expression_attribute_values[':worked'] = worked

        # create the update expression string
        update_expression = ' '.join(
            action + ' ' + ', '.join(values)
            for action, values in update_expressions.items()
            if values
        )
        return_values = 'ALL_NEW'

        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues=return_values
        )
        logger.critical("#RESPONSE")
        logger.critical(response)

        attributes = response.get('Attributes', None)
        if not attributes:
            return False

        created = attributes.get('created', None)
        if created:
            activity['created'] = created

        return activity
    except ClientError as ce:
        logger.critical(ce)
        return False


# if __name__ == '__main__':
#     response = lambda_handler({
#         "pathParameters": {
#             "activity_id": "worked"
#         },
#         "body": json.dumps({
#             "name": "Wooooed",
#             "code": "WooWoo",
#             "description": "My description"
#         })
#     }, {})
#     print(response)
