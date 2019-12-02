
function float2dollar(value){
    return (value).toFixed(4).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

function getaverage(dir)
{
	return [1292.619995,1287.880005,1286.77002,1277.719971,1290.079956,1285.22998,1280.589966,1290.079956,1289.969971,1276.060059,1276.609985,1297.920044,1287.880005,1282.02002,1280.589966,1283.130005,1279.040039,1275.839966,1277.5,1286.109985,1281.030029,1284.01001,1299.359985,1289.530029,1291.849976,1280.369995,1271.530029,1269.660034,1268.550049];
}
function getopen(dir)
{
	return [30,20,100];
}
function gethigh(dir)
{
	return [30,20,100];
}
function getlow(dir)
{
	return [30,20,100];
}
function getclose(dir)
{
	return [30,20,100];
}
function getlabel(dir)
{
	return ["1/29/1985","1/30/1985","1/31/1985","2/1/1985","2/4/1985","2/5/1985","2/6/1985","2/7/1985","2/8/1985","2/11/1985","2/12/1985","2/13/1985","2/14/1985","2/15/1985","2/19/1985","2/20/1985","2/21/1985","2/22/1985","2/25/1985","2/26/1985","2/27/1985","2/28/1985","3/1/1985","3/4/1985","3/5/1985","3/6/1985","3/7/1985","3/8/1985","3/11/1985"];
}

function renderChart(data, labels, chartname) {
	var bgcolor = [];
    var ctx = document.getElementById(chartname).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
				label: '',
                data: data,
                pointborderColor: bgcolor,
				pointBackgroundColor: bgcolor,
				borderColor: bgcolor,
                backgroundColor: 'rgba(25, 198, 225, 0.1)'
            }, {label: '50 Days stock price',backgroundColor: '#000080'}, 
			{label: 'Prediction Value', backgroundColor: '#FF0000'}]
        },
        options: { 
			legend: {
				labels: {
					filter: function(legendItem, chartData) {
						if (legendItem.datasetIndex === 0) {
							return false;
						}
							return true;
						}
					}
				},
			responsive: true,		
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function(value, index, values) {
                            return float2dollar(value);
                        }
                    }
                }]                
            }			
        },
    });
	
	for (i = 0; i < myChart.data.datasets[0].data.length; i++) {
		if (i > 5) 
		{
			bgcolor.push('#FF0000');
		} 
		else 
		{
			bgcolor.push('#000080');
		}
	}
	myChart.update();
}

$(document).ready(
    function () {
        average = getaverage();
		opening = getopen();
		highest = gethigh();
		lowest = getlow();
		closing = getclose();
        labels =  getlabel();
        renderChart(average, labels, "average");
		renderChart(opening, labels, "open");
		renderChart(highest, labels, "high");
		renderChart(lowest, labels, "low");
		renderChart(closing, labels, "close");
    }
);