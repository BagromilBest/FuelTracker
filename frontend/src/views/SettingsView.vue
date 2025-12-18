<script setup>
import { ref, onMounted } from 'vue';
import { useAppStore } from '../stores/app';

const store = useAppStore();
const settingsForm = ref({ currency: 'CZK', fuel_price: 35.5 });
const userForm = ref({ name: '', color: '#90CAF9' });
const message = ref('');
const isError = ref(false);

onMounted(() => {
  if (store.settings) {
    settingsForm.value = { ...store.settings };
  }
});

async function updateSettings() {
  try {
    const response = await fetch('/api/settings', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settingsForm.value)
    });
    if (response.ok) {
      await store.fetchInit();
      isError.value = false;
      message.value = 'Settings updated successfully!';
      setTimeout(() => message.value = '', 3000);
    } else {
      const error = await response.json();
      isError.value = true;
      message.value = `Error updating settings: ${error.detail || 'Unknown error'}`;
    }
  } catch (e) {
    isError.value = true;
    message.value = `Error updating settings: ${e.message || 'Network error'}`;
  }
}

async function addUser() {
  try {
    await store.addUser(userForm.value.name, userForm.value.color);
    userForm.value = { name: '', color: '#90CAF9' };
    isError.value = false;
    message.value = 'User added successfully!';
    setTimeout(() => message.value = '', 3000);
  } catch (e) {
    isError.value = true;
    message.value = `Error adding user: ${e.response?.data?.detail || e.message || 'Unknown error'}`;
  }
}
</script>

<template>
  <div class="container slide-in">
    <div class="page-header">
      <h1>
        <svg viewBox="0 0 24 24" fill="none" style="width: 40px; height: 40px;">
          <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" fill="currentColor"/>
        </svg>
        Settings
      </h1>
    </div>

    <div class="settings-grid">
      <div class="card">
        <div class="card-header">
          <svg viewBox="0 0 24 24" fill="none" style="width: 24px; height: 24px; color: var(--md-sys-color-primary);">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" fill="currentColor"/>
          </svg>
          <h3>General Settings</h3>
        </div>
        
        <div class="success-msg" v-if="message && !isError">
          ✓ {{ message }}
        </div>
        <div class="error-msg" v-if="message && isError">
          ⚠ {{ message }}
        </div>
        
        <div class="form-section">
          <label>Currency Symbol</label>
          <input 
            type="text" 
            v-model="settingsForm.currency" 
            placeholder="e.g., CZK, USD, EUR"
            maxlength="10"
          >
          <small>Used for displaying costs throughout the app</small>
        </div>
        
        <div class="form-section">
          <label>Fuel Price per Liter</label>
          <div class="input-group">
            <input 
              type="number" 
              step="0.1" 
              v-model.number="settingsForm.fuel_price" 
              placeholder="35.50"
              min="0"
            >
            <span class="input-suffix">{{ settingsForm.currency }}/L</span>
          </div>
          <small>Current fuel price for cost calculations</small>
        </div>
        
        <button @click="updateSettings">
          <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px; margin-right: 8px;">
            <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" fill="currentColor"/>
          </svg>
          Save Settings
        </button>
      </div>

      <div class="card">
        <div class="card-header">
          <svg viewBox="0 0 24 24" fill="none" style="width: 24px; height: 24px; color: var(--md-sys-color-primary);">
            <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" fill="currentColor"/>
          </svg>
          <h3>Manage Drivers</h3>
        </div>
        
        <div v-if="store.users.length > 0" class="users-section">
          <h4>Current Drivers</h4>
          <div class="users-list">
            <div v-for="user in store.users" :key="user.id" class="user-item">
              <span class="user-color-dot" :style="{ background: user.color }"></span>
              <span class="user-name">{{ user.name }}</span>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h4>Add New Driver</h4>
          
          <label>Driver Name</label>
          <input 
            type="text" 
            v-model="userForm.name" 
            placeholder="Enter driver name"
            maxlength="50"
          >
          
          <label>Identification Color</label>
          <div class="color-picker-wrapper">
            <input type="color" v-model="userForm.color" class="color-picker">
            <div class="color-preview" :style="{ background: userForm.color }"></div>
            <span class="color-value">{{ userForm.color }}</span>
          </div>
          <small>Choose a unique color to identify this driver in reports</small>
          
          <button @click="addUser" :disabled="!userForm.name">
            <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px; margin-right: 8px;">
              <path d="M15 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm-9-2V7H4v3H1v2h3v3h2v-3h3v-2H6zm9 4c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="currentColor"/>
            </svg>
            Add Driver
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  margin-bottom: var(--md-spacing-xl);
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--md-spacing-lg);
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-md);
  margin-bottom: var(--md-spacing-lg);
}

.card-header h3 {
  margin: 0;
}

.form-section {
  margin-bottom: var(--md-spacing-xl);
}

.form-section:last-of-type {
  margin-bottom: var(--md-spacing-md);
}

.form-section small {
  display: block;
  margin-top: var(--md-spacing-xs);
}

.input-group {
  position: relative;
}

.input-suffix {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.875rem;
  font-weight: 500;
  pointer-events: none;
}

.input-group input {
  padding-right: 80px;
}

.users-section {
  margin-bottom: var(--md-spacing-xl);
  padding-bottom: var(--md-spacing-lg);
  border-bottom: 1px solid var(--md-sys-color-outline-variant);
}

.users-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--md-spacing-sm);
  margin-top: var(--md-spacing-md);
}

.user-item {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-sm);
  padding: var(--md-spacing-sm) var(--md-spacing-md);
  background: var(--md-sys-color-surface-container-high);
  border-radius: var(--md-shape-corner-xlarge);
  font-weight: 500;
}

.user-color-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  box-shadow: 0 0 0 2px var(--md-sys-color-surface-container);
}

.color-picker-wrapper {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-md);
  padding: var(--md-spacing-md);
  background: var(--md-sys-color-surface-container-low);
  border-radius: var(--md-shape-corner-small);
  margin-bottom: var(--md-spacing-sm);
}

.color-picker {
  width: 60px;
  height: 48px;
}

.color-preview {
  width: 48px;
  height: 48px;
  border-radius: var(--md-shape-corner-small);
  box-shadow: var(--md-elevation-1);
}

.color-value {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: var(--md-sys-color-on-surface-variant);
  text-transform: uppercase;
}

button {
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 900px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}
</style>
