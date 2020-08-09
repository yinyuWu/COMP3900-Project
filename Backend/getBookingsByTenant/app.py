import json
import boto3
import os
from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key

# import requests

dynamodb = boto3.resource('dynamodb')
booking_table = dynamodb.Table(os.environ["BOOKING_TABLE"])


def lambda_handler(event, context):
    tenant = event['pathParameters']['tenant']
    print('Getting bookings with tenant email: %s' % (tenant))
    fe = Key('tenant').eq(tenant)
    response = booking_table.scan(FilterExpression=fe)
    bookings = response['Items']
    print(bookings)
    print('Done')

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps(bookings, cls=DecimalEncoder)
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
