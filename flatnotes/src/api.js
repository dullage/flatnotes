import axios from "axios";
import EventBus from "./eventBus.js";

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
      EventBus.$emit("logout");
    }
    return Promise.reject(error);
  }
);

export default api;
