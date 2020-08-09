import json
import boto3
import decimal
import os
from datetime import datetime
from boto3.dynamodb.conditions import Key

# import requests

dynamodb = boto3.resource('dynamodb')
ad_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):

    ownerEmail = event['pathParameters']['email']
    print('Getting advertisements of : %s' % (ownerEmail))
    fe = Key('owner').eq(ownerEmail)
    response = ad_table.scan(FilterExpression=fe)
    ads = response['Items']
    print(ads)
    print('Done')

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps(ads, cls=DecimalEncoder)
    }
