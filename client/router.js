import * as constants from "./constants.js";

import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("./views/Home.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("./views/LogIn.vue"),
      props: (route) => ({ [constants.params.redirect]: route.query.redirect }),
    },
    {
      path: "/note/:title",
      name: "note",
      component: () => import("./views/Note.vue"),
      props: true,
    },
  ],
});

export default router;
