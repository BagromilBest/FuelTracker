<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import { useAppStore } from '../stores/app';

const store = useAppStore();
const cycles = ref([]);
const selectedCycle = ref(null);
const stats = ref(null);
const error = ref('');
const loading = ref(false);

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

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function clearSelection() {
  stats.value = null;
  selectedCycle.value = null;
}

async function deleteCycle(cycleId) {
  if (!confirm('Are you sure you want to delete this entire tank cycle and all its rides? This action cannot be undone.')) {
    return;
  }
  
  loading.value = true;
  try {
    await api.delete(`/admin/cycles/${cycleId}`, {
      headers: store.getAdminHeaders()
    });
    
    // Reload cycles
    const response = await api.get('/cycles');
    cycles.value = response.data;
    
    // Clear selection if deleted cycle was selected
    if (selectedCycle.value && selectedCycle.value.id === cycleId) {
      clearSelection();
    }
    
    error.value = '';
  } catch (e) {
    error.value = `Failed to delete cycle: ${e.response?.data?.detail || e.message}`;
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="container slide-in">
    <div class="page-header">
      <h1>
        <svg viewBox="0 0 24 24" fill="none" style="width: 40px; height: 40px;">
          <path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z" fill="currentColor"/>
        </svg>
        History
      </h1>
    </div>
    
    <div class="error-msg" v-if="error">⚠ {{ error }}</div>
    
    <div class="card">
      <div class="card-header">
        <svg viewBox="0 0 24 24" fill="none" style="width: 24px; height: 24px; color: var(--md-sys-color-primary);">
          <path d="M9 11H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm2-7h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11z" fill="currentColor"/>
        </svg>
        <h3>Tank Refill Cycles</h3>
      </div>
      
      <div class="table-container" v-if="cycles.length > 0">
        <table>
          <thead>
            <tr>
              <th>Cycle</th>
              <th>Started</th>
              <th>Ended</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cycle in cycles" :key="cycle.id" :class="{ 'selected-row': selectedCycle && selectedCycle.id === cycle.id }">
              <td>
                <div class="cycle-id">
                  <span class="badge">#{{ cycle.id }}</span>
                </div>
              </td>
              <td>{{ formatDate(cycle.start_date) }}</td>
              <td>{{ cycle.end_date ? formatDate(cycle.end_date) : '—' }}</td>
              <td>
                <span class="status-badge" :class="cycle.is_active ? 'status-active' : 'status-closed'">
                  {{ cycle.is_active ? 'Active' : 'Closed' }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <button 
                    class="btn-small" 
                    @click="viewCycleStats(cycle.id)"
                    :class="{ 'btn-selected': selectedCycle && selectedCycle.id === cycle.id }"
                    :disabled="loading"
                  >
                    <svg viewBox="0 0 24 24" fill="none" style="width: 16px; height: 16px;">
                      <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" fill="currentColor"/>
                    </svg>
                    View Stats
                  </button>
                  <button 
                    v-if="store.isAdminAuthenticated && !cycle.is_active"
                    class="btn-small btn-danger" 
                    @click="deleteCycle(cycle.id)"
                    :disabled="loading"
                    title="Delete cycle (Admin only)"
                  >
                    <svg viewBox="0 0 24 24" fill="none" style="width: 16px; height: 16px;">
                      <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" fill="currentColor"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" style="width: 64px; height: 64px; color: var(--md-sys-color-on-surface-variant); opacity: 0.5;">
          <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z" fill="currentColor"/>
        </svg>
        <p>No cycles found yet</p>
      </div>
    </div>

    <div class="card cycle-details" v-if="stats && selectedCycle">
      <div class="card-header">
        <svg viewBox="0 0 24 24" fill="none" style="width: 24px; height: 24px; color: var(--md-sys-color-primary);">
          <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" fill="currentColor"/>
        </svg>
        <h3>Cycle #{{ selectedCycle.id }} Details</h3>
        <button class="close-button" @click="clearSelection" style="margin-left: auto; width: auto; padding: 8px 16px;">
          <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px;">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill="currentColor"/>
          </svg>
          Close
        </button>
      </div>
      
      <div class="cycle-period">
        <svg viewBox="0 0 24 24" fill="none" style="width: 20px; height: 20px; color: var(--md-sys-color-on-surface-variant);">
          <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z" fill="currentColor"/>
        </svg>
        <span>{{ formatDate(selectedCycle.start_date) }}</span>
        <span style="color: var(--md-sys-color-on-surface-variant);">→</span>
        <span>{{ selectedCycle.end_date ? formatDate(selectedCycle.end_date) : 'Ongoing' }}</span>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Total Distance</div>
          <div class="stat-value">{{ stats.total_distance }}</div>
          <div class="stat-unit">kilometers</div>
        </div>
        
        <div class="stat-card" style="border-left-color: var(--md-sys-color-secondary);">
          <div class="stat-label">Total Fuel</div>
          <div class="stat-value">{{ stats.total_fuel }}</div>
          <div class="stat-unit">liters</div>
        </div>
        
        <div class="stat-card" style="border-left-color: var(--md-sys-color-tertiary);">
          <div class="stat-label">Total Cost</div>
          <div class="stat-value">{{ stats.total_cost }}</div>
          <div class="stat-unit">{{ store.settings?.currency || 'CZK' }}</div>
        </div>
      </div>

      <h4>Driver Breakdown</h4>
      <div class="table-container" v-if="stats.user_stats.length > 0">
        <table>
          <thead>
            <tr>
              <th>Driver</th>
              <th>Distance</th>
              <th>Fuel</th>
              <th>Cost</th>
              <th>Avg Consumption</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in stats.user_stats" :key="u.user_id">
              <td>
                <div class="user-cell">
                  <span class="user-color-indicator" :style="{ background: u.user_color }"></span>
                  <span class="user-name">{{ u.user_name }}</span>
                </div>
              </td>
              <td><strong>{{ u.total_distance }}</strong> km</td>
              <td><strong>{{ u.total_fuel }}</strong> L</td>
              <td><strong>{{ u.total_cost }}</strong> {{ store.settings?.currency || 'CZK' }}</td>
              <td><strong>{{ u.avg_consumption }}</strong> L/100km</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="empty-state">
        <p>No rides recorded in this cycle</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  margin-bottom: var(--md-spacing-xl);
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

.cycle-details {
  animation: slideIn 0.3s ease;
}

.cycle-period {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-md);
  padding: var(--md-spacing-md);
  background: var(--md-sys-color-surface-container-low);
  border-radius: var(--md-shape-corner-small);
  margin-bottom: var(--md-spacing-lg);
  font-size: 0.9rem;
}

.cycle-id {
  font-weight: 600;
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-primary);
  border-radius: var(--md-shape-corner-xlarge);
  font-size: 0.875rem;
  font-weight: 600;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: var(--md-shape-corner-xlarge);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-active {
  background: rgba(129, 199, 132, 0.2);
  color: var(--md-sys-color-secondary);
}

.status-closed {
  background: var(--md-sys-color-surface-container-highest);
  color: var(--md-sys-color-on-surface-variant);
}

.btn-small {
  width: auto;
  padding: 8px 16px;
  font-size: 0.8rem;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0;
}

.btn-selected {
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-primary);
}

.selected-row {
  background: var(--md-sys-color-surface-container-high);
}

.user-cell {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-sm);
}

.user-name {
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: var(--md-spacing-xl);
  color: var(--md-sys-color-on-surface-variant);
}

.empty-state p {
  margin-top: var(--md-spacing-md);
  font-size: 1rem;
}

.stat-unit {
  font-size: 0.875rem;
  color: var(--md-sys-color-on-surface-variant);
  text-transform: lowercase;
  margin-top: var(--md-spacing-xs);
}

.close-button {
  border-radius: var(--md-shape-corner-small);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.action-buttons {
  display: flex;
  gap: var(--md-spacing-sm);
  align-items: center;
}

.btn-danger {
  background: var(--md-sys-color-error);
  color: white;
  padding: 8px;
  min-width: auto;
}

.btn-danger:hover:not(:disabled) {
  background: var(--md-sys-color-error-container);
}
</style>
