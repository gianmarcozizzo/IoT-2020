import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import math

client = boto3.client('dynamodb');                                              # DynamoDB connection, change the table's name and the region for different uses
dynamoDB = boto3.resource('dynamodb', region_name='us-east-2')
dynamoTable = dynamoDB.Table('CSedge')
dynamoTableDest = dynamoDB.Table('CScloud')

def lambda_handler(event, context):                                             # function for simple activity analysis

    response = dynamoTable.query(                                               # for different uses you need to adapt the KeyConditionExpression and the dictionary keys
    KeyConditionExpression = Key('mode').eq('cloud')
    )
    items = response['Items']
    usefulData = {}
    usefulData = items

    for i in range(len(usefulData)):
            x = float(usefulData[i]['payload']['x'])
            y = float(usefulData[i]['payload']['y'])
            z = float(usefulData[i]['payload']['z'])
            result = (math.sqrt((x*x) + (y*y) + (z*z)))
            treshold = ((result - 9.81))
            # print(i, usefulData[i]['payload'], result, treshold)              # check line for Lambda's console
            if (treshold > 0):
                usefulData[i]['payload']['activity'] = 'moving'
            else:
                usefulData[i]['payload']['activity'] = 'stopped'

            dynamoTableDest.put_item(Item=usefulData[i])


    return {
        'statusCode': 200,
        'body': json.dumps('!')
    }
