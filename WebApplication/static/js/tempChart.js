var xValues = [50,60,70,80,90,100,110,120];
var yValues = [7,8,8,9,9,9,10,11,14,14,15];



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
      text: 'Temperature',
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