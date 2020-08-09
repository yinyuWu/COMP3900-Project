import json
import boto3
import os
import uuid
import base64
from decimal import Decimal
s3 = boto3.client('s3')

# import requests
# environ variables
# change code path

dynamodb = boto3.resource('dynamodb')
advertisements_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])

def decode_image(image):
    image = image[image.find(",")+1:]
    dec = base64.b64decode(image + "===")
    return dec

def lambda_handler(event, context):
    advertisement_body = json.loads(event['body'])
    params = {}
    params['owner'] = advertisement_body['owner']
    params['ID'] = str(uuid.uuid4())
    params['title'] = advertisement_body.get('title')
    params['rent'] = int(advertisement_body.get('rent'))
    params['description'] = advertisement_body.get('description')
    params['active'] = True
    params['street'] = advertisement_body.get('street')
    params['aptNo'] = advertisement_body.get('aptNo')
    params['suburb'] = advertisement_body.get('suburb')
    params['city'] = advertisement_body.get('city')
    params['postcode'] = advertisement_body.get('postcode')
    params['photoURLs'] = advertisement_body.get('photoURLs')
    params['360PhotoURLs'] = advertisement_body.get('360PhotoURLs')
    params['averageReview'] = -1
    params['availability'] = {}
    if 'availability' in advertisement_body:
        for date in advertisement_body.get('availability'):
            params['availability'][date] = True
    # these are optional params
    if params['aptNo'] == '':
        del params['aptNo']
    print('Adding advertisement to table ', params)
    response = advertisements_table.put_item(Item=params)
    print('Advertisement added to table, done')
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps({
            "ID": params['ID'],
        }),
    }