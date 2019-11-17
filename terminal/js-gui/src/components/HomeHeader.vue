<template>
    <header>
      <router-link class="logo" to="/">HOME</router-link>
      <router-link class="logo" to="/contacts">Contacts</router-link>
      <router-link class="logout-link" to="/login">
        <el-button type="info" round>LOGOUT</el-button>
      </router-link>
    </header>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: ['profile'],
});
</script>


<style lang="scss" scoped>
header {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  border: solid 2px grey;
  min-height: 40px;
  background-color: #222;
}

.logo {
    color: white;
}
</style>
