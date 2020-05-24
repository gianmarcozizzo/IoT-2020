let xval = document.getElementById('x_value');                                  // passing the HTML page elements
let yval = document.getElementById('y_value');
let zval = document.getElementById('z_value');
let derr = document.getElementById('div-error');
let dact = document.getElementById('dacti');
let stco = document.getElementById('status-container');
let result = 0;                                                                 // var initializations
let treshold = 0;

let acc = new Accelerometer({ frequency : 1 });                                 // starting the accelerometer

let vals = {                                                                    // utility
  'x' : xval.innerHTML,
  'y' : yval.innerHTML,
  'z' : zval.innerHTML
};

$(document).ready(() => {                                                       // script starting
  try {
    if (window.Accelerometer) {
      this.getAccelerometerValues();
    } else {
      derr.innerHTML = 'Accelerometer not available';
    }
  } catch (error) {
    derr.innerHTML = error;
  }
});

function getAccelerometerValues() {                                             // function that gets the accelerometer's values and displays them
  acc.onreading = () => {
    xval.innerHTML = acc.x.toFixed(3);
    yval.innerHTML = acc.y.toFixed(3);
    zval.innerHTML = acc.z.toFixed(3);
    this.displayResult();
  }
  acc.start();
}

function movementDetection() {                                                  // utility for activity recognition model
  vals.x = acc.x.toFixed(3);
  vals.y = acc.y.toFixed(3);
  vals.z = acc.z.toFixed(3);
  return Math.sqrt( (vals.x * vals.x) + (vals.y * vals.y) + (vals.z * vals.z) );
}

async function displayResult(){

  var today = new Date();
  var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
  var hurs = ('0'+today.getHours()).slice(-2);
  var mins = ('0'+today.getMinutes()).slice(-2);                                // it's awful that I have to do this for having a 2 digits time...
  var secs = ('0'+today.getSeconds()).slice(-2);
  var time = hurs + ":" + mins + ":" + secs;
  var dateTime = date+' '+time;                                                 // current datetime

  result = movementDetection();                                                 // simple activity recognition model
  var activity = '';
  treshold = Math.abs(result - 9.81);
  if (treshold > 0.15) {                                                        // displaying the results in the HTML app
    stco.style.background = 'springgreen';
    dact.innerHTML = "<b> Current status: </b>" + "moving" + "<br/>" + "<b> Computed value: </b>" + treshold.toFixed(3) + "<br/>" + "<b> Time: </b>" + dateTime;
    activity = 'moving';
  } else {
    stco.style.background = 'tomato';
    dact.innerHTML = "<b> Current status: </b>" + "stopped" + "<br/>" + "<b> Computed value: </b>" + treshold.toFixed(3) + "<br/>" + "<b> Time: </b>" + dateTime;
    activity = 'stopped';
    }

    var activity_recognition = {                                                // data structuring for the cloud and the database
        "mode" : "edge",
        "datetime" : dateTime,
        "activity" : activity
    }

    const options = {                                                           // data structuring for the server
        method : 'POST',
        headers : {
            "Content-Type": "application/json"
        },
        body : JSON.stringify(activity_recognition)
    };

    const response = await fetch('/sendActivity', options);                     // sending data to the server
    const res = await response.json();
    console.log(res);

}
