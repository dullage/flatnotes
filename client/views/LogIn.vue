<template>
  <div class="flex h-full flex-col items-center justify-center">
    <Logo class="mb-5" />
    <form @submit.prevent="login" class="flex max-w-80 flex-col items-center">
      <TextInput placeholder="Username" class="mb-1" required />
      <TextInput placeholder="Password" type="password" class="mb-1" required />
      <TextInput placeholder="2FA Code" class="mb-1" required />
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
import { RouterLink, useRouter } from "vue-router";

import CustomButton from "../components/CustomButton.vue";
import Logo from "../components/Logo.vue";
import TextInput from "../components/TextInput.vue";

const router = useRouter();
const rememberMe = ref(false);

function login() {
  router.push({ name: "home" });
  // TODO: Implement login functionality
}
</script>
