import * as constants from "./constants.js";

import { createRouter, createWebHistory } from "vue-router";

import { authCheck } from "./api.js";

const router = createRouter({
  history: createWebHistory(""),
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
      path: "/note/:title",
      name: "note",
      component: () => import("./views/Note.vue"),
      props: true,
    },
    {
      path: "/new",
      name: "new",
      component: () => import("./views/Note.vue"),
    },
    {
      path: "/search",
      name: "search",
      component: () => import("./views/SearchResults.vue"),
      props: (route) => ({
        searchTerm: route.query[constants.params.searchTerm],
        sortBy: Number(route.query[constants.params.sortBy]) || undefined,
      }),
    },
  ],
});

// Check the user is authenticated on first navigation (unless going to login)
let authChecked = false;
router.beforeEach(async (to) => {
  if (authChecked || to.name === "login") {
    return;
  }
  try {
    await authCheck();
    return;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      return {
        name: "login",
        query: { [constants.params.redirect]: to.fullPath },
      };
    }
  } finally {
    authChecked = true;
  }
});

router.afterEach((to) => {
  let title = "flatnotes";
  if (to.name === "note") {
    if (to.params.title) {
      title = `${to.params.title} - ${title}`;
    } else {
      title = "New Note - " + title;
    }
  }
  document.title = title;
});

export default router;
