# About
For a detailed explaination about how to run the whole system, it is strongly suggested to give a look to the Hackster [guide](https://www.hackster.io/gianmarcozizzo/aws-based-iot-system-using-riot-os-lorawan-ttn-iot-lab-dae93b).\
Otherwise, you can find the official and more general guide [here](https://www.iot-lab.info/tutorials/riot-ttn/)

## main.c
The main.c file contains a modified version of the test code provided by [RIOT](https://github.com/RIOT-OS/RIOT). It simulates a virtual environmental station that stands on IoT-Lab real device. The file needs to be in the folder RIOT/tests/pkg_semtech-loramac on your machine, while your are connected with the Saclay host site, as explained in the linked guides

## TTNbridge.py
The TTNbridge.py file is a Python script that acts like a bridge between The Things Network and AWS IoT Core
