import json
import boto3
import decimal
import os
import base64
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
booking_table = dynamodb.Table(os.environ["BOOKING_TABLE"])

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    id = event['pathParameters']['id']
    response = booking_table.get_item(Key={'ID': id})
    booking = response.get('Item', '')
    if booking == '':
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "message": "no ad for this id"
        }
    
    print(booking)
    print('Done')

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps(booking, cls=DecimalEncoder)
    }
