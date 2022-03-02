import App from "./components/App.vue";
import Vue from "vue";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";

import "./main.scss"

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

new Vue({
  el: "#app",
  render: (h) => h(App),
});
