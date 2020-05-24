## Crowd sensing application 

A simple Crowd Sensing application based on Amazon Web Services that determines the user activity through the smartphone's accelerometer. For a detailed explaination about the whole system give a look to my Hackster [guide](https://www.hackster.io/gianmarcozizzo/aws-based-crowd-sensing-application-d15f35).

- *index.html* and *cloud.html* compose the HTML5 web-app for getting and displaying the accelerometer's values
- *edge.js* and *cloud.js* are the respective scripts for analyzing and sendig the accelerometer's data to the cloud
- *server.js* is the local server that connects the parts
- In the *django_web* folder you can find all the files needed to run the web page that displays the values collected
- In the *lambda_function* folder you can find the Lambda function that I used on AWS for analyzing the data for the cloud-based mode

