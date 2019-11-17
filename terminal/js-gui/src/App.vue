<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script lang="js">
import Vue from 'vue';
export default Vue.extend({
  name: 'app',
});
</script>


<style lang="scss">
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  height: 100vh;
}
</style>
