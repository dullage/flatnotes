<template>
  <div class="flex h-full flex-col items-center justify-center">
    <Logo class="mb-5" />
    <form @submit.prevent="logIn" class="flex max-w-80 flex-col items-center">
      <TextInput
        v-model="username"
        placeholder="Username"
        class="mb-1"
        required
      />
      <TextInput
        v-model="password"
        placeholder="Password"
        type="password"
        class="mb-1"
        required
      />
      <TextInput
        v-if="globalStore.authType == authTypes.totp"
        v-model="totp"
        placeholder="2FA Code"
        class="mb-1"
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
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";

import { getToken } from "../api.js";
import CustomButton from "../components/CustomButton.vue";
import Logo from "../components/Logo.vue";
import TextInput from "../components/TextInput.vue";
import { authTypes } from "../constants.js";
import { useGlobalStore } from "../globalStore.js";
import { storeToken } from "../tokenStorage.js";
import * as constants from "../constants.js";

const router = useRouter();
const route = useRoute();
const globalStore = useGlobalStore();

const username = ref("");
const password = ref("");
const totp = ref("");
const rememberMe = ref(false);

function logIn() {
  getToken(username.value, password.value, totp.value)
    .then((response) => {
      storeToken(response.data.access_token, rememberMe.value);
      const redirectPath = route.query[constants.params.redirect];
      if (redirectPath) {
        router.push(redirectPath);
      } else {
        router.push({ name: "home" });
      }
    })
    .catch((error) => {
      console.error(error);
      // TODO: Trigger error toast
    });
}
</script>
