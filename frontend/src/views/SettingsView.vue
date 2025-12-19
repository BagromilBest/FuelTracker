<script setup>
import { ref, onMounted } from 'vue';
import { useAppStore } from '../stores/app';
import AdminLogin from '../components/AdminLogin.vue';
import AdminPanel from '../components/AdminPanel.vue';
import DriverForm from '../components/DriverForm.vue';

const store = useAppStore();
const settingsForm = ref({ currency: 'CZK', fuel_price: 35.5 });
const message = ref('');
const isError = ref(false);
const showAdminLogin = ref(false);
const showAdminPanel = ref(false);
const showDriverForm = ref(false);
const editingDriver = ref(null);

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

function openDriverForm(driver = null) {
  editingDriver.value = driver;
  showDriverForm.value = true;
}

async function handleDriverSubmit(formData) {
  try {
    if (editingDriver.value) {
      // Edit existing driver (requires admin)
      if (!store.isAdminAuthenticated) {
        isError.value = true;
        message.value = 'Admin authentication required to edit drivers';
        return;
      }
      
      const updateData = {
        name: formData.name,
        color: formData.color
      };
      if (formData.password) {
        updateData.password = formData.password;
      }
      
      const response = await fetch(`/api/admin/users/${editingDriver.value.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${store.adminToken}`
        },
        body: JSON.stringify(updateData)
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update driver');
      }
      
      await store.fetchInit();
      showDriverForm.value = false;
      editingDriver.value = null;
      isError.value = false;
      message.value = 'Driver updated successfully!';
      setTimeout(() => message.value = '', 3000);
    } else {
      // Create new driver
      await store.addUser(formData.name, formData.color, formData.password);
      showDriverForm.value = false;
      isError.value = false;
      message.value = 'Driver added successfully!';
      setTimeout(() => message.value = '', 3000);
    }
  } catch (e) {
    isError.value = true;
    message.value = `Error: ${e.message || 'Unknown error'}`;
  }
}

async function deleteDriver(driver) {
  if (!store.isAdminAuthenticated) {
    isError.value = true;
    message.value = 'Admin authentication required to delete drivers';
    return;
  }
  
  if (!confirm(`Are you sure you want to delete driver "${driver.name}"? This action cannot be undone.`)) {
    return;
  }
  
  try {
    const response = await fetch(`/api/admin/users/${driver.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${store.adminToken}`
      }
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to delete driver');
    }
    
    await store.fetchInit();
    isError.value = false;
    message.value = 'Driver deleted successfully!';
    setTimeout(() => message.value = '', 3000);
  } catch (e) {
    isError.value = true;
    message.value = `Error deleting driver: ${e.message || 'Unknown error'}`;
  }
}

function openAdminLogin() {
  if (store.isAdminAuthenticated) {
    showAdminPanel.value = true;
  } else {
    showAdminLogin.value = true;
  }
}

function handleAdminLoginSuccess() {
  showAdminLogin.value = false;
  showAdminPanel.value = true;
}

function handleAdminPanelClose() {
  showAdminPanel.value = false;
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
        
        <button @click="openAdminLogin" class="admin-access-btn" style="margin-bottom: var(--md-spacing-lg);">
          <svg viewBox="0 0 24 24" fill="none" style="width: 20px; height: 20px; margin-right: 8px;">
            <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z" fill="currentColor"/>
          </svg>
          {{ store.isAdminAuthenticated ? 'Admin Panel' : 'Admin Access' }}
        </button>
        
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
        
        <div v-if="store.users.length > 0" class="drivers-section">
          <div v-for="user in store.users" :key="user.id" class="driver-row">
            <div class="driver-info">
              <span class="user-color-dot" :style="{ background: user.color }"></span>
              <span class="user-name">{{ user.name }}</span>
            </div>
            <div class="driver-actions" v-if="store.isAdminAuthenticated">
              <button @click="openDriverForm(user)" class="icon-btn edit-btn" title="Edit driver">
                <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px;">
                  <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="currentColor"/>
                </svg>
              </button>
              <button @click="deleteDriver(user)" class="icon-btn delete-btn" title="Delete driver">
                <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px;">
                  <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" fill="currentColor"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" style="width: 48px; height: 48px; color: var(--md-sys-color-on-surface-variant); opacity: 0.5;">
            <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" fill="currentColor"/>
          </svg>
          <p>No drivers yet</p>
        </div>

        <button @click="openDriverForm()" class="add-driver-btn">
          <svg viewBox="0 0 24 24" fill="none" style="width: 20px; height: 20px; margin-right: 8px;">
            <path d="M15 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm-9-2V7H4v3H1v2h3v3h2v-3h3v-2H6zm9 4c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="currentColor"/>
          </svg>
          Add New Driver
        </button>
      </div>
    </div>

    <!-- Admin Login Modal -->
    <AdminLogin 
      v-if="showAdminLogin" 
      @success="handleAdminLoginSuccess"
      @cancel="showAdminLogin = false"
    />

    <!-- Admin Panel Modal -->
    <AdminPanel
      v-if="showAdminPanel"
      @close="handleAdminPanelClose"
    />

    <!-- Driver Form Modal -->
    <DriverForm
      v-if="showDriverForm"
      :driver="editingDriver"
      @submit="handleDriverSubmit"
      @cancel="showDriverForm = false; editingDriver = null"
    />
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

.admin-access-btn {
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.admin-access-btn:hover {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
}

.drivers-section {
  margin-bottom: var(--md-spacing-lg);
}

.driver-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--md-spacing-md);
  margin-bottom: var(--md-spacing-sm);
  background: var(--md-sys-color-surface-container);
  border-radius: var(--md-shape-corner-medium);
  transition: background 0.2s;
}

.driver-row:hover {
  background: var(--md-sys-color-surface-container-high);
}

.driver-row:last-child {
  margin-bottom: 0;
}

.driver-info {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-md);
}

.user-name {
  font-weight: 500;
  font-size: 1rem;
}

.driver-actions {
  display: flex;
  gap: var(--md-spacing-sm);
}

.icon-btn {
  background: transparent;
  border: none;
  padding: 8px;
  border-radius: var(--md-shape-corner-small);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.edit-btn {
  color: var(--md-sys-color-primary);
}

.edit-btn:hover {
  background: var(--md-sys-color-primary-container);
}

.delete-btn {
  color: var(--md-sys-color-error);
}

.delete-btn:hover {
  background: var(--md-sys-color-error-container);
}

.empty-state {
  text-align: center;
  padding: var(--md-spacing-xl);
  color: var(--md-sys-color-on-surface-variant);
}

.empty-state p {
  margin-top: var(--md-spacing-md);
  font-size: 0.875rem;
}

.add-driver-btn {
  width: 100%;
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-top: var(--md-spacing-md);
}

.add-driver-btn:hover {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
}
</style>
