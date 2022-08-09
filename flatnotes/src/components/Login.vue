<template>
  <div
    class="
      d-flex
      flex-column
      justify-content-center
      align-items-center
      flex-grow-1
    "
  >
    <!-- Logo -->
    <Logo class="mb-3"></Logo>

    <form
      class="d-flex flex-column align-items-center"
      v-on:submit.prevent="login"
    >
      <!-- Username -->
      <div class="mb-1">
        <input
          type="text"
          placeholder="Username"
          class="form-control"
          id="username"
          autocomplete="username"
          v-model="usernameInput"
          autofocus
          required
        />
      </div>

      <!-- Password -->
      <div class="mb-2">
        <input
          type="password"
          placeholder="Password"
          class="form-control"
          id="password"
          autocomplete="current-password"
          v-model="passwordInput"
          required
        />
      </div>

      <!-- Remember Me -->
      <div class="mb-3 form-check">
        <input
          type="checkbox"
          class="form-check-input"
          id="rememberMe"
          v-model="rememberMeInput"
        />
        <label class="form-check-label" for="rememberMe">Remember Me</label>
      </div>

      <!-- Button -->
      <button type="submit" class="bttn">
        <b-icon icon="box-arrow-in-right"></b-icon> Log In
      </button>
    </form>
  </div>
</template>

<script>
import api from "../api";
import * as helpers from "../helpers";
import * as constants from "../constants";
import EventBus from "../eventBus";
import Logo from "./Logo";

export default {
  components: {
    Logo,
  },

  data: function () {
    return {
      usernameInput: null,
      passwordInput: null,
      rememberMeInput: false,
    };
  },

  methods: {
    login: function () {
      let parent = this;
      api
        .post("/api/token", {
          username: this.usernameInput,
          password: this.passwordInput,
        })
        .then(function (response) {
          sessionStorage.setItem("token", response.data.access_token);
          if (parent.rememberMeInput == true) {
            localStorage.setItem("token", response.data.access_token);
          }
          let redirectPath = helpers.getSearchParam(constants.params.redirect);
          EventBus.$emit("navigate", redirectPath || "/");
        })
        .catch(function (error) {
          if (error.handled) {
            return;
          } else if (
            typeof error.response !== "undefined" &&
            [400, 422].includes(error.response.status)
          ) {
            parent.$bvToast.toast("Incorrect Username or Password ✘", {
              variant: "danger",
              noCloseButton: true,
            });
          } else {
            EventBus.$emit("unhandledServerError");
          }
        })
        .finally(function () {
          parent.usernameInput = null;
          parent.passwordInput = null;
          parent.rememberMeInput = false;
        });
    },
  },
};
</script>
