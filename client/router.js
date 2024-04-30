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
      props: (route) => ({ redirect: route.query[constants.params.redirect] }),
    },
    {
      path: "/note/:title?",
      name: "note",
      component: () => import("./views/Note.vue"),
      props: true,
    },
    {
      path: "/search",
      name: "search",
      component: () => import("./views/Search.vue"),
      props: (route) => ({
        searchTerm: route.query[constants.params.searchTerm],
      }),
    },
  ],
});

export default router;
