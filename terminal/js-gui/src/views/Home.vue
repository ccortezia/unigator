<template>
  <div class="home">
    <HomeHeader/>
    <router-view/>
    <HomeFooter/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import HomeHeader from '../components/HomeHeader.vue';
import HomeFooter from '../components/HomeFooter.vue';

export default Vue.extend({
  name: 'home',
  components: {
    HomeHeader,
    HomeFooter,
  },
});
</script>

<style lang="scss" scoped>
.home {
  display: flex;
  flex-direction: column;
  height: 100vh;

  > footer,
  > header {
    flex-shrink: 0;
  }

  > div {
    flex: 1 0 auto;
  }
}
</style>
