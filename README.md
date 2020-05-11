# Internet of Things 19-20 
### Concept
This project is part of an assignment for the course of Internet of Things at the Sapienza University of Rome. The aim is to build a Virtual Environmental Station based on Amazon Web Services (AWS) that simulates some sensors (Temperature, Humidity, Rain Height, Wind Direction and Wind Intensity) generating random values in several ways and sending them to a database, AWS DynamoDB, with an MQTT broker. Then these data will be shown on a simple web application (running in localhost for this project).

## First Assignment
The environmental data are generated by a Python script.\
You can find the script at *virtual_stations/environmental_station_simulator.py*\
You can find the *manage.py* to run the localhost page at *django_web/manage.py*\

- Reference: http://ichatz.me/Site/InternetOfThings2020-Assignment1
- Hackster [guide](https://www.hackster.io/gianmarcozizzo/aws-based-iot-virtual-environmental-station-4ccb71)
- YouTube [video](https://www.youtube.com/watch?v=YGlRryTL12Y)
- LinkedIn [profile](https://www.linkedin.com/in/gianmarco-zizzo-9741861a3/)

## Second Assignment
The environmental data are generated by two RIOT devices and sent to AWS with an MQTT-SN\MQTT transparent bridge.\
You can find the RIOT file at *emcute_mqttsn/main.c*\
You can find the transparent bridge at *mqttsn_client/bridge.py*\
You can find the *manage.py* to run the localhost page at *django_web/manage.py*\
Attention: if you clone this repository you may have to do some paths adjustments. For further information give a look to the guide on Hackster

- Reference: http://ichatz.me/Site/InternetOfThings2020-Assignment2
- Hackster [guide](https://www.hackster.io/gianmarcozizzo/aws-based-iot-virtual-environmental-station-using-riot-os-1bd69d)
- YouTube [video](https://www.youtube.com/watch?v=HLiNK_PDmZs&feature=youtu.be)
- LinkedIn [profile](https://www.linkedin.com/in/gianmarco-zizzo-9741861a3/)

## Third Assignment
The environmental data are generated by two RIOT devices that stand on IoT-Lab real devices, sent to The Things Network through the LoRaWAN protocol and forwarded to AWS IoT Core and DynamoDB thourg a TTN/AWS bridge.\
You can find the RIOT file at *lorawan_station/main.c*\
You can find the bridge at *lorawan_station/TTNbridge.py*\
You can find the *manage.py* to run the localhost page at *django_web/manage.py*\
Attention: if you clone this repository you may have to do some paths adjustments. For further information give a look to the guide on Hackster

- Reference: http://ichatz.me/Site/InternetOfThings2020-Assignment3
- Hackster [guide](https://www.hackster.io/gianmarcozizzo/aws-based-iot-system-using-riot-os-lorawan-ttn-iot-lab-dae93b)
- YouTube [video](https://www.youtube.com/watch?v=CvmiBjnKEso)
- LinkedIn [profile](https://www.linkedin.com/in/gianmarco-zizzo-9741861a3/)


