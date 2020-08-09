#  This file from the AWS documentation (https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html) was modified to fit our needs.

#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
# 
#  http://aws.amazon.com/apache2.0/
# 
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')

tables = []

tables.append(dynamodb.create_table(
    TableName='Users',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
))

tables.append(dynamodb.create_table(
    TableName='Advertisements',
    KeySchema=[
        {
            'AttributeName': 'ID',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'ID',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
))

tables.append(dynamodb.create_table(
    TableName='Bookings',
    KeySchema=[
        {
            'AttributeName': 'ID',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'ID',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
))


tables.append(dynamodb.create_table(
    TableName='Reviews',
    KeySchema=[
        {
            'AttributeName': 'advertisementID',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'bookingID',
            'KeyType': 'RANGE' 
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'advertisementID',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'bookingID',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
))

for table in tables:
    print("Table status:", table.table_status)

