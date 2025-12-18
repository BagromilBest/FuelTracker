<script setup>
import { useRoute } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();
const isActive = (name) => computed(() => route.name === name);
</script>

<template>
  <nav class="app-nav">
    <div class="nav-container">
      <div class="nav-brand">
        <svg class="nav-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M17 3H7C5.89543 3 5 3.89543 5 5V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V5C19 3.89543 18.1046 3 17 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 7V13M12 13L9 11M12 13L15 11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M9 17H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span class="nav-title">FuelTracker</span>
      </div>
      
      <div class="nav-links">
        <router-link to="/" class="nav-link" :class="{ 'nav-link-active': isActive('dashboard').value }">
          <svg class="nav-link-icon" viewBox="0 0 24 24" fill="none">
            <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z" fill="currentColor"/>
          </svg>
          <span>Dashboard</span>
        </router-link>
        
        <router-link to="/history" class="nav-link" :class="{ 'nav-link-active': isActive('history').value }">
          <svg class="nav-link-icon" viewBox="0 0 24 24" fill="none">
            <path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z" fill="currentColor"/>
          </svg>
          <span>History</span>
        </router-link>
        
        <router-link to="/settings" class="nav-link" :class="{ 'nav-link-active': isActive('settings').value }">
          <svg class="nav-link-icon" viewBox="0 0 24 24" fill="none">
            <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" fill="currentColor"/>
          </svg>
          <span>Settings</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.app-nav {
  background: var(--md-sys-color-surface-container);
  border-bottom: 1px solid var(--md-sys-color-outline-variant);
  box-shadow: var(--md-elevation-1);
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--md-spacing-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-md);
}

.nav-icon {
  width: 32px;
  height: 32px;
  color: var(--md-sys-color-primary);
}

.nav-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--md-sys-color-on-surface);
  letter-spacing: 0.5px;
}

.nav-links {
  display: flex;
  gap: var(--md-spacing-xs);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-sm);
  padding: var(--md-spacing-sm) var(--md-spacing-md);
  border-radius: var(--md-shape-corner-large);
  color: var(--md-sys-color-on-surface-variant);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.nav-link-icon {
  width: 20px;
  height: 20px;
}

.nav-link:hover {
  background: var(--md-sys-color-surface-container-highest);
  color: var(--md-sys-color-on-surface);
}

.nav-link-active {
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-primary);
}

.nav-link-active:hover {
  background: var(--md-sys-color-primary-container);
}

@media (max-width: 768px) {
  .nav-container {
    padding: 0 var(--md-spacing-md);
  }
  
  .nav-title {
    display: none;
  }
  
  .nav-link span {
    display: none;
  }
  
  .nav-link {
    padding: var(--md-spacing-sm);
  }
}
</style>
