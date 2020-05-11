# This script is based on "environmental_station_simulator.py" in virtual_stations folder
# Basically most of the functions and variables are the same

import paho.mqtt.client as mqtt
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
import json
import sys
import parser
import argparse
import logging
import datetime
import time
import base64

myClient = AWSIoTMQTTClient("TTNbridge")                                        # client to AWS
TTNClient = mqtt.Client()                                                       # bridge

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')                  # connection to DynamoDB and access
dynamoTable = dynamodb.Table('YOUR_TABLE_NAME')                                 # to the table EnvironmentalStation that will store the data provided

def awsconnection(useWebsocket = False,                                         # the function sets the connection to AWS
    clientId = "",                                                              # client id
    thingName = "YOUR_THING_NAME",                                              # thing name (on AWS)
    host = "YOUR_ENDPOINT",                                                     # your AWS endpoint
    caPath = "YOUR_ROOT_CA",                                                    # rootCA certificate (folder's path)
    certPath = "YOUR_CERTIFICATE",                                              # client certificate (folder's path)
    keyPath = "YOUR_KEY"                                                        # private key (folder's path)
    ):

    port = 8883 if not useWebsocket else 443
    useWebsocket = useWebsocket
    # clientId = clientId
    host = host
    port = port
    rootCaPath = caPath
    privateKeyPath = keyPath
    certificatePath = certPath

    # Logger settings
    # more information at https://docs.python.org/3/library/logging.html
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.NOTSET)                                                      # NOTSET causes all messages to be processed when the logger is the root logger
    streamHandler = logging.StreamHandler()                                              # sends logging output to streams
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    # AWSIoTMQTTClient initialization
    myClient = None
    if useWebsocket:
        myClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
        myClient.configureEndpoint(host, port)
        myClient.configureCredentials(rootCaPath)
    else:
        myClient = AWSIoTMQTTClient(clientId)
        myClient.configureEndpoint(host, port)
        myClient.configureCredentials(rootCaPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    myClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myClient.configureOfflinePublishQueueing(-1)                                # param: if set to 0, the queue is disabled. If set to -1, the queue size is set to be infinite.
    myClient.configureDrainingFrequency(2)                                      # Draining: 2 Hz
    myClient.configureConnectDisconnectTimeout(10)                              # 10 sec
    myClient.configureMQTTOperationTimeout(5)                                   # 5 sec

    return myClient

myClient = awsconnection()                                                      # initializing the connection to AWS

def on_connect(client, userdata, flags, rc):                                    # on_connect for the TTN Client
    print("Connected with result code "+str(rc))
    # subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed
    client.subscribe("+/devices/+/up")

# the callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):                                          # on_message for the TTN Client
    payload = json.loads(msg.payload)
    decoded_payload = base64.b64decode(payload['payload_raw'])                  # decoding needed tuo get only the payload (try without it if you want...)
    final_payload = json.loads(str(decoded_payload)[2:-1])                      # better visualization of the payload
    final_payload['datetime'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print(final_payload,"\n")
    myClient.connect()
    myClient.publish("YOUR_TOPIC", json.dumps(new_msg), 0)                      # publish the payload on the topic
    dynamoTable.put_item(Item=new_msg)                                          # store the payload in DynamoDB
    myClient.disconnect()

TTNClient = mqtt.Client()                                                       # setting the TTN client
TTNClient.on_connect = on_connect
TTNClient.on_message = on_message

TTNClient.username_pw_set("YOUR_APP", "YOUR_ACCESS_KEY")                        # set your parameters (the name of you application on TTN, your access key)

TTNClient.connect("eu.thethings.network", 1883, 60)                             # connection
print("Check connessione")

TTNClient.loop_start()                                                          # loop starts

while True:                                                                     # endless party until ctrl+c
    if False:
        break
    time.sleep(5)

TTNClient.loop_stop()                                                           # disconnection
TTNClient.disconnect()
