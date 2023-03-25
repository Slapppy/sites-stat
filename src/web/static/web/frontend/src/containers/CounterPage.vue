<template>
  <div class="filter-wrapper">
      <div class="filter-panel">
        <button id="btn3Days" class="filter-btn" :class="{ active: filter === 'threedays' }" @click="handleFilterClick('threedays')">3 дня</button>
        <button id="btnWeek" class="filter-btn" :class="{ active: filter === 'week' }" @click="handleFilterClick('week')">Неделя</button>
        <button id="btnMonth" class="filter-btn" :class="{ active: filter === 'month' }" @click="handleFilterClick('month')">Месяц</button>
        <button id="btnQuarter" class="filter-btn" :class="{ active: filter === 'quarter' }" @click="handleFilterClick('quarter')">Квартал</button>
        <button id="btnYear" class="filter-btn" :class="{ active: filter === 'year' }" @click="handleFilterClick('year')">Год</button>
      </div>
</div>

  <div class="chart-container" id="chart-container"></div>
  <div class="visit-chart" id="visit-chart"></div>
  <div class="visitor-chart" id="visitor-chart"></div>

</template>
<script>
import Highcharts from 'highcharts'
import $ from 'jquery'

export default {
  name: 'CounterPage',
  data() {
    return {
      apiResponse1: null,
      apiResponse2: null,
      apiResponse3: null,
      filter: 'month', // добавляем параметр фильтрации по умолчанию
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
        url: `http://${ip}:8000/api/view/data?id=${id}&filter=${this.filter}`,
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
        url: `http://${ip}:8000/api/visit/data?id=${id}&filter=${this.filter}`,
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
        url: `http://${ip}:8000/api/visitor/data?id=${id}&filter=${this.filter}`,
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
      Highcharts.chart('chart-container', {
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
          name: 'Посещения',
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
          name: 'Посещения',
          data: chartData
        }]
      });
    },


    handleFilterClick(filter) {
      this.filter = filter;
      console.log(filter)
      this.loadData();
    },

    },
        }
  </script>


<style scoped>

.filter-wrapper {
  margin-bottom: 20px;
  border-radius: 5px;
  padding-left: 50px;
  position: relative;
  width: fit-content;
}
.filter-wrapper::before{
  content: "";
  position: absolute;
  bottom: -20px;
  width: 354%;
  left: -10px;
  height: 2px;
  background: black;
}

.filter-panel {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 5px;
  border: none;
}

.filter-btn {
  border: 2px solid #4dcc40;
  background-color: transparent;
  color: #555;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  padding: 5px 10px;
  text-transform: uppercase;
  text-align: center;
  margin-left: -2px;
}

.filter-btn.active {
  color: #4dcc40;
  border-bottom: 2px solid #4dcc40;

}

.filter-btn:first-child {
  border-right: none;
  margin-left: 0;
}

.filter-btn:last-child {
  border-left: none;
  margin-right: 0;
}

.chart-container{
    margin-top:70px;
    width: 450px;
    height: 250px;
      border: 1px solid black;
      margin-left: 20px;

  }

.visit-chart{
    margin-top:-250px;
    width: 450px;
    height: 250px;
    border: 1px solid black;
    margin-left: 493px;

  }

.visitor-chart{
    margin-top:-250px;
    width: 450px;
    height: 250px;
      border: 1px solid black;
      margin-left: 966px;

  }


</style>