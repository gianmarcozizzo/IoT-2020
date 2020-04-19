# This script is basend on "environmental_station_simulator.py" in virtual_stations folder
# Basically most of the functions and variables are the same
# Don't use Python3 because you might haave some troubles with default Mosquitto's scripts

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import MQTTSNclient
import boto3
import json
import sys
import parser
import argparse
import logging
from  MQTTSNclient import Client

myClient = AWSIoTMQTTClient("MQTTSNbridge")                                     # client to AWS
MQTTSNClient = MQTTSNclient.Client("bridge", port=1885)                         # bridge

dynamodb = boto3.resource('dynamodb', region_name='YOUR_REGION')                # connection to DynamoDB and access
dynamoTable = dynamodb.Table('YOUR_TABLE_NAME')                                 # to the table EnvironmentalStation that will store the data provided
json_payload = '';

def send_data(myClient, data, topic):                                           # the function publishes the recieved data
    messageJson = json.dumps(data)
    myClient.publish(topic, messageJson, 1)
    print("########## DATA RECIEVED ##########")
    print("Published on topic: %s\nData provided by: %s\nRecieved data:\n%s\n" % (topic, clientId, messageJson))
    print("I'm sending the data to DynamoDB... \n \n")


def awsconnection(useWebsocket = False,                                         # the function sets the connection to AWS
    clientId = "",                                                              # client id
    thingName = "YOUR_THING_NAME",                                              # thing name (on AWS)
    host = "YOUR_ENDPOINT",                                                     # your AWS endpoint
    caPath = "YOUR_PATH/rootCa.pem",                                            # rootCA certificate (folder's path)
    certPath = "YOUR_PATH/XXXXXXXXXX-certificate.pem.crt",                      # client certificate (folder's path)
    keyPath = "YOUR_PATH/XXXXXXXXXX-private.pem.key"                            # private key (folder's path)
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
    myClient.configureOfflinePublishQueueing(-1)      # param: if set to 0, the queue is disabled. If set to -1, the queue size is set to be infinite.
    myClient.configureDrainingFrequency(2)            # Draining: 2 Hz
    myClient.configureConnectDisconnectTimeout(10)    # 10 sec
    myClient.configureMQTTOperationTimeout(5)         # 5 sec

    return myClient

# Not necessary this time
# Arguments passing: in this case the only argument that we need is the clientId, that is supposed to be station1 or station2
# parser = argparse.ArgumentParser()
# parser.add_argument('--clientid', type=str)
# args = parser.parse_args()
# clientId = args.clientid
topic = "environmental_station"

class myCallback:                                                               # useful guide at http://www.steves-internet-guide.com/python-mqttsn-client/
    def messageArrived(self, topicName, payload, qos, retained, msgid):         # don't change the arguments to have no problems with default files of Mosquitto
        json_payload = json.loads(payload)
        print(topic, payload)                                                   # just for a checking
        myClient.publish(topic, payload, qos)                                   # publish the payload on the topic
        dynamoTable.put_item(Item=json_payload)                                 # store the payload in DynamoDB
        return True


myClient =  awsconnection()                                                     # setting connection, callback, subscription
myClient.connect()
MQTTSNClient.registerCallback(myCallback())
MQTTSNClient.connect()
MQTTSNClient.subscribe(topic)

print("Ctrl+C to kill");

while True:                                                                     # endless party until ctrl+c
    if False:
        break

MQTTSNClient.disconnect()                                                       # disconnection
myClient.disconnect()
