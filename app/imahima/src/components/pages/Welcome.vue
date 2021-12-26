<template>
    <div class="container">
        Welcome!!
      <div>
        <button class="btn btn-primary" @click="push">ログアウト</button>
      </div>
    </div>
</template>

<script>
import router from "../../router";
export default {
  name: "Welcome",
  methods: {
    push() {
      localStorage.setItem('token', '');
      this.$router.push('Login');
    }
  }
};
</script>