import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createStore } from 'vuex'
import App from './App.vue'
import router from './router'
import panel from './stores/modules/panel.js'

const store = createStore({
  modules: {
    panel
  }
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(store)
app.mount('#app')
