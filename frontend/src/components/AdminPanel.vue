<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAppStore } from '../stores/app';
import api from '../services/api';

const emit = defineEmits(['close']);
const store = useAppStore();

const activeTab = ref('rides');
const selectedUser = ref(null);
const rides = ref([]);
const editingRide = ref(null);
const editForm = ref({});
const message = ref('');
const isError = ref(false);
const loading = ref(false);

// Password change form
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
});

onMounted(() => {
  if (store.users.length > 0) {
    selectedUser.value = store.users[0].id;
    loadUserRides();
  }
});

async function loadUserRides() {
  if (!selectedUser.value) return;
  
  loading.value = true;
  try {
    const response = await api.get(`/admin/users/${selectedUser.value}/rides`, {
      headers: store.getAdminHeaders()
    });
    rides.value = response.data;
  } catch (e) {
    showError(`Failed to load rides: ${e.response?.data?.detail || e.message}`);
  } finally {
    loading.value = false;
  }
}

function startEdit(ride) {
  editingRide.value = ride.id;
  editForm.value = {
    distance_km: ride.distance_km,
    consumption_l100km: ride.consumption_l100km,
    fuel_liters: ride.fuel_liters
  };
}

function cancelEdit() {
  editingRide.value = null;
  editForm.value = {};
}

function onFieldChange() {
  // Auto-calculate the third value if two are provided
  const { distance_km, consumption_l100km, fuel_liters } = editForm.value;
  
  const hasDistance = distance_km !== null && distance_km !== undefined && distance_km > 0;
  const hasConsumption = consumption_l100km !== null && consumption_l100km !== undefined && consumption_l100km > 0;
  const hasFuel = fuel_liters !== null && fuel_liters !== undefined && fuel_liters > 0;
  
  const count = [hasDistance, hasConsumption, hasFuel].filter(Boolean).length;
  
  if (count === 2) {
    // Calculate the missing value (with division by zero protection)
    if (!hasDistance && hasConsumption && hasFuel && consumption_l100km > 0) {
      // Calculate distance: d = (f * 100) / c
      editForm.value.distance_km = parseFloat(((fuel_liters * 100) / consumption_l100km).toFixed(2));
    } else if (!hasConsumption && hasDistance && hasFuel && distance_km > 0) {
      // Calculate consumption: c = (f * 100) / d
      editForm.value.consumption_l100km = parseFloat(((fuel_liters * 100) / distance_km).toFixed(2));
    } else if (!hasFuel && hasDistance && hasConsumption) {
      // Calculate fuel: f = (d * c) / 100
      editForm.value.fuel_liters = parseFloat(((distance_km * consumption_l100km) / 100).toFixed(2));
    }
  }
}

async function saveEdit(rideId) {
  loading.value = true;
  try {
    await api.put(`/admin/rides/${rideId}`, editForm.value, {
      headers: store.getAdminHeaders()
    });
    showSuccess('Ride updated successfully');
    await loadUserRides();
    // Refresh dashboard stats
    await store.fetchInit();
    cancelEdit();
  } catch (e) {
    showError(`Failed to update ride: ${e.response?.data?.detail || e.message}`);
  } finally {
    loading.value = false;
  }
}

async function deleteRide(rideId) {
  if (!confirm('Are you sure you want to delete this ride?')) return;
  
  loading.value = true;
  try {
    await api.delete(`/admin/rides/${rideId}`, {
      headers: store.getAdminHeaders()
    });
    showSuccess('Ride deleted successfully');
    await loadUserRides();
    // Refresh dashboard stats
    await store.fetchInit();
  } catch (e) {
    showError(`Failed to delete ride: ${e.response?.data?.detail || e.message}`);
  } finally {
    loading.value = false;
  }
}

