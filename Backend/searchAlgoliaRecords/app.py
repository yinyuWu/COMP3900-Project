import json
from algoliasearch.search_client import SearchClient


client = SearchClient.create('LDOJL787U6', '806ce69c538faebcd93876b815ef996c')



def lambda_handler(event, context):
    print(event)
    if 'body' not in event:
        return {
            "statusCode": 500,
            "body": "No search body"
        }

    searchBody = json.loads(event['body'])

    city = searchBody['city']
    page = searchBody['page']
    sortType = searchBody['sortType']
    
    if(sortType == "Best rated"):
        indexToSort = "AdvertisementsRatingSort"
    elif(sortType == "Cheapest"):
        indexToSort = "AdvertisementsRentSort"
    else:
         indexToSort = "Advertisements"
    
    index = client.init_index(indexToSort)

    print(page)
    searchResults = index.search(city, {'page':page})
    #nHits = searchResults['nbHits']
    #nHits = searchResults['hitsPerPage']
    nHits = len(searchResults['hits'])

    objectIDs = []
    print(nHits)
    print(searchResults)
    for n in range (0, nHits):
        objectIDs.append(searchResults['hits'][n]['objectID'])

    print(objectIDs)

    output = {'objectIDs':objectIDs, 'nbPages':searchResults['nbPages']} 
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps(output)
    }