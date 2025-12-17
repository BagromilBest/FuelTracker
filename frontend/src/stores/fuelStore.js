// Alternative store implementation with more explicit method names
// The main application uses app.js for simplicity, but this store provides
// a more modular approach if you want to refactor the application later
// Note: DashboardView uses app.js store, so choose one and stick with it
import { defineStore } from 'pinia'
import api from '../services/api'

export const useFuelStore = defineStore('fuel', {
  state: () => ({
    users: [],
    settings: { currency: 'CZK', fuel_price: 35.5 },
    currentStats: null,
    cycles: []
  }),
  actions: {
    async initialize() {
      await this.fetchUsers()
      await this.fetchSettings()
      await this.fetchCurrentStats()
    },
    async fetchUsers() {
      const response = await api.get('/users')
      this.users = response.data
    },
    async fetchSettings() {
      const response = await api.get('/settings')
      this.settings = response.data
    },
    async fetchCurrentStats() {
      const response = await api.get('/stats')
      this.currentStats = response.data
    },
    async fetchCycles() {
      const response = await api.get('/cycles')
      this.cycles = response.data
    },
    async addRide(rideData) {
      await api.post('/rides', rideData)
      await this.fetchCurrentStats()
    },
    async closeCycle() {
      await api.post('/cycles/close')
      await this.initialize()
    },
    async createUser(userData) {
      await api.post('/users', userData)
      await this.fetchUsers()
    },
    async updateSettings(settingsData) {
      const response = await api.put('/settings', settingsData)
      this.settings = response.data
    }
  }
})
