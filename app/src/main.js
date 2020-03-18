/**
 * @file app/src/main.js
 */
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import axios from "axios";

axios.defaults.baseURL = 'https://1uhxwlcib5.execute-api.eu-west-2.amazonaws.com/prod/';

Vue.config.productionTip = false;


// /**
//  * filters
//  *
//  * @link https://vuejs.org/v2/guide/filters.html
//  */
// Vue.filter('capitalize', function (value) {
//   if (!value) return ''
//   value = value.toString()
//   return value.charAt(0).toUpperCase() + value.slice(1)
// });


new Vue({
  router,
  store,
  vuetify,
  created() {
    //
  },
  render: h => h(App)
}).$mount('#app')
