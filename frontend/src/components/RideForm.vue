<script setup>
import { ref, computed } from 'vue';
import { useAppStore } from '../stores/app';

const store = useAppStore();

function getLocalDatetimeString() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  return `${day}.${month}.${year} ${hours}:${minutes}`;
}

function parseDisplayDatetime(displayStr) {
  const match = displayStr.match(/^(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}):(\d{2})$/);
  if (!match) return new Date().toISOString();
  const [, day, month, year, hours, minutes] = match;
  return new Date(year, month - 1, day, hours, minutes).toISOString();
}

const form = ref({
  user_id: '', timestamp: getLocalDatetimeString(),
  distance_km: '', consumption_l100km: '', fuel_liters: ''
});
const error = ref('');
const success = ref(false);

const canSubmit = computed(() => {
    const filled = [form.value.distance_km, form.value.consumption_l100km, form.value.fuel_liters].filter(x => x !== '').length;
    return form.value.user_id && filled >= 2;
});

async function submit() {
  try {
    error.value = '';
    success.value = false;
    const payload = { ...form.value };
    payload.timestamp = parseDisplayDatetime(form.value.timestamp);
    // Convert empty strings to null for backend logic
    if (payload.distance_km === '') payload.distance_km = null;
    if (payload.consumption_l100km === '') payload.consumption_l100km = null;
    if (payload.fuel_liters === '') payload.fuel_liters = null;

    await store.addRide(payload);
    // Reset numeric fields and update timestamp to current time
    form.value.distance_km = '';
    form.value.consumption_l100km = '';
    form.value.fuel_liters = '';
    form.value.timestamp = getLocalDatetimeString();
    
    success.value = true;
    setTimeout(() => success.value = false, 3000);
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error submitting ride';
  }
}
</script>

<template>
  <div class="card ride-form">
    <div class="form-header">
      <svg class="form-icon" viewBox="0 0 24 24" fill="none">
        <path d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z" fill="currentColor"/>
      </svg>
      <h3>Log New Ride</h3>
    </div>
    
    <div class="success-msg" v-if="success">
      ✓ Ride logged successfully!
    </div>
    <div class="error-msg" v-if="error">
      ⚠ {{ error }}
    </div>
    
    <div class="form-content">
      <label>Driver</label>
      <select v-model="form.user_id">
        <option disabled value="">Select User</option>
        <option v-for="u in store.users" :key="u.id" :value="u.id">
          {{ u.name }}
        </option>
      </select>
      
      <label>Date & Time</label>
      <input type="text" v-model="form.timestamp" placeholder="DD.MM.YYYY HH:mm" />

      <label>Trip Details</label>
      <div class="form-info">
        <small>Enter at least 2 values to auto-calculate the 3rd</small>
      </div>
      
      <div class="input-row">
        <div class="input-col">
          <div class="input-group">
            <input 
              type="number" 
              step="0.1" 
              placeholder="Distance" 
              v-model.number="form.distance_km"
            />
            <span class="input-suffix">km</span>
          </div>
        </div>
        <div class="input-col">
          <div class="input-group">
            <input 
              type="number" 
              step="0.1" 
              placeholder="Consumption" 
              v-model.number="form.consumption_l100km"
            />
            <span class="input-suffix">L/100km</span>
          </div>
        </div>
        <div class="input-col">
          <div class="input-group">
            <input 
              type="number" 
              step="0.1" 
              placeholder="Fuel" 
              v-model.number="form.fuel_liters"
            />
            <span class="input-suffix">L</span>
          </div>
        </div>
      </div>
      
      <button @click="submit" :disabled="!canSubmit">
        <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px; margin-right: 8px;">
          <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" fill="currentColor"/>
        </svg>
        Save Ride
      </button>
    </div>
  </div>
</template>

<style scoped>
.ride-form {
  height: 100%;
}

.form-header {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-md);
  margin-bottom: var(--md-spacing-lg);
}

.form-icon {
  width: 28px;
  height: 28px;
  color: var(--md-sys-color-primary);
}

.form-header h3 {
  margin: 0;
}

.form-content {
  display: flex;
  flex-direction: column;
}

.form-info {
  margin-bottom: var(--md-spacing-md);
  padding: var(--md-spacing-sm) var(--md-spacing-md);
  background: var(--md-sys-color-surface-container-low);
  border-radius: var(--md-shape-corner-small);
  border-left: 3px solid var(--md-sys-color-primary);
}

.input-group {
  position: relative;
}

.input-suffix {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.875rem;
  font-weight: 500;
  pointer-events: none;
  white-space: nowrap;
}

.input-group input {
  padding-right: 80px;
}

.input-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--md-spacing-lg);
  margin-bottom: var(--md-spacing-md);
}

.input-col {
  display: flex;
  flex-direction: column;
}

button {
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .input-row {
    grid-template-columns: 1fr;
  }
}
</style>