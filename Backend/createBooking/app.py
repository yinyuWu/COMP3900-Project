import json
import boto3
import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import os
import sys
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
advertisement_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])
booking_table = dynamodb.Table(os.environ["BOOKING_TABLE"])
lambda_client = boto3.client('lambda')


def lambda_handler(event, context):

    if 'body' not in event:
        return {
            "statusCode": 500,
            "body": "No review data body"
        }

    booking_body = json.loads(event['body'])
    advertisementID = booking_body['advertisementID']
    email = booking_body['email']
    _from = datetime.datetime.strptime(booking_body['from'], '%d-%m-%Y')
    _to = datetime.datetime.strptime(booking_body['to'], '%d-%m-%Y')
    dateList = [date.strftime('%d-%m-%Y') for date in date_range(_from, _to)]
    day = len(dateList) - 1
    _from = dateList[0]
    _to = dateList[-1]

    updateExpression = ','.join(['#ATTR.#FIELD%s = :value%s' %
                                 (i+1, i+1) for i in range(day)])
    expressionAttributeNames = {'#ATTR': 'availability'}
    expressionAttributeValues = {}
    for i in range(day):
        expressionAttributeNames['#FIELD' + str(i+1)] = dateList[i]
        expressionAttributeValues[':value' + str(i+1)] = False
    # change available date
    # print('updateExpression', updateExpression)
    # print('expressionAttributeNames', expressionAttributeNames)
    # print('expressionAttributeValues', expressionAttributeValues)
    response = advertisement_table.update_item(Key={
        'ID': advertisementID
    }, UpdateExpression='SET ' + updateExpression,
        ExpressionAttributeNames=expressionAttributeNames,
        ExpressionAttributeValues=expressionAttributeValues,
        ReturnValues="UPDATED_NEW"
    )
    print('Changed available date on advertisement table:', response)

    # add a record to booking table
    bookingID = str(uuid.uuid4())
    booking = {
        'ID': bookingID,
        'advertisementID': advertisementID,
        'tenant': email,
        'cancelled': False,
        'from': _from,
        'to': _to,
        'day': day,
        'timestamp': int(datetime.datetime.now().timestamp())
    }

    print('Adding booking:', booking)
    response = booking_table.put_item(Item=booking)
    print(response)
    print('Done')

    # get information on the advertisement that the booking is for
    adResponse = lambda_client.invoke(
        FunctionName="taxidi-getSingleAdvertisement",
        InvocationType='RequestResponse', # run syncronously
        Payload=json.dumps({"pathParameters": {"id": advertisementID}})
    )
    adResponsePayload = json.loads(adResponse['Payload'].read().decode("utf-8"))
    print(adResponsePayload)
    if adResponsePayload.get('statusCode') != 200 or adResponsePayload.get('body') == None:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({'bookingID': bookingID, 'message': 'there was something wrong with getting the advertisement details'})
        }
    adBody = json.loads(adResponsePayload['body'])
    print(adBody)

    # send confirmation emails to tenant and owner
    emailTenant = sendEmail(email, "Booking Made!", "Hi there,\nYour booking at {} for the dates {} - {} has been made!\n-Taxidi".format(adBody['title'], _from, _to))
    emailOwner = sendEmail(adBody['owner'], "Someone has booked your property!", "Hi there,\nGood news! {} has requested to stay at your property '{}' for the dates {} - {}!\n-Taxidi".format(email, adBody['title'], _from, _to))
    print(emailTenant, emailOwner)
    if emailTenant['ResponseMetadata']['HTTPStatusCode'] != 202 or emailOwner['ResponseMetadata']['HTTPStatusCode'] != 202:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({'bookingID': bookingID, 'message': 'there was something wrong with sending the confirmation emails to the tenant and owner'})
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps({'bookingID': bookingID})
    }

def sendEmail(recipient, subject, body):
    jsonBody = json.dumps({
        "recipient": recipient,
        "body": body,
        "subject": subject
    })
    response = lambda_client.invoke(
        FunctionName="taxidi-email",
        InvocationType='Event',
        Payload=json.dumps({"body": jsonBody})
    )
    return response
    

def date_range(start, end):
    r = (end+datetime.timedelta(days=1)-start).days
    return [start+datetime.timedelta(days=i) for i in range(r)]
