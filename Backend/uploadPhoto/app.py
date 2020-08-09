import json
import boto3
import os
from decimal import Decimal
import base64s3 = boto3.client('s3')

def lambda_handler(event, context):
    print event
    if event['httpMethod'] == 'POST' : 
        print event['body']
        data = json.loads(event['body'])
        name = data['name']
        image = data['file']
        image = image[image.find(",")+1:]
        dec = base64.b64decode(image + "===")
        key = str(uuid.uuid4())
        s3.put_object(Bucket='taxidi-photo', Key=key, Body=dec)
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            'body': json.dumps({'ID': key})
        }