async function changePassword() {
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    showError('New passwords do not match');
    return;
  }
  
  if (!passwordForm.value.new_password || passwordForm.value.new_password.length < 6) {
    showError('New password must be at least 6 characters');
    return;
  }
  
  loading.value = true;
  try {
    await api.post('/admin/password', {
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    }, {
      headers: store.getAdminHeaders()
    });
    showSuccess('Password changed successfully');
    passwordForm.value = { old_password: '', new_password: '', confirm_password: '' };
  } catch (e) {
    showError(`Failed to change password: ${e.response?.data?.detail || e.message}`);
  } finally {
    loading.value = false;
  }
}

function showSuccess(msg) {
  isError.value = false;
  message.value = msg;
  setTimeout(() => message.value = '', 3000);
}

function showError(msg) {
  isError.value = true;
  message.value = msg;
  setTimeout(() => message.value = '', 5000);
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

const selectedUserName = computed(() => {
  const user = store.users.find(u => u.id === selectedUser.value);
  return user ? user.name : '';
});
</script>

<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="admin-panel">
      <div class="panel-header">
        <div class="header-title">
          <svg viewBox="0 0 24 24" fill="none" style="width: 32px; height: 32px; color: var(--md-sys-color-primary);">
            <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" fill="currentColor"/>
          </svg>
          <h2>Admin Panel</h2>
        </div>
        <button class="close-btn" @click="$emit('close')" :disabled="loading">
          <svg viewBox="0 0 24 24" fill="none" style="width: 24px; height: 24px;">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill="currentColor"/>
          </svg>
        </button>
      </div>

      <div class="success-msg" v-if="message && !isError">
        ✓ {{ message }}
      </div>
      <div class="error-msg" v-if="message && isError">
        ⚠ {{ message }}
      </div>

      <div class="tabs">
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'rides' }"
          @click="activeTab = 'rides'"
        >
          <svg viewBox="0 0 24 24" fill="none" style="width: 20px; height: 20px;">
            <path d="M23 8c0 1.1-.9 2-2 2-.18 0-.35-.02-.51-.07l-3.56 3.55c.05.16.07.34.07.52 0 1.1-.9 2-2 2s-2-.9-2-2c0-.18.02-.36.07-.52l-2.55-2.55c-.16.05-.34.07-.52.07s-.36-.02-.52-.07l-4.55 4.56c.05.16.07.33.07.51 0 1.1-.9 2-2 2s-2-.9-2-2 .9-2 2-2c.18 0 .35.02.51.07l4.56-4.55C8.02 9.36 8 9.18 8 9c0-1.1.9-2 2-2s2 .9 2 2c0 .18-.02.36-.07.52l2.55 2.55c.16-.05.34-.07.52-.07s.36.02.52.07l3.55-3.56C19.02 8.35 19 8.18 19 8c0-1.1.9-2 2-2s2 .9 2 2z" fill="currentColor"/>
          </svg>
          Manage Rides
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'password' }"
          @click="activeTab = 'password'"
        >
          <svg viewBox="0 0 24 24" fill="none" style="width: 20px; height: 20px;">
            <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z" fill="currentColor"/>
          </svg>
          Change Password
        </button>
      </div>

      <div class="panel-body">
        <!-- Rides Management Tab -->
        <div v-if="activeTab === 'rides'" class="tab-content">
          <div class="form-section">
            <label>Select Driver</label>
            <select v-model="selectedUser" @change="loadUserRides" :disabled="loading">
              <option v-for="user in store.users" :key="user.id" :value="user.id">
                {{ user.name }}
              </option>
            </select>
          </div>

          <div v-if="loading" class="loading-state">
            <p>Loading rides...</p>
          </div>

          <div v-else-if="rides.length === 0" class="empty-state">
            <svg viewBox="0 0 24 24" fill="none" style="width: 48px; height: 48px; color: var(--md-sys-color-on-surface-variant); opacity: 0.5;">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z" fill="currentColor"/>
            </svg>
            <p>No rides found for {{ selectedUserName }} in the current tank cycle</p>
          </div>

          <div v-else class="rides-list">
            <h4>Rides for {{ selectedUserName }} (Current Cycle)</h4>
            <div v-for="ride in rides" :key="ride.id" class="ride-card">
              <div class="ride-header">
                <span class="ride-date">{{ formatDate(ride.timestamp) }}</span>
                <span class="ride-id">#{{ ride.id }}</span>
              </div>

              <div v-if="editingRide === ride.id" class="ride-edit-form">
                <div class="edit-fields">
                  <div class="edit-field">
                    <label>Distance (km)</label>
                    <input type="number" step="0.1" v-model.number="editForm.distance_km" min="0" @input="onFieldChange">
                  </div>
                  <div class="edit-field">
                    <label>Consumption (L/100km)</label>
                    <input type="number" step="0.1" v-model.number="editForm.consumption_l100km" min="0" @input="onFieldChange">
                  </div>
                  <div class="edit-field">
                    <label>Fuel (L)</label>
                    <input type="number" step="0.1" v-model.number="editForm.fuel_liters" min="0" @input="onFieldChange">
                  </div>
                </div>
                <div class="edit-actions">
                  <button class="btn-small btn-secondary" @click="cancelEdit" :disabled="loading">
                    Cancel
                  </button>
                  <button class="btn-small" @click="saveEdit(ride.id)" :disabled="loading">
                    Save
                  </button>
                </div>
              </div>

              <div v-else class="ride-details">
                <div class="ride-stat">
                  <span class="stat-label">Distance</span>
                  <span class="stat-value">{{ ride.distance_km }} km</span>
                </div>
                <div class="ride-stat">
                  <span class="stat-label">Consumption</span>
                  <span class="stat-value">{{ ride.consumption_l100km }} L/100km</span>
                </div>
                <div class="ride-stat">
                  <span class="stat-label">Fuel</span>
                  <span class="stat-value">{{ ride.fuel_liters }} L</span>
                </div>
                <div class="ride-actions">
                  <button class="btn-small" @click="startEdit(ride)" :disabled="loading">
                    <svg viewBox="0 0 24 24" fill="none" style="width: 16px; height: 16px;">
                      <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="currentColor"/>
                    </svg>
                    Edit
                  </button>
                  <button class="btn-small btn-danger" @click="deleteRide(ride.id)" :disabled="loading">
                    <svg viewBox="0 0 24 24" fill="none" style="width: 16px; height: 16px;">
                      <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" fill="currentColor"/>
                    </svg>
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Password Change Tab -->
        <div v-if="activeTab === 'password'" class="tab-content">
          <div class="form-section">
            <label>Current Password</label>
            <input
              type="password"
              v-model="passwordForm.old_password"
              placeholder="Enter current password"
              :disabled="loading"
            >
          </div>

          <div class="form-section">
            <label>New Password</label>
            <input
              type="password"
              v-model="passwordForm.new_password"
              placeholder="Enter new password"
              :disabled="loading"
            >
          </div>

          <div class="form-section">
            <label>Confirm New Password</label>
            <input
              type="password"
              v-model="passwordForm.confirm_password"
              placeholder="Confirm new password"
              :disabled="loading"
            >
          </div>

          <button 
            @click="changePassword" 
            :disabled="loading || !passwordForm.old_password || !passwordForm.new_password || !passwordForm.confirm_password"
          >
            <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px; margin-right: 8px;">
              <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" fill="currentColor"/>
            </svg>
            Change Password
          </button>
        </div>
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
  overflow-y: auto;
  padding: var(--md-spacing-lg);
}

