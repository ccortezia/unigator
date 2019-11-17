import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './plugins/element.js';
import './plugins/local-packages.js';

Vue.config.productionTip = false;

(window as any).vm = new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
