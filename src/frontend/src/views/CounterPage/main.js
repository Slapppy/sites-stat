import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createStore } from 'vuex'
import App from '../CounterPage/App.vue'
import router from '../../../router/index.js'
import panel from '../../stores/panel.js'

const store = createStore({
  modules: {
    panel
  },
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(store)
app.mount("#counterpage")

