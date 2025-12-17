<script setup>
import { useRoute } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();
const isActive = (name) => computed(() => route.name === name);
</script>

<template>
  <nav class="nav">
    <router-link to="/" :class="{ active: isActive('dashboard').value }">Dashboard</router-link>
    <router-link to="/history" :class="{ active: isActive('history').value }">History</router-link>
    <router-link to="/settings" :class="{ active: isActive('settings').value }">Settings</router-link>
  </nav>
</template>
