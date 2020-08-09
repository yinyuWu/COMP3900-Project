import json
import boto3
import decimal
import os
import base64
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key

# import requests

dynamodb = boto3.resource('dynamodb')
ad_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])
s3 = boto3.resource('s3')
BUCKET_NAME = 'taxidi-photo'


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def check_booking_possible(check_in: str, check_out: str, avaialble_dates: dict) -> bool:
    checkin = datetime.strptime(check_in, '%d-%m-%Y')
    checkout = datetime.strptime(check_out, '%d-%m-%Y')
    checkout_1 = checkout - timedelta(days=1)
    desired_dates = date_range(checkin, checkout_1)

    for date in desired_dates:
        if date not in avaialble_dates or (not avaialble_dates[date]):
            return False
    return True


def date_range(start, end):
    r = (end+timedelta(days=1)-start).days
    return [(start+timedelta(days=i)).strftime('%d-%m-%Y') for i in range(r)]


def lambda_handler(event, context):
    print(event)
    checkin = '' if event.get('queryStringParameters') == None else event['queryStringParameters'].get(
        'checkin', '')
    checkout = '' if event.get('queryStringParameters') == None else event['queryStringParameters'].get(
        'checkout', '')

    id = event['pathParameters']['id']
    print('Getting advertisement with id : %s' % (id))
    response = ad_table.get_item(Key={'ID': id})
    ad = response.get('Item', '')

    # there should only be one ad matching the id
    if ad == '':
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "message": "no ad for this id"
        }
    if checkin and checkout:
        ad['availableToBook'] = check_booking_possible(
            checkin, checkout, ad['availability'])
    print(ad)
    print('Done')

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps(ad, cls=DecimalEncoder)
    }
