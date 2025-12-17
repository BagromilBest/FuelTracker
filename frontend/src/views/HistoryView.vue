<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const api = axios.create({ baseURL: '/api' });
const cycles = ref([]);
const selectedCycle = ref(null);
const stats = ref(null);
const error = ref('');

onMounted(async () => {
  try {
    const response = await api.get('/cycles');
    cycles.value = response.data;
  } catch (e) {
    error.value = `Failed to load cycles: ${e.response?.data?.detail || e.message}`;
  }
});

async function viewCycleStats(cycleId) {
  try {
    error.value = '';
    const response = await api.get(`/stats?cycle_id=${cycleId}`);
    stats.value = response.data;
    selectedCycle.value = cycles.value.find(c => c.id === cycleId);
  } catch (e) {
    error.value = `Failed to load stats: ${e.response?.data?.detail || e.message}`;
  }
}
</script>

<template>
  <div class="container">
    <h1>History</h1>
    
    <div class="error-msg" v-if="error">{{ error }}</div>
    
    <div class="card">
      <h3>Past Tank Cycles</h3>
      <table v-if="cycles.length > 0">
        <thead>
          <tr>
            <th>Cycle ID</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cycle in cycles" :key="cycle.id">
            <td>{{ cycle.id }}</td>
            <td>{{ new Date(cycle.start_date).toLocaleString() }}</td>
            <td>{{ cycle.end_date ? new Date(cycle.end_date).toLocaleString() : 'N/A' }}</td>
            <td>{{ cycle.is_active ? 'Active' : 'Closed' }}</td>
            <td>
              <button @click="viewCycleStats(cycle.id)">View Stats</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No cycles found.</p>
    </div>

    <div class="card" v-if="stats && selectedCycle">
      <h3>Stats for Cycle #{{ selectedCycle.id }}</h3>
      <p><strong>Period:</strong> {{ new Date(selectedCycle.start_date).toLocaleDateString() }} - 
         {{ selectedCycle.end_date ? new Date(selectedCycle.end_date).toLocaleDateString() : 'Ongoing' }}</p>
      <p><strong>Total Distance:</strong> {{ stats.total_distance }} km</p>
      <p><strong>Total Fuel:</strong> {{ stats.total_fuel }} L</p>
      <p><strong>Total Cost:</strong> {{ stats.total_cost }} CZK</p>

      <h4>User Breakdown</h4>
      <table v-if="stats.user_stats.length > 0">
        <thead>
          <tr>
            <th>User</th>
            <th>Distance (km)</th>
            <th>Fuel (L)</th>
            <th>Cost</th>
            <th>Avg Consumption</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in stats.user_stats" :key="u.user_id">
            <td :style="{ color: u.user_color }">{{ u.user_name }}</td>
            <td>{{ u.total_distance }}</td>
            <td>{{ u.total_fuel }}</td>
            <td>{{ u.total_cost }}</td>
            <td>{{ u.avg_consumption }} L/100km</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No rides in this cycle.</p>
    </div>
  </div>
</template>
