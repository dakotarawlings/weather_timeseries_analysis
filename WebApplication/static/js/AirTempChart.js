
TEMP_FORECAST_API="http://127.0.0.1:5000/weatherForecast"

window.addEventListener('load', callTemperatureForecast);

//This function makes an http request to our flask api, sending the user input data and getting a price prediction
async function callTemperatureForecast() {


  //make an http request using fetch to pass in house features to flaskAPI, get prediction, and pass it into our html updating function
  const response=await fetch(TEMP_FORECAST_API, {
    method:"GET",
    headers: {
      "Content-type": "application/json"
    }
      })

      const data=await response.json()

      const dataObj = JSON.parse(data['data'])['ATMP'];

      const forecastObj = JSON.parse(data['forecast']);

      const xForecast=Object.keys(forecastObj);

      const yForecast=Object.values(forecastObj);

      for (let i = 0; i < xForecast.length; i++) {
        
        dateInt=parseInt(xForecast[i]);
        const dateObj=new Date(dateInt);
        xForecast[i]=dateObj.toLocaleDateString();
      }

      const xValues=Object.keys(dataObj);

      

      const yValues=Object.values(dataObj);

      for (let i = 0; i < xValues.length; i++) {
        
        dateInt=parseInt(xValues[i]);
        const dateObj=new Date(dateInt);
        xValues[i]=dateObj.toLocaleDateString();
      }
      
      xValues_xForecast=xValues.concat(xForecast);

  var ctx=document.getElementById('myChart1');

  new Chart(ctx, {

    data: {
      labels: xValues_xForecast,
      datasets: [{
        label:"Pat 10 days",
        fill: false,
        type: "line",
        pointBackgroundColor: '#3e95cd',
        pointBorderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgb(75, 192, 192)',
        backgroundColor:'rgb(75, 192, 192)',
        borderColor: 'rgb(75, 192, 192)',
        pointRadius: '6',
        borderWidth: '3',
        data: yValues
      },

      {
        label:"forecast",
        fill: false,
        type: "scatter",
        pointBackgroundColor: '#ff0000',
        pointBorderColor: 'rgb(75, 192, 192)',
        pointRadius: '6',
        borderWidth: '3',
        data: [{x:xForecast[0],y:[yForecast[0]]}, {x:xForecast[1],y:[yForecast[1]]}]

      },
    
    
    
    ],
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
          ticks: {min: 10, max: 20, fontSize: 15},
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






   }





