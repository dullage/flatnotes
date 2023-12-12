import "./global.scss"

import { BootstrapVue, IconsPlugin } from "bootstrap-vue";

import App from "./components/App.vue";
import Vue from "vue";

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

new Vue({
  el: "#app",
  render: (h) => h(App),
});
