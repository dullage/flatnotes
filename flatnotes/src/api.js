import * as constants from "./constants";

import EventBus from "./eventBus";
import axios from "axios";

const api = axios.create();

api.interceptors.request.use(
  function(config) {
    if (config.url !== "/api/token") {
      let token = sessionStorage.getItem("token");
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  function(error) {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  function(response) {
    return response;
  },
  function(error) {
    if (
      typeof error.response !== "undefined" &&
      error.response.status === 401
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
