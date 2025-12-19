<script setup>
import { ref } from 'vue';
import { useAppStore } from '../stores/app';

const emit = defineEmits(['success', 'cancel']);
const store = useAppStore();

const password = ref('');
const error = ref('');
const loading = ref(false);

async function handleLogin() {
  if (!password.value) {
    error.value = 'Password is required';
    return;
  }
  
  loading.value = true;
  error.value = '';
  
  try {
    await store.adminLogin(password.value);
    emit('success');
  } catch (e) {
    error.value = 'Invalid password';
  } finally {
    loading.value = false;
  }
}

function handleCancel() {
  emit('cancel');
}
</script>

<template>
  <div class="modal-overlay" @click.self="handleCancel">
    <div class="modal-content">
      <div class="modal-header">
        <svg viewBox="0 0 24 24" fill="none" style="width: 32px; height: 32px; color: var(--md-sys-color-primary);">
          <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z" fill="currentColor"/>
        </svg>
        <h2>Admin Access</h2>
      </div>
      
      <div class="modal-body">
        <p class="modal-description">Enter admin password to access administrative functions</p>
        
        <div class="form-section">
          <label>Password</label>
          <input
            type="password"
            v-model="password"
            placeholder="Enter admin password"
            @keyup.enter="handleLogin"
            :disabled="loading"
            autofocus
          >
          <div class="error-msg" v-if="error">⚠ {{ error }}</div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn-secondary" @click="handleCancel" :disabled="loading">
          Cancel
        </button>
        <button @click="handleLogin" :disabled="loading || !password">
          <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px; margin-right: 8px;" v-if="!loading">
            <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" fill="currentColor"/>
          </svg>
          <span v-if="loading">Verifying...</span>
          <span v-else>Login</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: var(--md-sys-color-surface-container-high);
  border-radius: var(--md-shape-corner-large);
  box-shadow: var(--md-elevation-3);
  border: 1px solid var(--md-sys-color-outline);
  max-width: 480px;
  width: 90%;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-md);
  padding: var(--md-spacing-lg);
  border-bottom: 1px solid var(--md-sys-color-outline-variant);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 500;
}

.modal-body {
  padding: var(--md-spacing-lg);
}

.modal-description {
  color: var(--md-sys-color-on-surface-variant);
  margin-bottom: var(--md-spacing-lg);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--md-spacing-md);
  padding: var(--md-spacing-lg);
  border-top: 1px solid var(--md-sys-color-outline-variant);
}

.btn-secondary {
  background: var(--md-sys-color-surface-container-highest);
  color: var(--md-sys-color-on-surface);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--md-sys-color-surface-container-high);
}

.form-section {
  margin-bottom: 0;
}

.error-msg {
  margin-top: var(--md-spacing-sm);
}
</style>
