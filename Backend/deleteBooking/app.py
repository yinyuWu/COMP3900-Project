import boto3
import os
import json
import datetime

dynamodb = boto3.resource('dynamodb')
advertisement_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])
booking_table = dynamodb.Table(os.environ["BOOKING_TABLE"])


def lambda_handler(message, context):

    bookingID = message['pathParameters']['id']

    print('Deleting booking: %s' % (bookingID))
    response = booking_table.delete_item(
        Key={'ID': bookingID}, ReturnValues="ALL_OLD")

    print('Deleting booking response:', response)
    deleted_record = response['Attributes']
    _from = datetime.datetime.strptime(deleted_record['from'], '%d-%m-%Y')
    _to = datetime.datetime.strptime(deleted_record['to'], '%d-%m-%Y')
    advertisementID = deleted_record['advertisementID']
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

    return {
        'statusCode': 204,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        'body': 'Booking deleted!!'
    }


def date_range(start, end):
    r = (end+datetime.timedelta(days=1)-start).days
    return [start+datetime.timedelta(days=i) for i in range(r)]
