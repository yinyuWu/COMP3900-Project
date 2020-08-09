import json
import boto3
from datetime import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import os
import sys

# import requests

dynamodb = boto3.resource('dynamodb')
review_table = dynamodb.Table(os.environ["REVIEW_TABLE"])
advertisement_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])



def lambda_handler(event, context):

    if 'body' not in event:
        return {
            "statusCode": 500,
            "body": "No review data body"
        }

    review_body = json.loads(event['body'])
    review = {
        'advertisementID': review_body['advertisementID'],
        'bookingID': review_body['bookingID'],
        'rating': Decimal(review_body['rating']),
        'review': review_body['review'],
        'reviewer': review_body['reviewer'],
        'timestamp': int(datetime.now().timestamp())
    }

    print('Adding review:', review)
    response = review_table.put_item(Item=review)
    print(response)
    print('Done')

    advertisementID = review_body['advertisementID']
    print('Getting reviews with advertisement id: %s' % (advertisementID))
    response = review_table.query(KeyConditionExpression=Key(
        'advertisementID').eq(advertisementID))
    reviews = response['Items']
    print(reviews)
    print('Done')

    nReviews = len(reviews)
    ratingSum = 0
    for n in range(0, nReviews):
        ratingSum = ratingSum + reviews[n]['rating']

    if (nReviews == 0):
        ratingAvg = -1
    else:
        ratingAvg = ratingSum/nReviews

    response = advertisement_table.update_item(Key={
        'ID': advertisementID
    }, UpdateExpression="set averageReview = :r",
        ExpressionAttributeValues={
        ':r': ratingAvg
    },
    ReturnValues="UPDATED_NEW")


    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": "Review added!"
    }
