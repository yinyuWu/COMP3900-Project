import json
import boto3
import os
from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key

# import requests

dynamodb = boto3.resource('dynamodb')
review_table = dynamodb.Table(os.environ["REVIEW_TABLE"])
advertisement_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])


def lambda_handler(event, context):
    advertisementID = event['pathParameters']['id']
    print('Getting cached average review for advertisement id: %s' % (advertisementID))
    fe = Key('ID').eq(advertisementID)
    response = advertisement_table.scan(FilterExpression=fe)
    advertisement = response['Items']
    if len(advertisement) == 0:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "message": "no ad for this id"
        }
    print(advertisement)
    advertisement = advertisement[0]
    if 'averageReview' not in advertisement:
        ratingAvg = -1
    else:
        ratingAvg = advertisement['averageReview']

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps(ratingAvg, cls=DecimalEncoder)
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
