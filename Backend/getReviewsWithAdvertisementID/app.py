import json
import boto3
import os
from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key

# import requests

dynamodb = boto3.resource('dynamodb')
review_table = dynamodb.Table(os.environ["REVIEW_TABLE"])


def lambda_handler(event, context):

    advertisementID = event['pathParameters']['id']
    print('Getting reviews with advertisement id: %s' % (advertisementID))
    response = review_table.query(KeyConditionExpression=Key(
        'advertisementID').eq(advertisementID))
    reviews = response['Items']
    print(reviews)
    print('Done')

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps(reviews, cls=DecimalEncoder)
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
