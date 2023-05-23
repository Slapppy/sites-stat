<script setup>
import CounterPage from "../../containers/CounterPage.vue";
</script>


<template>
<CounterPage></CounterPage>
</template>



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
