import { defineStore } from 'pinia'
import axios from 'axios'

const api = axios.create({ baseURL: '/api' });

export const useAppStore = defineStore('app', {
  state: () => ({
    users: [],
    settings: { currency: 'CZK', fuel_price: 0 },
    currentStats: null,
    historyCycles: [],
    isAdminAuthenticated: false,
    adminToken: null
  }),
  actions: {
    async fetchInit() {
      const [u, s, cs] = await Promise.all([
        api.get('/users'),
        api.get('/settings'),
        api.get('/stats')
      ]);
      this.users = u.data;
      this.settings = s.data;
      this.currentStats = cs.data;
    },
    async addRide(payload) {
      await api.post('/rides', payload);
      await this.fetchInit(); // refresh stats
    },
    async closeCycle() {
      await api.post('/cycles/close');
      await this.fetchInit();
    },
    async addUser(name, color) {
        await api.post('/users', {name, color});
        await this.fetchInit();
    },
    async adminLogin(password) {
      const response = await api.post('/admin/login', { password });
      this.adminToken = response.data.access_token;
      this.isAdminAuthenticated = true;
      return response.data;
    },
    adminLogout() {
      this.adminToken = null;
      this.isAdminAuthenticated = false;
    },
    getAdminHeaders() {
      return {
        Authorization: `Bearer ${this.adminToken}`
      };
    }
  }
})