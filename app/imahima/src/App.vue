<template>
  <router-view/>
</template>

<style>
#app {
  font-family: "游ゴシック";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100vh;
  width: 100vw;
  overflow: auto;
  -ms-overflow-style: none;    /* IE, Edge 対応 */
  scrollbar-width: none;       /* Firefox 対応 */
}
#app::-webkit-scrollbar {  /* Chrome, Safari 対応 */
  display:none;
}
</style>
