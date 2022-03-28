
TEMP_FORECAST_API="/weatherForecast"

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
        label:"Past 10 days",
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
        label:"Forecast",
        fill: false,
        type: "scatter",
        pointBackgroundColor: 'rgb(230, 69, 69)',
        pointBorderColor: 'rgb(75, 192, 192)',
        pointRadius: '6',
        borderWidth: '3',
        data: [{x:xForecast[0],y:[yForecast[0]]}, {x:xForecast[1],y:[yForecast[1]]}]

      },
    
    
    
    ],
  },

    options: {
 
      legend: {
        display: true,
        labels: {
          fontStyle: "bold",
          usePointStyle: true,
          padding: 30
      }  
      },
      layout: {
        padding: {
          left: 20,
          right: 20,
        }
      },
      aspectRatio: 1.5,

      title: {
        display: false,
        // text: '   ',
        fontSize: 20,
      },
      

      scales: {
        
        yAxes: [{
          ticks: {min: 10, max: 20, fontSize: 15, fontStyle: "bold",},
          scaleLabel: {
            display: true,
            labelString: 'Temperature (C)',
            fontStyle: "bold",
            fontSize: 16,
          },

          gridLines: {
            color: "#3e95cd",
            lineWidth:2,
            borderDash: [2, 5], 
            display: true,
          }, 
          
        },

          {
            position: 'right',
            ticks: {
              display: false
            },
            gridLines: {
              display: false,
              color: "#3e95cd",
              lineWidth:2,
              drawOnChartArea: false,
              drawTicks: false
            }
          }
      
      
      ],
        xAxes: [{
          ticks: {fontSize: 15, },
          scaleLabel: {
            display: true,
            labelString: 'Day',
            fontStyle: "bold",
            fontSize: 16,
          },
          gridLines: {
            color: "#3e95cd",
            lineWidth:2,
            borderDash: [2, 5], 
            display: true

          },
              
        },
            
          {
            position: 'top',
            ticks: {
              display: false
            },
            gridLines: {
              display: false,
              color: "#3e95cd",
              lineWidth:2,
              drawOnChartArea: false,
              drawTicks: false
            }
          }
      ],
      },

    }
  
    
  });

   }

