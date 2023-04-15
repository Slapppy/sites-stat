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
    <div id="counter_script" v-if="showF">
        <pre>
            <code class="language-html">
                &lt;!-- /Auf.Metrika counter --&gt;
                &lt;script&gt;&lt;img src="https://127.0.0.1/api/getmetadata/{{ counter_id }}" style="position:absolute; left:-9999px;" alt="" /&gt;&lt;/script&gt;
                &lt;noscript&gt;&lt;div&gt;&lt;img src="https://127.0.0.1/api/getmetadata/{{ counter_id }}" style="position:absolute; left:-9999px;" alt="" /&gt;
                &lt;/div&gt;&lt;/noscript&gt;

            </code>
        </pre>
            <button @click="copyToClipboard">Copy script</button>
    </div>
</template>
<script>
import axios from 'axios';
import {API_URL} from "@/consts";


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
            counter_id: 0,
            showF: false,
            name: '',
            link: ''
        }
    },
    methods: {
        copyToClipboard() {
            const el = document.createElement('textarea');
            el.value = document.querySelector('#counter_script code').textContent;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
            alert('Script copied to clipboard!');
        },
        submitForm() {
            const form = new FormData();

            form.append('name', this.name);
            form.append('link', this.link);
            console.log(API_URL)
            axios.post(`${API_URL}/counters/add`, {
                    name: this.name,
                    link: this.link

                },

                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'X-CSRFToken': csrfToken
                    }
                }
            )
                .then(response => {
                    this.counter_id = response.data.counter,
                        this.showF = true
                    console.log(this.showF)

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

#counter_script {
    background-color: #f5f5f5;
    padding: 10px;
    margin: 10px 0;
    border: 2px solid #92d82f;
}
button {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 10px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 10px 0;
    cursor: pointer;
}
.language-html {
    display: block;
    font-size: 14px;
    font-family: monospace;
    white-space: pre-wrap;
    line-height: 1.5;
    color: #333;
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