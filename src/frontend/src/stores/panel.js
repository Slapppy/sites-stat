import Vuex from 'vuex';


// TODO удалить лишнии файлы
const store = new Vuex.Store({
  state: {
    period: 'year' // default filter value
  },
  mutations: {
    setPeriod(state, period) {
      state.period = period;
    }
  }
});

export default store;
