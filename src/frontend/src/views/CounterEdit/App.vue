<template>
  <div ref="counterEdit" class="mt-5 mb-5">
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-3" style="max-width: 600px;">
      <h3>Код счетчика</h3>
      <div class="d-flex flex-wrap align-items-center">
        <div v-if="message" class="me-3">{{ message }}</div>
        <button @click="copyScript" class="btn-save">Копировать</button>
      </div>
    </div>
    <p ref="script" id="text" class="counter-code p-4">
      &lt;!-- FreeStat counter --&gt;
      <br>
      &lt;div id="counter_id" style="transform: translateX(9999px);"&gt;{{ counterId }}&lt;/div&gt;
      <br>
      &lt;script src="https://site-stats.ya.uenv.ru/src/src/assets/collectdata.js"&gt;&lt;/script&gt;
      <br>
      &lt;noscript&gt;&lt;div&gt;&lt;img src="https://site-stats.ya.uenv.ru/api/getmetadata/{{ counterId }}"/&gt;&lt;/div&gt;&lt;/noscript&gt;
    </p>
  </div>
</template>

<script>
import {ref} from 'vue';

export default {
  data() {
    return {
      counterId: null,
      message: ''
    }
  },
  created() {
    this.counterId = document.querySelector('#counter_edit').getAttribute('data-counter-id');
  },
  mounted() {
    this.script = ref(null);
  },
  methods: {
    copyScript() {
      navigator.clipboard.writeText(this.$refs.script.innerText);
      this.message = 'Код скопирован!'
    }
  }
}
</script>

<style scoped>

</style>