<template>
    <div>
        <form novalidate @submit="checkForm">
            <el-button native-type="submit">SUBMIT</el-button>
        </form>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
    methods: {
        checkForm(e: Event) {
            this.$store.commit('contacts/create', {name: 'Cristiano Cortezia'});
            e.preventDefault();
        },
    },
});
</script>
