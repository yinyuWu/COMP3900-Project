import json
import boto3
import os
import uuid
import base64

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')


def decode_image(image):
    image = image[image.find(",")+1:]
    dec = base64.b64decode(image + "===")
    return dec


def lambda_handler(event, context):
    print(event)
    image = event['body']
    dec = decode_image(image)

    key = 'photos/' + str(uuid.uuid4()) + '.jpg'
    s3.put_object(Bucket='taxidi-photo', Key=key, Body=dec,
                  ACL='public-read', ContentType='image/jpeg')
    print(key)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": key
    }