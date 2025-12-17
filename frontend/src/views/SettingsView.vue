<script setup>
import { ref, onMounted } from 'vue';
import { useAppStore } from '../stores/app';

const store = useAppStore();
const settingsForm = ref({ currency: 'CZK', fuel_price: 35.5 });
const userForm = ref({ name: '', color: '#3498db' });
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
    userForm.value = { name: '', color: '#3498db' };
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
  <div class="container">
    <h1>Settings</h1>

    <div class="card">
      <h3>General Settings</h3>
      <p v-if="message" :class="isError ? 'error-msg' : 'success-msg'">{{ message }}</p>
      
      <label>Currency</label>
      <input type="text" v-model="settingsForm.currency" placeholder="e.g., CZK, USD">
      
      <label>Fuel Price per Liter</label>
      <input type="number" step="0.1" v-model.number="settingsForm.fuel_price" placeholder="35.50">
      
      <button @click="updateSettings">Save Settings</button>
    </div>

    <div class="card">
      <h3>Manage Users</h3>
      
      <div v-if="store.users.length > 0">
        <h4>Current Users</h4>
        <div v-for="user in store.users" :key="user.id" style="display: flex; align-items: center; gap: 10px; margin: 10px 0;">
          <span :style="{ width: '20px', height: '20px', background: user.color, borderRadius: '50%' }"></span>
          <span>{{ user.name }}</span>
        </div>
      </div>

      <h4 style="margin-top: 20px;">Add New User</h4>
      <label>Name</label>
      <input type="text" v-model="userForm.name" placeholder="User Name">
      
      <label>Color</label>
      <input type="color" v-model="userForm.color">
      
      <button @click="addUser" :disabled="!userForm.name">Add User</button>
    </div>
  </div>
</template>
