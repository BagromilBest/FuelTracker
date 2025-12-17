<script setup>
import { onMounted } from 'vue';
import { useAppStore } from './stores/app';
import NavBar from './components/NavBar.vue';

const store = useAppStore();

onMounted(() => {
  store.fetchInit();
});
</script>

<template>
  <div>
    <NavBar />
    <router-view />
  </div>
</template>
