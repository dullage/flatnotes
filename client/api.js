import * as constants from "./constants.js";

import EventBus from "./eventBus.js";
import axios from "axios";
import { getToken } from "./tokenStorage.js";

const api = axios.create();

api.interceptors.request.use(
  function (config) {
    if (config.url !== "/api/token") {
      const token = getToken();
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    if (
      typeof error.response !== "undefined" &&
      error.response.status === 401 &&
      error.response.config.url !== "/api/token"
    ) {
      EventBus.$emit(
        "navigate",
        `${constants.basePaths.login}?${constants.params.redirect}=${encodeURI(
          window.location.pathname + window.location.search
        )}`
      );
      error.handled = true;
    }
    return Promise.reject(error);
  }
);

export default api;
