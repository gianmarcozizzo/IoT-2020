from django.shortcuts import render
from subprocess import run, PIPE
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from datetime import datetime, timedelta

last_hour_r = datetime.now() - timedelta(hours = 0)

# Change the region name and the table name
client = boto3.client('dynamodb');
dynamoDB = boto3.resource('dynamodb', region_name='us-east-2')     # connection to DynamoDB and access
dynamoTable = dynamoDB.Table('EnvironmentalStation')               # to the table EnvironmentalStation that will store the data provided



def home(request):

    # Last data from station1
    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station1')
    )
    items = response['Items']

    context = {}
    context['ID'] = (items[len(items) - 1]["ID"])
    context['Temperature'] = (items[len(items) - 1]["Temperature"])
    context['datetime'] = (items[len(items) - 1]["datetime"])
    context['WindIntensity'] = (items[len(items) - 1]["WindIntensity"])
    context['WindDirection'] = (items[len(items) - 1]["WindDirection"])
    context['Humidity'] = (items[len(items) - 1]["Humidity"])
    context['RainHeight'] = (items[len(items) - 1]["RainHeight"])

    # Last data from station2
    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station2')
    )
    items = response['Items']

    context['ID2'] = (items[len(items) - 1]["ID"])
    context['Temperature2'] = (items[len(items) - 1]["Temperature"])
    context['datetime2'] = (items[len(items) - 1]["datetime"])
    context['WindIntensity2'] = (items[len(items) - 1]["WindIntensity"])
    context['WindDirection2'] = (items[len(items) - 1]["WindDirection"])
    context['Humidity2'] = (items[len(items) - 1]["Humidity"])
    context['RainHeight2'] = (items[len(items) - 1]["RainHeight"])


    return render(request, 'blog/home.html', context)



def storage(request):

    # Last hour data from station1
    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station1')
    )
    items = response['Items']

    context = {}
    context['items1'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['items1'] = res


    # Last hour ata from station2
    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station2')
    )
    items = response['Items']

    context['items2'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['items2'] = res


    # The rest of the code is for the last hour data of each sensor (maybe not in the best way...)

    # Temperature (last hour data from all stations)
    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station2')
    )
    items = response['Items']
    context['temp'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['temp'] = res

    resTemp = []
    for i in reversed(range(len(res))):
        resTemp.append(res[i]["datetime"] + " | " + res[i]["ID"] + " | " + res[i]["Temperature"] + " C°")

    context['temp'] = resTemp

    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station1')
    )
    items = response['Items']
    context['temp'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['temp'] = res


    for i in reversed(range(len(res))):
        resTemp.append(res[i]["datetime"] + " | " + res[i]["ID"] + " | " + res[i]["Temperature"] + " C°")

    context['temp'] = reversed(resTemp)

    # Rain Height (last hour data from all stations)
    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station2')
    )
    items = response['Items']
    context['rain'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['rain'] = res

    resRain = []
    for i in reversed(range(len(res))):
        resRain.append(res[i]["datetime"] + " | " + res[i]["ID"] + " | " + res[i]["RainHeight"] + " mm/h")

    context['rain'] = resTemp

    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station1')
    )
    items = response['Items']
    context['rain'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['rain'] = res


    for i in reversed(range(len(res))):
        resRain.append(res[i]["datetime"] + " | " + res[i]["ID"] + " | " + res[i]["RainHeight"] + " m/s")

    context['rain'] = reversed(resRain)

    # Wind Intensity (last hour data from all stations)
    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station2')
    )
    items = response['Items']
    context['windintensity'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['windintensity'] = res

    resWin = []
    for i in reversed(range(len(res))):
        resWin.append(res[i]["datetime"] + " | " + res[i]["ID"] + " | " + res[i]["WindIntensity"] + " m/s")

    context['windintensity'] = resWin

    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station1')
    )
    items = response['Items']
    context['windintensity'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['windintensity'] = res


    for i in reversed(range(len(res))):
        resWin.append(res[i]["datetime"] + " | " + res[i]["ID"] + " | " + res[i]["WindIntensity"] + " mm/h")

    context['windintensity'] = reversed(resWin)

    # Humidity (last hour data from all stations)
    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station2')
    )
    items = response['Items']
    context['humidity'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['humidity'] = res

    resHum = []
    for i in reversed(range(len(res))):
        resHum.append(res[i]["datetime"] + " | " + res[i]["ID"] + " | " + res[i]["Humidity"] + " %")

    context['humidity'] = resHum

    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station1')
    )
    items = response['Items']
    context['humidity'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['humidity'] = res


    for i in reversed(range(len(res))):
        resHum.append(res[i]["datetime"] + " | " + res[i]["ID"] + " | " + res[i]["Humidity"] + " %")

    context['humidity'] = reversed(resHum)

    # Wind Direction (last hour data from all stations)
    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station2')
    )
    items = response['Items']
    context['windirection'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['windirection'] = res

    resWdir = []
    for i in reversed(range(len(res))):
        resWdir.append(res[i]["datetime"] + " | " + res[i]["ID"] + " | " + res[i]["WindDirection"] + " °")

    context['windirection'] = resWdir

    response = dynamoTable.query(
        KeyConditionExpression = Key('ID').eq('station1')
    )
    items = response['Items']
    context['windirection'] = reversed(items)

    res = []

    for elem in reversed(items):
        strhour = elem["datetime"]
        hour = datetime.strptime(strhour, '%Y-%m-%d %H:%M:%S')
        if hour >= last_hour_r:
            res.append(elem)

    context['windirection'] = res


    for i in reversed(range(len(res))):
        resWdir.append(res[i]["datetime"] + " | " + res[i]["ID"] + " | " + res[i]["WindDirection"] + " °")

    context['windirection'] = reversed(resWdir)


    return render(request, 'blog/storage.html', context)
