import { defineStore } from 'pinia'
import axios from 'axios'

const api = axios.create({ baseURL: '/api' });

export const useAppStore = defineStore('app', {
  state: () => ({
    users: [],
    settings: { currency: 'CZK', fuel_price: 0 },
    currentStats: null,
    historyCycles: [],
    isAuthenticated: false,
    currentUser: null,
    isAdmin: false,
    authToken: null
  }),
  getters: {
    availableDrivers: (state) => {
      if (state.isAdmin) {
        return state.users;
      }
      return state.currentUser ? state.users.filter(u => u.id === state.currentUser.id) : [];
    }
  },
  actions: {
    setAuthHeader() {
      if (this.authToken) {
        api.defaults.headers.common['Authorization'] = `Bearer ${this.authToken}`;
      } else {
        delete api.defaults.headers.common['Authorization'];
      }
    },
    
    async fetchUsers() {
      const response = await api.get('/users');
      this.users = response.data;
    },
    
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
    
    async userLogin(userId, password) {
      const response = await api.post('/users/login', { user_id: userId, password });
      this.authToken = response.data.access_token;
      this.isAuthenticated = true;
      this.isAdmin = response.data.is_admin;
      this.currentUser = {
        id: response.data.user_id,
        name: response.data.user_name
      };
      this.setAuthHeader();
      
      // Store in localStorage for persistence
      localStorage.setItem('authToken', this.authToken);
      localStorage.setItem('userId', response.data.user_id);
      localStorage.setItem('userName', response.data.user_name);
      localStorage.setItem('isAdmin', response.data.is_admin);
      
      return response.data;
    },
    
    async adminLogin(password) {
      const response = await api.post('/admin/login', { password });
      this.authToken = response.data.access_token;
      this.isAuthenticated = true;
      this.isAdmin = true;
      this.currentUser = {
        id: 0,
        name: 'Admin'
      };
      this.setAuthHeader();
      
      // Store in localStorage for persistence
      localStorage.setItem('authToken', this.authToken);
      localStorage.setItem('userId', 0);
      localStorage.setItem('userName', 'Admin');
      localStorage.setItem('isAdmin', 'true');
      
      return response.data;
    },
    
    logout() {
      this.authToken = null;
      this.isAuthenticated = false;
      this.isAdmin = false;
      this.currentUser = null;
      this.setAuthHeader();
      
      // Clear localStorage
      localStorage.removeItem('authToken');
      localStorage.removeItem('userId');
      localStorage.removeItem('userName');
      localStorage.removeItem('isAdmin');
    },
    
    restoreAuth() {
      const token = localStorage.getItem('authToken');
      const userId = localStorage.getItem('userId');
      const userName = localStorage.getItem('userName');
      const isAdmin = localStorage.getItem('isAdmin') === 'true';
      
      if (token && userId && userName) {
        this.authToken = token;
        this.isAuthenticated = true;
        this.isAdmin = isAdmin;
        this.currentUser = {
          id: parseInt(userId),
          name: userName
        };
        this.setAuthHeader();
      }
    },
    
    async addRide(payload) {
      await api.post('/rides', payload);
      await this.fetchInit(); // refresh stats
    },
    async closeCycle() {
      await api.post('/cycles/close');
      await this.fetchInit();
    },
    async addUser(name, color, password) {
        await api.post('/users', {name, color, password});
        await this.fetchInit();
    },
    getAdminHeaders() {
      return {
        Authorization: `Bearer ${this.authToken}`
      };
    }
  }
})