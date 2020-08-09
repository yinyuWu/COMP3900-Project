import json
import boto3
import os
from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key

# import requests

dynamodb = boto3.resource('dynamodb')
advertisement_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])
booking_table = dynamodb.Table(os.environ["BOOKING_TABLE"])


def lambda_handler(event, context):
    owner = event['pathParameters']['owner']
    print('Getting advertisements with owner email: %s' % (owner))
    fe = Key('owner').eq(owner)
    response = advertisement_table.scan(FilterExpression=fe)
    bookings = []
    advertisements = response['Items']
    print(advertisements)
    for ad in advertisements:
        fe = Key('advertisementID').eq(ad['ID'])
        response = booking_table.scan(FilterExpression=fe)
        print(ad['ID'], response['Items'])
        bookings += response['Items']

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
