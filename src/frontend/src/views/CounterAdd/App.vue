<template>
  <form @submit.prevent="submitForm" class="form">
    <div class="form__item">
      <label for="name">Имя счетчика:</label>
      <input type="text" id="name" v-model="name">
    </div>
    <div class="form__item">
      <label for="link">Адрес сайта:</label>
      <input type="text" id="link" v-model="link">
    </div>
    <div class="form__item_button">
      <button type="submit">Отправить</button>
    </div>
  </form>
  <div id="counter_script" v-if="showScript">
        <pre>
            <code class="language-html" ref="counterScript">
              {{ script }}
            </code>
        </pre>
    <div class="form__item_button">
      <button @click="copyToClipboard">Скопировать</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {generateCounterScript} from '@/services';
import {getCookie} from '@/services'


const csrfToken = getCookie('csrftoken');

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.headers.common['X-CSRFToken'] = csrfToken;


export default {
  data() {
    return {
      showScript: false,
      script: '',
      name: '',
      link: ''
    }
  },
  methods: {
    copyToClipboard() {
      // TODO зачем ходить напрямую в DOM? Вы же работаете во Vue и должны использовать инструменты Vue
      // Не надо в обход менять DOM
      const el = document.createElement('textarea');
      el.value = document.querySelector('#counter_script code').textContent;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      alert('Скрипт скопирован!');
    },

    submitForm() {
      const form = new FormData();
      form.append('name', this.name);
      form.append('link', this.link);
      this.addCounter();
    },
    updateScript(counter_id) {
      this.script = generateCounterScript(counter_id);
      this.showScript = true;
    },
    async addCounter() {
      try {
        const response = await axios.post(`${window.location.origin}/counters/add`, {
          name: this.name,
          link: this.link
        }, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': csrfToken
          }
        });
        await this.updateScript(response.data.id);
      } catch (error) {
        console.log(error.response);
      }
    }
  }
}
</script>

<style scoped>
</style>