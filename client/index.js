import App from "/App.vue";
import PrimeVue from "primevue/config";
import ToastService from "primevue/toastservice";
import { createApp } from "vue";
import { createPinia } from "pinia";
import { primeStyles } from "./style.js";
import router from "/router.js";

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);
app.use(PrimeVue, {
  unstyled: true,
  pt: primeStyles,
});
app.use(ToastService);
app.mount("#app");
