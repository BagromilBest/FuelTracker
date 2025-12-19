<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAppStore } from '../stores/app';

const router = useRouter();
const store = useAppStore();

const selectedUserId = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);
const showAdminLogin = ref(false);

onMounted(async () => {
  // Fetch users for the login dropdown
  try {
    await store.fetchUsers();
  } catch (e) {
    // If fetch fails, that's okay - user can try admin login
    console.error('Failed to fetch users:', e);
  }
});

const canSubmit = computed(() => {
  if (showAdminLogin.value) {
    return password.value !== '';
  }
  return selectedUserId.value !== '' && password.value !== '';
});

async function handleLogin() {
  if (!canSubmit.value) return;
  
  loading.value = true;
  error.value = '';
  
  try {
    if (showAdminLogin.value) {
      await store.adminLogin(password.value);
    } else {
      await store.userLogin(parseInt(selectedUserId.value), password.value);
    }
    
    await store.fetchInit();
    router.push('/');
  } catch (e) {
    error.value = e.response?.data?.detail || 'Login failed. Please check your credentials.';
  } finally {
    loading.value = false;
  }
}

function toggleAdminLogin() {
  showAdminLogin.value = !showAdminLogin.value;
  selectedUserId.value = '';
  password.value = '';
  error.value = '';
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <svg viewBox="0 0 24 24" fill="none" style="width: 48px; height: 48px; color: var(--md-sys-color-primary);">
          <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z" fill="currentColor"/>
        </svg>
        <h1 v-if="!showAdminLogin">Fuel Tracker Login</h1>
        <h1 v-else>Admin Login</h1>
      </div>
      
      <div class="error-msg" v-if="error">
        ⚠ {{ error }}
      </div>
      
      <div class="login-form">
        <div v-if="!showAdminLogin">
          <label>Select Your Account</label>
          <select v-model="selectedUserId" :disabled="loading">
            <option disabled value="">Choose a driver</option>
            <option v-for="user in store.users" :key="user.id" :value="user.id">
              {{ user.name }}
            </option>
          </select>
        </div>
        
        <label>Password</label>
        <input 
          type="password" 
          v-model="password" 
          placeholder="Enter your password"
          :disabled="loading"
          @keyup.enter="handleLogin"
        />
        
        <button @click="handleLogin" :disabled="!canSubmit || loading">
          <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px; margin-right: 8px;">
            <path d="M11 7L9.6 8.4l2.6 2.6H2v2h10.2l-2.6 2.6L11 17l5-5-5-5zm9 12h-8v2h8c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-8v2h8v14z" fill="currentColor"/>
          </svg>
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
        
        <div class="login-divider">
          <span>or</span>
        </div>
        
        <button class="secondary" @click="toggleAdminLogin" :disabled="loading">
          <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px; margin-right: 8px;">
            <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z" fill="currentColor"/>
          </svg>
          {{ showAdminLogin ? 'Back to User Login' : 'Admin Login' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--md-sys-color-background);
  padding: var(--md-spacing-lg);
}

.login-card {
  background: var(--md-sys-color-surface-container);
  border-radius: var(--md-shape-corner-large);
  padding: var(--md-spacing-xl);
  box-shadow: var(--md-elevation-3);
  border: 1px solid var(--md-sys-color-outline-variant);
  width: 100%;
  max-width: 450px;
  animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.login-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--md-spacing-md);
  margin-bottom: var(--md-spacing-xl);
  text-align: center;
}

.login-header h1 {
  margin: 0;
  font-size: 1.75rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--md-spacing-xs);
}

.login-divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: var(--md-spacing-lg) 0;
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.875rem;
}

.login-divider::before,
.login-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--md-sys-color-outline);
}

.login-divider span {
  padding: 0 var(--md-spacing-md);
}

button {
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
