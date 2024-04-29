import * as constants from "./constants.js";

import { Note } from "./classes.js";
import axios from "axios";
import { getStoredToken } from "./tokenStorage.js";
import router from "./router.js";

const api = axios.create();

api.interceptors.request.use(
  // If the request is not for the token endpoint, add the token to the headers.
  function (config) {
    if (config.url !== "/api/token") {
      const token = getStoredToken();
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  function (error) {
    return Promise.reject(error);
  },
);

api.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    // If the response is a 401 Unauthorized, redirect to the login page.
    if (
      error.response?.status === 401 &&
      router.currentRoute.value.name !== "login"
    ) {
      const redirectPath = router.currentRoute.value.fullPath;
      router.push({
        name: "login",
        query: { [constants.params.redirect]: redirectPath },
      });
    }
    return Promise.reject(error);
  },
);

export async function getConfig() {
  try {
    const response = await api.get("/api/config");
    return response.data;
  } catch (error) {
    return Promise.reject(error);
  }
}

export async function getToken(username, password, totp) {
  try {
    const response = await api.post("/api/token", {
      username: username,
      password: totp ? password + totp : password,
    });
    return response.data.access_token;
  } catch (response) {
    return Promise.reject(response);
  }
}

export async function getNotes(term, sort, order, limit) {
  try {
    const response = await api.get("/api/search", {
      params: {
        term: term,
        sort: sort,
        order: order,
        limit: limit,
      },
    });
    return response.data.map(
      (note) => new Note(note.title, note.lastModified, note.content),
    );
  } catch (response) {
    return Promise.reject(response);
  }
}
