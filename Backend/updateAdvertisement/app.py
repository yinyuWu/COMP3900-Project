import json
import boto3
import os
import uuid
import base64
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
advertisements_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])
s3 = boto3.client('s3')


def decode_image(image):
    image = image[image.find(",")+1:]
    dec = base64.b64decode(image + "===")
    return dec


def lambda_handler(event, context):
    advertisement_body = json.loads(event['body'])
    advertisement_id = advertisement_body['id']
    params = {}
    params['title'] = advertisement_body.get('title')
    params['rent'] = int(advertisement_body.get('rent'))
    params['description'] = advertisement_body.get('description')
    params['city'] = advertisement_body.get('city')
    params['aptNo'] = advertisement_body.get('aptNo')
    params['suburb'] = advertisement_body.get('suburb')
    params['street'] = advertisement_body.get('street')
    params['postcode'] = advertisement_body.get('postcode')
    params['availability'] = advertisement_body.get('availability')
    params['photoURLs'] = advertisement_body.get('photoURLs')
    params['360PhotoURLs'] = advertisement_body.get('360PhotoURLs')

    update_dates = {}
    remove_dates = []

    for date in params['availability']:
        if params['availability'][date]:
            update_dates[date] = params['availability'][date]
        else:
            remove_dates.append(date)

    print('Updating advertisement to table ', params)

    updateExpression = "set title = :t, rent=:r, description=:d, city=:c, aptNo=:a, street=:s, suburb=:sub, postcode=:p, photoURLs=:photourls, #PHOTO360=:photourls360"
    expressionAttributeNames = {
        '#ATTR': 'availability', '#PHOTO360': '360PhotoURLs'}
    expressionAttributeValues = {
        ':t': params['title'],
        ':r': params['rent'],
        ':d': params['description'],
        ':c': params['city'],
        ':a': params['aptNo'],
        ':s': params['street'],
        ':p': params['postcode'],
        ':sub': params['suburb'],
        ':photourls': params['photoURLs'],
        ':photourls360': params['360PhotoURLs']
    }
    for i, (k, v) in enumerate(update_dates.items()):
        updateExpression += (', #ATTR.#FIELD%s = :value%s' % (i+1, i+1))
        expressionAttributeNames['#FIELD' + str(i+1)] = k
        expressionAttributeValues[':value' + str(i+1)] = v

    if len(remove_dates) > 0:
        updateExpression += ' REMOVE '
        updateExpression += ', '.join(['#ATTR.#R_FIELD%s' % str(i+1)
                                       for i in range(len(remove_dates))])
    for i in range(len(remove_dates)):
        expressionAttributeNames['#R_FIELD%s' % str(i+1)] = remove_dates[i]

    print('updateExpression', updateExpression)
    print('expressionAttributeNames', expressionAttributeNames)
    print('expressionAttributeValues', expressionAttributeValues)
    response = advertisements_table.update_item(Key={
        'ID': advertisement_id
    }, UpdateExpression=updateExpression,
        ExpressionAttributeNames=expressionAttributeNames,
        ExpressionAttributeValues=expressionAttributeValues,
        ReturnValues="UPDATED_NEW")

    print('Advertisement updated to table, done')

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps(response, cls=DecimalEncoder),
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
