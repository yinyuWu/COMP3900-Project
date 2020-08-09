import json
import boto3
import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import os
import sys
import uuid
import smtplib
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
advertisement_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])
booking_table = dynamodb.Table(os.environ["BOOKING_TABLE"])
gmail_user = 'taxidi.notifications@gmail.com'
gmail_password = '9g%rJAgd86X348U'

def lambda_handler(event, context):

    if 'body' not in event:
        return {
            "statusCode": 500,
            "body": "No email data body"
        }
    print(event)
    emailDetails = json.loads(event['body'])
    recipient = emailDetails['recipient']
    subject = emailDetails['subject']
    body = emailDetails['body']
    print(emailDetails)

    message = 'Subject: {}\n\n{}'.format(subject, body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, message)
        server.close()
    except:
        print('Email failed to send.')
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": "Email didn't send."
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": "Email sent successfully!"
    }


def date_range(start, end):
    r = (end+datetime.timedelta(days=1)-start).days
    return [start+datetime.timedelta(days=i) for i in range(r)]
