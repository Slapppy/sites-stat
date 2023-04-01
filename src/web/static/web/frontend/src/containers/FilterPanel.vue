<template>
  <div class="page-charts">
    <div class="filter-wrapper">
      <div class="date-selector mb-3">
        <span class="date-radio-buttons">
            <label class="radio-button">
                <input class="input-radio-button" type="radio" name="period" value="threedays"
                       v-model="selectedFilter" @change="onFilterChange">
                <span class="title-radio-button left-radio-button">3 дня</span>
            </label>
            <label class="radio-button">
                <input class="input-radio-button" type="radio" name="period" value="week"
                        v-model="selectedFilter" @change="onFilterChange">
                <span class="title-radio-button">Неделя</span>
            </label>
            <label class="radio-button">
                <input class="input-radio-button" type="radio" name="period" value="month"
                       v-model="selectedFilter" @change="onFilterChange">
                <span class="title-radio-button">Месяц</span>
            </label>
            <label class="radio-button">
                <input class="input-radio-button" type="radio" name="period" value="quarter"
                       v-model="selectedFilter" @change="onFilterChange">
                <span class="title-radio-button">Квартал</span>
            </label>
            <label class="radio-button">
                <input class="input-radio-button" type="radio" name="period" value="year"
                       v-model="selectedFilter" @change="onFilterChange">
                <span class="title-radio-button  right-radio-button">Год</span>
            </label>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    filter: {
      type: String,
      default: 'month'
    }
  },
  data() {
    return {
      periods: [
        { value: 'threedays', label: '3 дня' },
        { value: 'week', label: 'Неделя' },
        { value: 'month', label: 'Месяц' },
        { value: 'quarter', label: 'Квартал' },
        { value: 'year', label: 'Год' }
      ],
      selectedFilter: this.filter
    }
  },
  computed: {
  syncedFilter: {
    get() {
      return this.selectedFilter;
    },
    set(value) {
      this.selectedFilter = value;
    },
  },
},
  watch: {
    filter(newVal) {
      this.selectedFilter = newVal;
    }
  },
  methods: {
    onFilterChange() {
      this.$emit('filter-changed', this.selectedFilter);
    }
  }
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



</style>