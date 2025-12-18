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
  <div class="app-root">
    <NavBar />
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
.app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-main {
  flex: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
