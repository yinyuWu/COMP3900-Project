import boto3
import os
import json
import datetime
from boto3.dynamodb.conditions import Key

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

    body = json.loads(event['body'])
    bookingID = body['bookingID']

    print('Cancelling booking: %s' % (bookingID))
    response = booking_table.update_item(
        Key={'ID': bookingID}, UpdateExpression='SET cancelled = :value',
        ExpressionAttributeValues={
            ':value': True
        },
        ReturnValues="ALL_NEW"
    )

    bookingDetails = booking_table.query(
        KeyConditionExpression=Key('ID').eq(bookingID)
    )
    print(bookingDetails)
    advertisementDetails = advertisement_table.query(
        KeyConditionExpression=Key('ID').eq(bookingDetails['Items'][0]['advertisementID'])
    )
    print(advertisementDetails)

    print('Updated booking response:', response)
    updated_record = response['Attributes']
    _from = datetime.datetime.strptime(updated_record['from'], '%d-%m-%Y')
    _to = datetime.datetime.strptime(updated_record['to'], '%d-%m-%Y')
    advertisementID = updated_record['advertisementID']
    dateList = [date.strftime('%d-%m-%Y') for date in date_range(_from, _to)]
    day = len(dateList) - 1

    updateExpression = ','.join(['#ATTR.#FIELD%s = :value%s' %
                                 (i+1, i+1) for i in range(day)])
    expressionAttributeNames = {'#ATTR': 'availability'}
    expressionAttributeValues = {}
    for i in range(day):
        expressionAttributeNames['#FIELD' + str(i+1)] = dateList[i]
        expressionAttributeValues[':value' + str(i+1)] = True
    # change available date
    print('updateExpression', updateExpression)
    print('expressionAttributeNames', expressionAttributeNames)
    print('expressionAttributeValues', expressionAttributeValues)
    response = advertisement_table.update_item(Key={
        'ID': advertisementID
    }, UpdateExpression='SET ' + updateExpression,
        ExpressionAttributeNames=expressionAttributeNames,
        ExpressionAttributeValues=expressionAttributeValues,
        ReturnValues="UPDATED_NEW"
    )
    print('Changed available date on advertisement table:', response)
    print('Done')
    print(bookingDetails, advertisementDetails)
    bd = bookingDetails['Items'][0]
    ad = advertisementDetails['Items'][0]

    # send confirmation emails to tenant and owner
    subject = "Booking Cancelled"
    messageTenant = "Hi there,\nYour booking at '{}' for the dates '{} - {}' has been cancelled. Check the dashboard for more details.\n-Taxidi".format(ad['title'], bd['from'], bd['to'])
    messageOwner = "Hi there,\nThe tenant {}'s reservation at '{}' for the dates '{} - {}' has been cancelled. Check the dashboard for more details\n-Taxidi.".format(bd['tenant'], ad['title'], bd['from'], bd['to'])

    emailTenant = sendEmail(bd['tenant'], subject, messageTenant)
    emailOwner = sendEmail(ad['owner'], subject, messageOwner)
    print(emailTenant, emailOwner)
    if emailTenant['ResponseMetadata']['HTTPStatusCode'] != 202 or emailOwner['ResponseMetadata']['HTTPStatusCode'] != 202:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({'message': 'there was something wrong with sending the confirmation emails to the tenant and owner'})
        }


    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        'body': 'Booking is cancelled!!'
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
