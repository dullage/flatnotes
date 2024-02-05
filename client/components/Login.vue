<template>
  <div class="d-flex flex-column justify-content-center align-items-center">
    <!-- Logo -->
    <Logo class="mb-5"></Logo>
    <div
      v-if="authType != null && authType != constants.authTypes.none"
      class="d-flex flex-column justify-content-center align-items-center"
    >
      <form
        v-show="authType != null"
        class="login-form d-flex flex-column align-items-center"
        v-on:submit.prevent="login"
      >
        <div class="mb-1">
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
          <div class="mb-1">
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

          <!-- 2FA -->
          <div v-if="authType == constants.authTypes.totp" class="mb-1">
            <input
              type="text"
              inputmode="numeric"
              pattern="[0-9]*"
              placeholder="2FA Code"
              class="form-control"
              id="totp"
              autocomplete="one-time-code"
              v-model="totpInput"
              required
            />
          </div>
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
          <b-icon icon="box-arrow-in-right"></b-icon><span>Log In</span>
        </button>
      </form>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.login-form {
  input {
    color: var(--colour-text);
    background-color: var(--colour-background-elevated);
    border-color: var(--colour-border);
  }
}
</style>

<script>
import * as constants from "../constants";
import * as helpers from "../helpers";
import { setToken } from "../tokenStorage";

import EventBus from "../eventBus";
import Logo from "./Logo";
import api from "../api";

export default {
  components: {
    Logo,
  },

  props: {
    authType: { type: String, default: null },
  },

  data: function () {
    return {
      usernameInput: null,
      passwordInput: null,
      totpInput: null,
      rememberMeInput: false,
    };
  },

  watch: {
    authType: function () {
      this.skipIfNoneAuthType();
    },
  },

  methods: {
    skipIfNoneAuthType: function () {
      // Skip past the login page if authentication is disabled
      if (this.authType == constants.authTypes.none) {
        EventBus.$emit("navigate", constants.basePaths.home);
      }
    },

    login: function () {
      let parent = this;
      api
        .post("/api/token", {
          username: this.usernameInput,
          password:
            this.authType == constants.authTypes.totp
              ? this.passwordInput + this.totpInput
              : this.passwordInput,
        })
        .then(function (response) {
          setToken(response.data.access_token, parent.rememberMeInput);
          let redirectPath = helpers.getSearchParam(constants.params.redirect);
          EventBus.$emit("navigate", redirectPath || constants.basePaths.home);
        })
        .catch(function (error) {
          if (error.handled) {
            return;
          } else if (
            typeof error.response !== "undefined" &&
            error.response.status == 401
          ) {
            EventBus.$emit("showToast", "danger", "Incorrect login credentials ✘")
          } else {
            EventBus.$emit("unhandledServerErrorToast");
          }
        })
        .finally(function () {
          parent.usernameInput = null;
          parent.passwordInput = null;
          parent.totpInput = null;
          parent.rememberMeInput = false;
        });
    },
  },

  created: function () {
    this.constants = constants;
    this.skipIfNoneAuthType();
  },
};
</script>
