<script setup>
import { computed } from 'vue';
import { useAppStore } from '../stores/app';
import RideForm from '../components/RideForm.vue';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { Pie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const store = useAppStore();

const pieData = computed(() => {
    if (!store.currentStats) return null;
    return {
        labels: store.currentStats.user_stats.map(u => u.user_name),
        datasets: [{
            data: store.currentStats.user_stats.map(u => u.total_fuel),
            backgroundColor: store.currentStats.user_stats.map(u => u.user_color),
            borderWidth: 0
        }]
    }
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#E6E8EB',
        padding: 15,
        font: {
          size: 12,
          family: 'Roboto'
        }
      }
    },
    tooltip: {
      backgroundColor: '#1E242F',
      titleColor: '#E6E8EB',
      bodyColor: '#B8BCC2',
      borderColor: '#3D444F',
      borderWidth: 1,
      padding: 12,
      displayColors: true,
      callbacks: {
        label: function(context) {
          return context.label + ': ' + context.parsed + ' L';
        }
      }
    }
  }
};
</script>

<template>
  <div class="container slide-in">
    <div class="page-header">
      <h1>
        <svg viewBox="0 0 24 24" fill="none" style="width: 40px; height: 40px;">
          <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z" fill="currentColor"/>
        </svg>
        Dashboard
      </h1>
    </div>

    <div class="row">
        <div class="col"><RideForm /></div>

        <div class="col" v-if="store.currentStats">
          <div class="card stats-overview">
            <div class="card-header">
              <svg viewBox="0 0 24 24" fill="none" style="width: 24px; height: 24px; color: var(--md-sys-color-primary);">
                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" fill="currentColor"/>
              </svg>
              <h3>Current Cycle Stats</h3>
            </div>
            
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-label">Total Distance</div>
                <div class="stat-value">{{ store.currentStats.total_distance }}</div>
                <div class="stat-unit">kilometers</div>
              </div>
              
              <div class="stat-card" style="border-left-color: var(--md-sys-color-secondary);">
                <div class="stat-label">Total Fuel</div>
                <div class="stat-value">{{ store.currentStats.total_fuel }}</div>
                <div class="stat-unit">liters</div>
              </div>
              
              <div class="stat-card" style="border-left-color: var(--md-sys-color-tertiary);">
                <div class="stat-label">Total Cost</div>
                <div class="stat-value">{{ store.currentStats.total_cost }}</div>
                <div class="stat-unit">{{ store.settings.currency }}</div>
              </div>
            </div>
            
            <button class="secondary" @click="store.closeCycle">
              <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px; margin-right: 8px;">
                <path d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z" fill="currentColor"/>
              </svg>
              Refill Tank / Close Cycle
            </button>
          </div>
        </div>
    </div>

    <div class="row" v-if="store.currentStats">
        <div class="col">
          <div class="card">
            <div class="card-header">
              <svg viewBox="0 0 24 24" fill="none" style="width: 24px; height: 24px; color: var(--md-sys-color-primary);">
                <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" fill="currentColor"/>
              </svg>
              <h3>User Breakdown</h3>
            </div>
            
            <div class="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Driver</th>
                    <th>Distance</th>
                    <th>Fuel</th>
                    <th>Cost</th>
                    <th>Consumption</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="u in store.currentStats.user_stats" :key="u.user_id">
                    <td>
                      <div class="user-cell">
                        <span class="user-color-indicator" :style="{ background: u.user_color }"></span>
                        <span class="user-name">{{ u.user_name }}</span>
                      </div>
                    </td>
                    <td><strong>{{ u.total_distance }}</strong> km</td>
                    <td><strong>{{ u.total_fuel }}</strong> L</td>
                    <td><strong>{{ u.total_cost }}</strong> {{ store.settings.currency }}</td>
                    <td><strong>{{ u.avg_consumption }}</strong> L/100km</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div class="col" v-if="pieData">
          <div class="card">
            <div class="card-header">
              <svg viewBox="0 0 24 24" fill="none" style="width: 24px; height: 24px; color: var(--md-sys-color-primary);">
                <path d="M11 2v20c-5.07-.5-9-4.79-9-10s3.93-9.5 9-10zm2.03 0v8.99H22c-.47-4.74-4.24-8.52-8.97-8.99zm0 11.01V22c4.74-.47 8.5-4.25 8.97-8.99h-8.97z" fill="currentColor"/>
              </svg>
              <h3>Fuel Consumption Share</h3>
            </div>
            <div class="chart-container">
              <Pie :data="pieData" :options="chartOptions" />
            </div>
          </div>
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

.stats-overview {
  display: flex;
  flex-direction: column;
  gap: var(--md-spacing-lg);
}

.stat-unit {
  font-size: 0.875rem;
  color: var(--md-sys-color-on-surface-variant);
  text-transform: lowercase;
  margin-top: var(--md-spacing-xs);
}

.user-cell {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-sm);
}

.user-name {
  font-weight: 500;
}

button.secondary {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>