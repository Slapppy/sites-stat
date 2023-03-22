const currentUrl = window.location.href;
const url = new URL(currentUrl);
const path = url.pathname.slice(1);
const id = path.split('/')[1];
// Get the ID of the counter from the URL

// Set the default filter to 'month'
let filter = 'month';

// Get the chart container element
const chartContainer = document.getElementById('chart-container');

const radioButton = document.querySelectorAll('[name="period"]');

radioButton.forEach(radio => radio.addEventListener('change', function () {
        filter = radio.value;
        updateChartData();
    }
))

// Update the chart data based on the selected filter
function updateChartData() {
    // Call the API to get the data for the selected filter
    $.ajax({
        url: `http://127.0.0.1:8000/api/view/data?id=${id}&filter=${filter}`,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // Extract the data for the chart
            const chartData = data.data.map(item => [Date.parse(item.date), <item className="count_views"></item>]);
            console.log(chartData)
            // Create a Highcharts chart
            Highcharts.chart(chartContainer, {
                chart: {
                    type: 'line'
                },
                title: {
                    text: 'Просмотры'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: 'Date'
                    },
                    crosshair: {
                        dashStyle: 'dot', // Style of the dot-line (solid, shortdash, shortdot, etc.)
                        width: 1, // Width of the dot-line
                        color: 'gray', // Color of the dot-line
                        zIndex: 5 // Z-index of the dot-line (to ensure it appears above other chart elements)
                    }
                },

                yAxis: {
                    title: {
                        text: 'Количество'

                    },
                },
                tooltip: {
                    // Tooltip options...
                    positioner: function (labelWidth, labelHeight, point) {
                        var tooltipX, tooltipY;
                        if (point.plotX + labelWidth > this.chart.plotWidth) {
                            tooltipX = point.plotX + this.chart.plotLeft - labelWidth - 10;
                        } else {
                            tooltipX = point.plotX + this.chart.plotLeft + 10;
                        }
                        tooltipY = point.plotY + this.chart.plotTop - labelHeight - 10;
                        return {
                            x: tooltipX,
                            y: tooltipY
                        };
                    }
                },
                series: [{
                    name: 'Views',
                    data: chartData
                }]
            });
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    });
}

// Initialize the chart with the default filter
updateChartData();
