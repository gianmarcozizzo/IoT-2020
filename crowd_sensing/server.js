var express = require('express');                                               // requirements
var fs = require('fs');
var https = require('https');

var app = express();

app.use(express.static('.'));
app.use(express.json());

https.createServer({                                                            // https server creation
  key: fs.readFileSync('YOUR_SERVER_KEY_PATH'),                                 // key (check the Hackster guide fort further information)
  cert: fs.readFileSync('YOUR_SERVER_CERTIFICATE_PATH')                         // certificate (check the Hackster guide fort further information)
}, app)
.listen(3000, '0.0.0.0', function () {
  console.log('Example app listening on port 3000! Go to https://localhost:3000/')
})


var awsIot = require('aws-iot-device-sdk');                                     // connection to AWS through the aws-sdk
var device = awsIot.device({
    keyPath: "YOUR_KEY_PATH",                                                   // insert here the folder's path of the needed elements
    certPath: "YOUR_CERTIFICATE_PATH",
      caPath: "YOUR_ROOTCA_PATH",
    clientId: "YOUR_CLIENT_ID",                                                 // client Id
        host: "YOUR_ENDPOINT"                                                   // your AWS endpoint
  });

device.on('connect', function() {                                               // device connection setup
    console.log('connection');
  });

app.post('/sendActivity', (request, response) => {                              // sending data to AWS
  console.log("Received a request");
  console.log(request.body);

  device.publish('sensors', JSON.stringify(request.body));                      // 'sensors' is the topic

  response.json({
    status: "success"
  });
