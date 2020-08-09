from algoliasearch.search_client import SearchClient
import sys

client = SearchClient.create('LDOJL787U6', '806ce69c538faebcd93876b815ef996c')
index = client.init_index('Advertisements')

def addAdvertisement(streamAd):
    ad = prepareAdForAlgolia(streamAd)
    return index.save_object(ad)

def prepareAdForAlgolia(streamAd):
    return{
        'objectID': streamAd['ID']['S'],
        'city': streamAd['city']['S'],
        'suburb': streamAd['suburb']['S'],
        'avgReview': float(streamAd['averageReview']['N']),
        'rent': int(streamAd['rent']['N'])
    }

def deleteAdvertisements(objectID):
    return index.delete_object(objectID)

def lambda_handler(event, context):
    print(event)
    try:
        for record in event['Records']:
            eventName = record['eventName']
            print(record)
            dynamodbData = record['dynamodb']
            if(eventName == "INSERT" or eventName == "MODIFY"):
                ad = dynamodbData['NewImage']
                addAdvertisement(ad)
            if(eventName == "REMOVE"):
                objectID = dynamodbData['Keys']['ID']['S']
                deleteAdvertisements(objectID)
    except:
        print(sys.exc_info()[0])
            
            
            
    return {}