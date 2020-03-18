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

# This function is used to delete the specified Employee.
# This process requires 3 db actions:
# - 1 read
# - 1 put
# - 1 delete

#
# curl -XDELETE https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/employees/2002 | python -m json.tool
#

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
                "message": f"An Employee Id is required"
            })
        }

    employee_id = path_parameters.get('employee_id', None)
    if not employee_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": f"An Employee Id is required"
            })
        }

    employee = get_employee(employee_id)
    if not employee:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": f"Employee {employee_id} could not be located"
            })
        }

    deleted = delete_employee(employee)
    if not deleted:
        return {
            'statusCode': 500,
            'body': json.dumps({
                "message": f"Employee {employee_id} could not be deleted"
            })
        }

    return {
        'statusCode': 204,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*"
        }
    }


def get_employee(employee_id: str) -> [dict, bool]:
    """ Return the Employee identified by employee_uuid """
    try:
        key = {
            'pkey': f"EMPLOYEE-{employee_id}",
            'skey': 'EMPLOYEE',
        }
        response = table.get_item(Key=key)
        item = response.get('Item', None)
        if item is None:
            return False
        employee = {
            'employee_id': item.get('pkey').replace('EMPLOYEE-', '', 1)
        }

        created = item.get('created', None)
        if created:
            employee['created'] = created

        name = item.get('name', None)
        if name:
            employee['name'] = name

        parent_group_id = item.get('parent_group_id', None)
        if parent_group_id:
            employee['parent_group_id'] = parent_group_id

        return employee
    except ClientError as ce:
        logger.critical(ce)
        return False


def delete_employee(employee: dict) -> bool:
    """ Delete the supplied Employee.
        This function will copy the Employee to delete - changing its skey  to `DELETED_`
        before saving it back to the db.
        This function will also delete the original Employee record.
    """
    try:
        employee_id = employee.get('employee_id')
        deleted_employee = employee.copy()
        deleted_employee['deleted'] = str(datetime.now(timezone.utc))
        item = {
            'pkey': f'EMPLOYEE-{employee_id}',
            'skey': 'DELETED_EMPLOYEE',
        }
        created = deleted_employee.get('created', None)
        if created:
            item['created'] = created

        name = deleted_employee.get('name', None)
        if name:
            item['name'] = name

        parent_group_id = deleted_employee.get('parent_group_id', None)
        if parent_group_id:
            item['parent_group_id'] = parent_group_id

        key = {
            'pkey': f"EMPLOYEE-{employee_id}",
            'skey': 'EMPLOYEE',
        }
        with table.batch_writer() as batch:
            batch.put_item(Item=item)
            batch.delete_item(Key=key)
        return True
    except ClientError as ce:
        logger.critical(ce)
        return False


# if __name__ == '__main__':
#     response = lambda_handler(
#         {
#             "pathParameters": {
#                 "employee_id": "1000"
#             }
#         },
#         {}
#     )
#     print(response)
