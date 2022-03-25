var xValues = [50,60,70,80,90,100,110,120];
var yValues = [7,8,8,9,9,9,10,11,14,14,15];

TEMP_FORECAST_API="http://127.0.0.1:5000/temperatureForecast"

window.addEventListener('load', callTemperatureForecast);

//This function makes an http request to our flask api, sending the user input data and getting a price prediction
function callTemperatureForecast() {


  //make an http request using fetch to pass in house features to flaskAPI, get prediction, and pass it into our html updating function
  fetch(TEMP_FORECAST_API, {
    method:"GET",
    headers: {
      "Content-type": "application/json"
    }
      }).then(response => response.json()
      .then(function(data) {

          const dataObj = JSON.parse(data['data'])['ATMP'];

          console.log(Object.keys(dataObj));
          console.log(Object.values(dataObj));

          xValues=Object.values(dataObj)
          yValues=Object.values(dataObj)

          const forecastObj = JSON.parse(data['forecast']);

          console.log(Object.keys(forecastObj));

          

           }))
          

 
  }


  var ctx=document.getElementById('myChart2');

  new Chart(ctx, {
    type: "line",
    data: {
      labels: xValues,
      datasets: [{
        fill: false,
  
        pointBackgroundColor: '#3e95cd',
        pointBorderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgb(75, 192, 192)',
        backgroundColor:'rgb(75, 192, 192)',
        borderColor: 'rgb(75, 192, 192)',
        pointRadius: '6',
        borderWidth: '3',
        data: yValues
      }]
    },
    
    options: {

      legend: {display: false},
      aspectRatio: 1.5,

      title: {
        display: true,
        text: '   ',
        fontSize: 20,
      },
      

      scales: {
        
        yAxes: [{
          ticks: {min: 6, max:16, fontSize: 15},
          scaleLabel: {
            display: true,
            labelString: 'Temperature (C)',
            fontSize: 15,
          },

          gridLines: {
            color: "#3e95cd",
            lineWidth:2,
            borderDash: [2, 5], 
          }, 
          
        }],
        xAxes: [{
          ticks: {fontSize: 15},
          scaleLabel: {
            display: true,
            labelString: 'Day',
            fontSize: 15,
          },
          gridLines: {
            color: "#3e95cd",
            lineWidth:2,
            borderDash: [2, 5], 

          },    
        }],
      },

    }
  });

  