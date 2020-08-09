import boto3
import os
import requests
import json
from datetime import datetime, timedelta
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
ad_table = dynamodb.Table(os.environ["ADVERTISEMENT_TABLE"])

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):

    if 'body' not in event:
        return {
            "statusCode": 500,
            "body": "No review data body"
        }

    search_body = json.loads(event['body'])

    city = search_body['city']
    page = search_body['page']
    sortType = search_body['sortType']
    check_in = search_body['checkin']
    check_out = search_body['checkout']
    
 

    # Get desired city
    response = requests.post(
        'https://0rfkxyvpxe.execute-api.ap-southeast-2.amazonaws.com/Prod/algoliaSearch', json={'city':city, 'page':page, 'sortType':sortType})

    response_matching_list = response.json()["objectIDs"]
    nbPages =  response.json()["nbPages"]
    print(response)
    print(response_matching_list)

    if len(response_matching_list) == 0:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps([])
        }

    checkin = datetime.strptime(check_in, '%d-%m-%Y')
    checkout = datetime.strptime(check_out, '%d-%m-%Y')
    checkout_1 = checkout - timedelta(days=1)

    def check_booking_possible(dates: dict) -> bool:
        available = [k for (k, v) in dates.items() if v]
        if len(available) == 0:
            return False
        desired = date_range(checkin, checkout_1)
        for d in desired:
            if d not in available:
                return False
        return True

    def date_range(start, end):
        r = (end+timedelta(days=1)-start).days
        return [(start+timedelta(days=i)).strftime('%d-%m-%Y') for i in range(r)]

    hits_response = {}

    for match in response_matching_list:
        try:
            item = ad_table.query(KeyConditionExpression=Key('ID').eq(match))[
                'Items'][0]
            booking_ok = check_booking_possible(item['availability'])
        except IndexError:
            continue
        except KeyError:
            booking_ok = False
        finally:
            hit = {'title': item['title'],
                'rent': item['rent'],
                'description': item['description'],
                'rating': item['averageReview'],
                'images': item['photoURLs'],
                'ok': booking_ok,
                'objectID': item['ID']
            }
            hits_response[item['ID']] = hit
    
    output = {'hits_response': hits_response, 'nbPages': nbPages }
            
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps(output, cls=DecimalEncoder)
    }
