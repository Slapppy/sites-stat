<template>
    <form @submit.prevent="submitForm" class="form">
        <div class="form__item">
            <label for="name">Имя счетчика:</label>
            <input type="text" id="name" v-model="name">
        </div>
        <div class="form__item">
            <label for="link">Ссылка:</label>
            <input type="text" id="link" v-model="link">
        </div>
        <div class="form__item_button">
            <button type="submit">Отправить</button>
        </div>
    </form>
</template>
<script>
import axios from 'axios';

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const csrfToken = getCookie('csrftoken');

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.headers.common['X-CSRFToken'] = csrfToken;



export default {
  data() {
    return {

      name: '',
      link: ''
    }
  },
  methods: {
    submitForm() {
        const form = new FormData();

         form.append('name', this.name);
        form.append('link', this.link);

      axios.post('http://127.0.0.1:8000/counters/add', {
        name:this.name,
          link:this.link

      },

{
  headers: {
    'Content-Type': 'multipart/form-data',
    'X-CSRFToken': csrfToken
  }
}




  )
      .then(response => {
        console.log(response.data);
        console.log(this.name);

      })
      .catch(error => {
        console.log(error.response.data);
      });
    }
  }
}
</script>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600&display=swap');

    body {
        font-family: 'Montserrat', sans-serif;
    }

    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
        max-width: 500px;
        font-weight: 500;
    }

    .form__item {
        display: flex;
        gap: 20px;
        justify-content: space-between;
    }

    .form__item input {
        font-size: 1rem;
        width: 60%;
        padding: 2px 0px 2px 2px;
        border-radius: 4px;
        border-color: #c5c5c5;
    }

    .form__item_button button {
        padding: 12px 36px;
        font-size: 14px;
        border-radius: 4px;
        -webkit-box-shadow: 3px 3px 10px 3px #dddddd;
        -moz-box-shadow: 3px 3px 10px 3px #dddddd;
        box-shadow: 3px 3px 10px 3px #dddddd;
        border: 1px solid rgba(204, 204, 204, 0.5);
        background-color: #A7F736FF;
        color: black;
        cursor: pointer;
        font-weight: 500;
    }

    .form__item_button {
        width: 100%;
        display: flex;
        justify-content: flex-end;
    }
</style>