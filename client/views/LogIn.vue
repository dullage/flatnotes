<template>
  <div class="flex h-full flex-col items-center justify-center">
    <Logo class="mb-5" />
    <form @submit.prevent="logIn" class="flex max-w-80 flex-col items-center">
      <TextInput
        v-model="username"
        id="username"
        placeholder="Username"
        class="mb-1"
        autocomplete="username"
        required
      />
      <TextInput
        v-model="password"
        id="password"
        placeholder="Password"
        type="password"
        class="mb-1"
        autocomplete="current-password"
        required
      />
      <TextInput
        v-if="globalStore.config.authType == authTypes.totp"
        v-model="totp"
        id="one-time-code"
        placeholder="2FA Code"
        class="mb-1"
        autocomplete="one-time-code"
        required
      />
      <div class="mb-4 flex">
        <input
          type="checkbox"
          id="remember-me"
          v-model="rememberMe"
          class="mr-1"
        />
        <label for="remember-me">Remember Me</label>
      </div>
      <CustomButton :iconPath="mdilLogin" label="Log In" />
    </form>
  </div>
</template>

<script setup>
import { mdilLogin } from "@mdi/light-js";
import { useToast } from "primevue/usetoast";
import { ref, watch } from "vue";
import { useRouter } from "vue-router";

import { apiErrorHandler, getToken } from "../api.js";
import CustomButton from "../components/CustomButton.vue";
import Logo from "../components/Logo.vue";
import TextInput from "../components/TextInput.vue";
import { authTypes } from "../constants.js";
import { useGlobalStore } from "../globalStore.js";
import { getToastOptions } from "../helpers.js";
import { storeToken } from "../tokenStorage.js";

const props = defineProps({ redirect: String });

const globalStore = useGlobalStore();
const router = useRouter();
const toast = useToast();

const username = ref("");
const password = ref("");
const totp = ref("");
const rememberMe = ref(false);

function logIn() {
  getToken(username.value, password.value, totp.value)
    .then((access_token) => {
      storeToken(access_token, rememberMe.value);
      if (props.redirect) {
        router.push(props.redirect);
      } else {
        router.push({ name: "home" });
      }
    })
    .catch((error) => {
      username.value = "";
      password.value = "";
      totp.value = "";

      if (error.response?.status === 401) {
        toast.add(
          getToastOptions(
            "Please check your credentials and try again.",
            "Login Failed",
            "error",
          ),
        );
      } else {
        apiErrorHandler(error, toast);
      }
    });
}

// Redirect to home if authentication is disabled.
if (globalStore.config.authType === authTypes.none) {
  router.push({ name: "home" });
}
</script>
