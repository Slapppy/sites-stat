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
    <div class="error-message" v-if="message">{{message}}</div>
    <div class="form__item_button">
      <button type="submit">Отправить</button>
    </div>
  </form>
</template>

<script>
import axios from 'axios';
import {getCookie} from '@/services'


const csrfToken = getCookie('csrftoken');

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.headers.common['X-CSRFToken'] = csrfToken;


export default {
  data() {
    return {
      name: '',
      link: '',
      message: ''
    }
  },
  methods: {
    submitForm() {
      const form = new FormData();
      form.append('name', this.name);
      form.append('link', this.link);
      this.addCounter();
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
        if (response.data.id) {
          this.message = '';
          window.location.href = `http://localhost:8000/counters/edit/${response.data.id}`;
        } else {
          this.message = 'Не получилось создать счетчик. Проверьте, что все поля заполнены, или поменяйте название счетчика'
        }
      } catch (error) {
        console.log(error.response);
      }
    }
  }
}
</script>

<style scoped>
</style>