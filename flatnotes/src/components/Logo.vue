<template>
  <div>
    <img src="../assets/logo-part-icon.svg" /><img
      src="../assets/logo-part-name.svg"
      class="ml-2"
      :class="{ 'responsive-hide': responsive }"
    />
  </div>
</template>

<style lang="scss" scoped>
@media screen and (max-width: 500px) {
  .responsive-hide {
    display: none;
  }
}
</style>

<script>
export default {
  props: {
    responsive: { type: Boolean, default: false },
  },
};
</script>
