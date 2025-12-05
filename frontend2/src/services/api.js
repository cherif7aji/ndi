import axios from 'axios';
import { API_BASE_URL } from '../config';

// Configuration de base pour l'API

// Instance Axios avec configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 secondes
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token JWT aux requêtes
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les réponses et erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expiré ou invalide
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Services API
export const AuthService = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData), // userData = {username, password}
  getCurrentUser: () => api.get('/auth/me'),
  refreshToken: () => api.post('/auth/refresh'),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  }
};

export const CoursService = {
  getAll: () => api.get('/cours'),
  getById: (id) => api.get(`/cours/${id}`),
  create: (data) => api.post('/cours', data),
  update: (id, data) => api.put(`/cours/${id}`, data),
  delete: (id) => api.delete(`/cours/${id}`),
  // with-content helpers
  getAllWithContent: () => api.get('/cours/content/all'),
  getWithContent: (id) => api.get(`/cours/${id}/with-content`),
  createWithContent: (data) => api.post('/cours/with-content', data),
  updateWithContent: (id, data) => api.put(`/cours/${id}/with-content`, data),
  deleteWithContent: (id) => api.delete(`/cours/${id}/with-content`)
};

export const ExerciceService = {
  getAll: () => api.get('/exercices/'),
  getById: (id) => api.get(`/exercices/${id}`),
  getByCours: (coursId) => api.get(`/cours/${coursId}/exercices/`),
  create: (data) => api.post('/exercices/', data),
  update: (id, data) => api.put(`/exercices/${id}`, data),
  delete: (id) => api.delete(`/exercices/${id}`),
  // with-content helpers
  getAllWithContent: () => api.get('/exercices/content/all'),
  getWithContent: (id) => api.get(`/exercices/${id}/with-content`),
  createWithContent: (data) => api.post('/exercices/with-content', data),
  updateWithContent: (id, data) => api.put(`/exercices/${id}/with-content`, data),
  deleteWithContent: (id) => api.delete(`/exercices/${id}/with-content`)
};

export const UserService = {
  getAll: () => api.get('/users'),
  getById: (id) => api.get(`/users/${id}`),
  update: (id, data) => api.put(`/users/${id}`, data),
  delete: (id) => api.delete(`/users/${id}`)
};

export const SubmissionService = {
  submit: (data) => api.post('/submissions/exercice', data),
  getMesNotes: () => api.get('/submissions/mes-notes'),
  getNoteExercice: (exerciceId) => api.get(`/submissions/exercice/${exerciceId}/note`)
};

export default api;
