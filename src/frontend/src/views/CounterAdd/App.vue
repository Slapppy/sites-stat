<template>
  <form @submit.prevent="submitForm" class="form">
    <div class="form__item">
      <label for="name">Имя счетчика:</label>
      <input type="text" id="name" v-model="name">
    </div>
    <div class="form__item">
      <label for="link">Адрес сайта:</label>
      <input type="text" id="link" v-model="link" placeholder="Введите домен или полный путь сайта">
    </div>
    <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
    <div class="success-message" v-if="successMessage">{{ successMessage }}</div>
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
      errorMessage: '',
      successMessage: '',
    }
  },
  methods: {
    isValidUrl() {
      const regex = /^(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(?:\/|$)/;
      return regex.test(this.link);
    },
    getDomain() {
      const regex = /^(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(?:\/|$)/;
      let match = this.link.match(regex);
      if (match && match.length > 1) {
        return match[1];
      } else {
        return null;
      }
    },
    submitForm() {
      this.errorMessage = '';
      this.successMessage = '';
      if (this.isValidUrl()) {
        const formData = new FormData();
        formData.append('name', this.name);
        formData.append('link', this.getDomain());
        this.addCounter(formData);
      } else {
        this.errorMessage = 'Неверный формат адреса сайта'
      }
    },
    async addCounter(formData) {
      try {
        const response = await axios.post(`${window.location.origin}/counters/add`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': csrfToken
          }
        });
        const counterId = response.data.id
        if (counterId) {
          this.successMessage = 'Счетчик создан. Сейчас вы будете перенаправлены на страницу настройки.';
          setTimeout(function () {
            window.location.href = window.location.href.replace('add', `edit/${counterId}`);
          }, 1000);
        } else {
          this.errorMessage = 'Не получилось создать счетчик. Проверьте, что все поля заполнены, ' +
              'или поменяйте название счетчика.'
        }
      } catch (error) {
        console.log(error);
      }
    }
  }
}
</script>

<style scoped>
</style>