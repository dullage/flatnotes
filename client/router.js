import { createRouter, createWebHistory } from "vue-router";

import Home from "/views/Home.vue";
import LogIn from "/views/LogIn.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/login",
      name: "login",
      component: LogIn,
    },
  ],
});

export default router;
