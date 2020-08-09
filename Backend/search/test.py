import json
from datetime import datetime, timedelta
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
ad_table = dynamodb.Table('Advertisements')

response_matching_list = ['d5baaf09-15bd-471e-b0ca-ce1f2632984e', 'b800ca10-edb1-4f3b-8503-f9af601d6366', 'aeb7daad-0440-4918-8b9c-cc03f3b2ee4d',
                          '7182c491-5a56-4123-9ef3-1ffea9536721', '12ffec29-a75b-4367-aef1-4db79626b0f5', '0e1ae4e0-6298-4e04-8c51-9a6ffd71b8bc']
#response_matching_list = ['0e1ae4e0-6298-4e04-8c51-9a6ffd71b8bc']

checkin = datetime.strptime('01-05-2020', '%d-%m-%Y')
checkout = datetime.strptime('03-05-2020', '%d-%m-%Y')
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


hits_response = []

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
        hits_response.append({
            'title': item['title'],
            'rent': item['rent'],
            'description': item['description'],
            'rating': '5',
            'images': item['photoURLs'],
            'ok': booking_ok
        })

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

print(hits_response)
json.dumps(hits_response, cls=DecimalEncoder)