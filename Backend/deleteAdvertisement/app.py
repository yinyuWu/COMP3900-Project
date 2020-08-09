import boto3
import os
import json


def lambda_handler(message, context):
    print(message)

    adId = message['pathParameters']['id']

    print('Deleting ad %s from table %s' %
          (adId, os.environ['ADVERTISEMENT_TABLE']))
    client = boto3.client('dynamodb')
    response = client.delete_item(
        TableName=os.environ['ADVERTISEMENT_TABLE'], Key={'ID': {'S': adId}})
    print(response)
    print('Done')

    return {
        'statusCode': 204,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        'body': ''
    }