.admin-panel {
  background: var(--md-sys-color-surface-container);
  border-radius: var(--md-shape-corner-large);
  box-shadow: var(--md-elevation-3);
  border: 1px solid var(--md-sys-color-outline);
  max-width: 900px;
  width: 100%;
  animation: slideUp 0.3s ease;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--md-spacing-lg);
  border-bottom: 1px solid var(--md-sys-color-outline-variant);
}

.header-title {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-md);
}

.header-title h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 500;
}

.close-btn {
  width: auto;
  padding: var(--md-spacing-sm);
  background: transparent;
  color: var(--md-sys-color-on-surface);
  min-width: auto;
}

.close-btn:hover:not(:disabled) {
  background: var(--md-sys-color-surface-container-highest);
}

.tabs {
  display: flex;
  padding: var(--md-spacing-md) var(--md-spacing-lg);
  gap: var(--md-spacing-xs);
  background: var(--md-sys-color-surface-container-low);
  border-bottom: 1px solid var(--md-sys-color-outline-variant);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-sm);
  padding: var(--md-spacing-sm) var(--md-spacing-md);
  border-radius: var(--md-shape-corner-large);
  color: var(--md-sys-color-on-surface-variant);
  background: transparent;
  border: none;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  min-width: auto;
  width: auto;
}

