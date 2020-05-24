from django.shortcuts import render
from subprocess import run, PIPE
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from datetime import datetime, timedelta

last_hour_r = datetime.now() - timedelta(hours = 0)


client = boto3.client('dynamodb');
dynamoDB = boto3.resource('dynamodb', region_name='us-east-2')     # connection to DynamoDB and access
dynamoTableEdge = dynamoDB.Table('CSedge')                              # to the table EnvironmentalStation that will store the data provided
dynamoTableCloud = dynamoDB.Table('CScloud')


def home(request):

    # Last data for edge based mode
    response = dynamoTableEdge.query(
        KeyConditionExpression = Key('mode').eq('edge')
    )
    items = response['Items']

    context = {}
    context['mode'] = (items[len(items) - 1]["mode"])
    context['datetime'] = (items[len(items) - 1]["datetime"])
    context['activity'] = (items[len(items) - 1]["payload"]["activity"])

    # Last data for cloud based mode
    response = dynamoTableCloud.query(
        KeyConditionExpression = Key('mode').eq('cloud')
    )
    items = response['Items']

    context['modec'] = (items[len(items) - 1]["mode"])
    context['datetimec'] = (items[len(items) - 1]["datetime"])
    context['activityc'] = (items[len(items) - 1]["payload"]["activity"])
    context['xc'] = (items[len(items) - 1]["payload"]["x"])
    context['yc'] = (items[len(items) - 1]["payload"]["y"])
    context['zc'] = (items[len(items) - 1]["payload"]["z"])


    return render(request, 'blog/home.html', context)


def storage(request):

    # Data from edge mode
    response = dynamoTableEdge.query(
        KeyConditionExpression = Key('mode').eq('edge')
    )
    items = response['Items']

    context = {}
    context['items1'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem["datetime"] + " --- " + elem["mode"] + " --- " + elem["payload"]["activity"])

    context['items1'] = res

    # Data from cloud mode
    response = dynamoTableCloud.query(
        KeyConditionExpression = Key('mode').eq('cloud')
    )
    items = response['Items']

    context['items2'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem["datetime"] + " --- " + elem["mode"] + " --- " + elem["payload"]["activity"]  + " --- X: " +
            elem["payload"]["x"] + " --- Y: " + elem["payload"]["y"] + " --- Z: " + elem["payload"]["z"])

    context['items2'] = res





    return render(request, 'blog/storage.html', context)
