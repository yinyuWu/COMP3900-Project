import json
import uuid
import random
import requests
import boto3
from bs4 import BeautifulSoup
from tqdm import tqdm

s3 = boto3.client('s3')
bucket_name = 'taxidi-photo'
dynamodb = boto3.resource('dynamodb')
advertisements_table = dynamodb.Table('Advertisements')


owners = ['thanet.aus@gmail.com', 'josieanugerah@gmail.com',
          'kana_k123@outlook.com', 'zahra.ali@live.com']

filename = 'newcastle'
with open(filename + '.json') as json_file:
    data = json.load(json_file)


def hasNumber(s):
    return any(i.isdigit() for i in s)


success = []
for row in tqdm(data):
    # print(row)

    r = requests.get(row['url'])
    soup = BeautifulSoup(r.text, 'html.parser')
    description = soup.select("div#summary")[0].text.strip()
    location = soup.select(
        "span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip")[0].text.strip()
    # print(location)
    # continue
    locations = [loc.strip() for loc in location.split(',')]

    suburb = None
    street = None
    city = None
    postcode = None

    # if len(locations) == 3:
    #     if hasNumber(locations[-3]):
    #         continue
    #     postcode = locations[-2].split(' ')[0]
    #     city = locations[-2].split(' ')[1]
    #     suburb = locations[-3]
    if len(locations) > 3:
        postcode = locations[-2].split(' ')[0]
        city = locations[-2].split(' ')[1]
        suburb = locations[-3]
        street = locations[-4]
    else:
        continue

    image_urls = [img['href']
                  for img in soup.select("div.bh-photo-grid a")[1:-1]]
    photoURLs = []
    for image_url in image_urls:
        req_for_image = requests.get(image_url, stream=True)
        file_object_from_req = req_for_image.raw
        req_data = file_object_from_req.read()
        key = 'photos/' + str(uuid.uuid4()) + '.jpg'
        s3.put_object(Bucket='taxidi-photo', Key=key, Body=req_data,
                      ACL='public-read', ContentType='image/jpeg')
        photoURLs.append(key)

    params = {
        'ID': str(uuid.uuid4()),
        'owner': owners[random.randint(0, len(owners)-1)],
        'title': row['name'],
        'rent': random.randint(15, 40) * 5,
        'description': description,
        'active': True,
        'street': street,
        'aptNo': None,
        'suburb': suburb,
        'city': city,
        'postcode': postcode,
        'averageReview': random.randint(-1, 5),
        'availability': {
            '01-04-2020': True,
            '02-04-2020': True,
            '03-04-2020': True,
            '04-04-2020': True,
            '05-04-2020': True,
            '06-04-2020': True,
            '07-04-2020': True,
            '08-04-2020': True,
            '09-04-2020': True,
            '10-04-2020': True,
            '11-04-2020': True,
            '12-04-2020': True,
            '13-04-2020': True,
            '14-04-2020': True,
            '15-04-2020': True,
            '16-04-2020': True,
            '17-04-2020': True,
            '18-04-2020': True,
            '19-04-2020': True,
            '20-04-2020': True,
            '21-04-2020': True,
            '22-04-2020': True,
            '23-04-2020': True,
            '24-04-2020': True,
            '25-04-2020': True,
            '26-04-2020': True,
            '27-04-2020': True,
            '28-04-2020': True,
            '29-04-2020': True,
            '30-04-2020': True,
        },
        'photoURLs': photoURLs,
        '360PhotoURLs': []

    }
    try:
        response = advertisements_table.put_item(Item=params)
        success.append(params)
    except:
        print('error', params)


print('Success: ', len(success))

with open(filename+'_response.json', 'w') as outfile:
    json.dump(success, outfile)
