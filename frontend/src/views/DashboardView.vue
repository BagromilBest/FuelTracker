<script setup>
import { computed } from 'vue';
import { useAppStore } from '../stores/app';
import RideForm from '../components/RideForm.vue';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { Pie, Bar } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const store = useAppStore();

const pieData = computed(() => {
    if (!store.currentStats) return null;
    return {
        labels: store.currentStats.user_stats.map(u => u.user_name),
        datasets: [{
            data: store.currentStats.user_stats.map(u => u.total_fuel),
            backgroundColor: store.currentStats.user_stats.map(u => u.user_color)
        }]
    }
});
</script>

<template>
  <div class="container">
    <h1>Dashboard</h1>

    <div class="row">
        <div class="col"><RideForm /></div>

        <div class="col card" v-if="store.currentStats">
            <h3>Current Cycle Stats</h3>
            <p>Total Dist: <strong>{{ store.currentStats.total_distance }} km</strong></p>
            <p>Total Fuel: <strong>{{ store.currentStats.total_fuel }} L</strong></p>
            <p>Total Cost: <strong>{{ store.currentStats.total_cost }} {{ store.settings.currency }}</strong></p>
            <button class="secondary" @click="store.closeCycle">Refill Tank / Close Cycle</button>
        </div>
    </div>

    <div class="card" v-if="store.currentStats">
        <h3>User Breakdown</h3>
        <table>
            <thead>
                <tr><th>User</th><th>Dist (km)</th><th>Fuel (L)</th><th>Cost</th></tr>
            </thead>
            <tbody>
                <tr v-for="u in store.currentStats.user_stats" :key="u.user_id">
                    <td :style="{ color: u.user_color }">{{ u.user_name }}</td>
                    <td>{{ u.total_distance }}</td>
                    <td>{{ u.total_fuel }}</td>
                    <td>{{ u.total_cost }}</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="row" v-if="pieData">
        <div class="col card chart-container">
            <h3>Consumption Share</h3>
            <Pie :data="pieData" :options="{responsive: true, maintainAspectRatio: false}" />
        </div>
    </div>
  </div>
</template>