.tab-btn:hover:not(.active) {
  background: var(--md-sys-color-surface-container-highest);
  color: var(--md-sys-color-on-surface);
}

.tab-btn.active {
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-primary);
}

.tab-btn.active:hover {
  background: var(--md-sys-color-primary-container);
}

.panel-body {
  padding: var(--md-spacing-lg);
  overflow-y: auto;
  flex: 1;
}

.tab-content {
  animation: fadeIn 0.2s ease;
}

.loading-state, .empty-state {
  text-align: center;
  padding: var(--md-spacing-xl);
  color: var(--md-sys-color-on-surface-variant);
}

.rides-list h4 {
  margin-bottom: var(--md-spacing-lg);
  color: var(--md-sys-color-on-surface);
}

.ride-card {
  background: var(--md-sys-color-surface-container-high);
  border-radius: var(--md-shape-corner-medium);
  padding: var(--md-spacing-md);
  margin-bottom: var(--md-spacing-md);
  border: 1px solid var(--md-sys-color-outline-variant);
}

.ride-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--md-spacing-md);
  padding-bottom: var(--md-spacing-sm);
  border-bottom: 1px solid var(--md-sys-color-outline-variant);
}

.ride-date {
  font-weight: 500;
  color: var(--md-sys-color-on-surface);
}

.ride-id {
  font-size: 0.875rem;
  color: var(--md-sys-color-on-surface-variant);
  font-family: 'Courier New', monospace;
}

.ride-details {
  display: flex;
  flex-direction: column;
  gap: var(--md-spacing-md);
}

.ride-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.875rem;
}

.stat-value {
  font-weight: 600;
  color: var(--md-sys-color-on-surface);
}

.ride-actions {
  display: flex;
  gap: var(--md-spacing-sm);
  margin-top: var(--md-spacing-sm);
  padding-top: var(--md-spacing-sm);
  border-top: 1px solid var(--md-sys-color-outline-variant);
}

.ride-edit-form {
  display: flex;
  flex-direction: column;
  gap: var(--md-spacing-md);
}

.edit-fields {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--md-spacing-md);
}

.edit-field label {
  display: block;
  margin-bottom: var(--md-spacing-xs);
  font-size: 0.875rem;
  color: var(--md-sys-color-on-surface-variant);
}

.edit-field input {
  width: 100%;
}

.edit-actions {
  display: flex;
  gap: var(--md-spacing-sm);
  justify-content: flex-end;
}

.btn-small {
  width: auto;
  padding: 8px 16px;
  font-size: 0.875rem;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  min-width: auto;
}

.btn-secondary {
  background: var(--md-sys-color-surface-container-highest);
  color: var(--md-sys-color-on-surface);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--md-sys-color-surface-container-high);
}

.btn-danger {
  background: var(--md-sys-color-error);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: var(--md-sys-color-error-container);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
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
</style>
