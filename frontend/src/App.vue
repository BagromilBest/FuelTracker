<script setup>
import { onMounted } from 'vue';
import { useAppStore } from './stores/app';
import { useRouter } from 'vue-router';
import NavBar from './components/NavBar.vue';

const store = useAppStore();
const router = useRouter();

onMounted(async () => {
  // Restore authentication from localStorage
  store.restoreAuth();
  
  // If authenticated, fetch initial data
  if (store.isAuthenticated) {
    try {
      await store.fetchInit();
    } catch (error) {
      // If fetch fails (e.g., token expired), logout and redirect to login
      store.logout();
      router.push('/login');
    }
  } else {
    // Not authenticated, redirect to login
    router.push('/login');
  }
});
</script>

<template>
  <div class="app-root">
    <NavBar v-if="store.isAuthenticated" />
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
