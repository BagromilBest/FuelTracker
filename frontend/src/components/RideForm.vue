<script setup>
import { ref, computed } from 'vue';
import { useAppStore } from '../stores/app';

const store = useAppStore();
const form = ref({
  user_id: '', timestamp: new Date().toISOString().slice(0, 16),
  distance_km: '', consumption_l100km: '', fuel_liters: ''
});
const error = ref('');

const canSubmit = computed(() => {
    const filled = [form.value.distance_km, form.value.consumption_l100km, form.value.fuel_liters].filter(x => x !== '').length;
    return form.value.user_id && filled >= 2;
});

async function submit() {
  try {
    error.value = '';
    const payload = { ...form.value };
    // Convert empty strings to null for backend logic
    if (payload.distance_km === '') payload.distance_km = null;
    if (payload.consumption_l100km === '') payload.consumption_l100km = null;
    if (payload.fuel_liters === '') payload.fuel_liters = null;

    await store.addRide(payload);
    // Reset numeric fields
    form.value.distance_km = '';
    form.value.consumption_l100km = '';
    form.value.fuel_liters = '';
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error submitting ride';
  }
}
</script>

<template>
  <div class="card">
    <h3>Log Ride</h3>
    <div class="error-msg" v-if="error">{{ error }}</div>
    <select v-model="form.user_id">
      <option disabled value="">Select User</option>
      <option v-for="u in store.users" :key="u.id" :value="u.id">{{ u.name }}</option>
    </select>
    <input type="datetime-local" v-model="form.timestamp" />

    <div class="row">
        <div class="col"><input type="number" step="0.1" placeholder="Distance (km)" v-model.number="form.distance_km"></div>
        <div class="col"><input type="number" step="0.1" placeholder="L/100km" v-model.number="form.consumption_l100km"></div>
        <div class="col"><input type="number" step="0.1" placeholder="Fuel (L)" v-model.number="form.fuel_liters"></div>
    </div>
    <small style="color: #888">Enter at least 2 values to auto-calculate the 3rd.</small>
    <button @click="submit" :disabled="!canSubmit" style="margin-top: 10px">Save Ride</button>
  </div>
</template>