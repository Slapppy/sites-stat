<template>
  <div class="page-charts">
    <!-- Include FilterPanel component and listen for filter-changed event -->
    <FilterPanel v-model="selectedFilter" @filter-changed="handleFilterChanged" />
    <div class="charts">
      <div class="view-chart" id="view-chart"></div>
      <div class="visit-chart" id="visit-chart"></div>
      <div class="visitor-chart" id="visitor-chart"></div>
    </div>
  </div>
</template>


<script>
import Highcharts from 'highcharts'
import $ from 'jquery'
import FilterPanel from "../containers/FilterPanel.vue";

export default {
  name: 'CounterPage',
  components:{FilterPanel},
  data() {
    return {
      apiResponseViews: null,
      apiResponseVisits: null,
      apiResponseVisitors: null,
      selectedFilter: 'week',
    }
  },
  mounted() {

    this.loadData()
  },
  methods: {
    loadData() {
      const currentUrl = window.location.href;
      const url = new URL(currentUrl);
      const path = url.pathname.slice(1);
      const id = path.split('/')[1];
      const ip = '127.0.0.1';

      $.ajax({
        url: `http://${ip}:8000/api/view/data?id=${id}&filter=${this.selectedFilter}`,
        method: 'GET',
        dataType: 'json',
        success: (response) => {
          this.apiResponseViews = response
          this.updateChartViews()
        },
        error: (xhr, status, error) => {
          console.log(error)
        }
      })
      $.ajax({
        url: `http://${ip}:8000/api/visit/data?id=${id}&filter=${this.selectedFilter}`,
        method: 'GET',
        dataType: 'json',
        success: (response) => {
          this.apiResponseVisits = response
          this.updateChartVisits()
        },
        error: (xhr, status, error) => {
          console.log(error)
        }
      })
      $.ajax({
        url: `http://${ip}:8000/api/visitor/data?id=${id}&filter=${this.selectedFilter}`,
        method: 'GET',
        dataType: 'json',
        success: (response) => {
          this.apiResponseVisitors = response
          this.updateChartVisitors()
        },
        error: (xhr, status, error) => {
          console.log(error)
        }
      })
    },
    updateChartViews() {
      const chartData = this.apiResponseViews.data.map(item => [Date.parse(item.date), item.count_views]);
      Highcharts.chart('view-chart', {
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
        plotOptions: {
          series: {
            softThreshold: true // включаем опцию softThreshold для более плавных изломов
          }
        },
        series: [{
          name: 'Просмотры',
          data: chartData
        }]
      });
    },
    updateChartVisits() {
      const chartData = this.apiResponseVisits.data.map(item => [Date.parse(item.date), item.count_visits]);
      Highcharts.chart('visit-chart', {
        chart: {
          type: 'line'
        },
        title: {
          text: 'Посещения'
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
        plotOptions: {
          series: {
            softThreshold: true // включаем опцию softThreshold для более плавных изломов
          }
        },
        series: [{
          name: 'Посещения',
          data: chartData
        }]
      });
    },
    updateChartVisitors() {
      const chartData = this.apiResponseVisitors.data.map(item => [Date.parse(item.date), item.count_visitors]);
      Highcharts.chart('visitor-chart', {
        chart: {
          type: 'line'
        },
        title: {
          text: 'Посетители'
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
        plotOptions: {
          series: {
            softThreshold: true // включаем опцию softThreshold для более плавных изломов
          }
        },
        series: [{
          name: 'Посетители',
          data: chartData
        }]
      });
    },


   handleFilterChanged(filter) {
    this.selectedFilter = filter;
    this.loadData();
    }
  },
}
</script>


<style scoped>

.filter-wrapper {
  margin-bottom: 20px;
  border-radius: 5px;
  position: relative;
  width: fit-content;
}

.radio-button {
  cursor: pointer;
}

.radio-button:first-child {
  margin-left: 0;
}

.input-radio-button {
  width: auto;
  height: 100%;
  appearance: none;
  outline: none;
}

.title-radio-button {
  border: 1px solid #B8B5B5;
  margin-left: -.13em;
  font-size: 14px;
  padding: 4px 14px 4px 14px;
  text-align: center;
}

.title-radio-button:hover {
  border: 1px solid #8a8787;
}

.input-radio-button:checked + .title-radio-button {
  background-color: #C9FF55;
}

.left-radio-button {
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
}

.right-radio-button {
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
}

.charts {
  display: flex;
  width: 100%;
}

.view-chart, .visit-chart, .visitor-chart {
  margin-right: 10px;
  width: 450px;
  height: 250px;
  border: 1px solid black;
}


</style>