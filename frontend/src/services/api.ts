import axios, { AxiosInstance, AxiosError } from 'axios';

// Configurar instância Axios com baseURL
const api: AxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para logging de requisições
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API] Erro na requisição:', error);
    return Promise.reject(error);
  }
);

// Interceptor para logging de respostas
api.interceptors.response.use(
  (response) => {
    console.log(`[API] Resposta: ${response.status} ${response.statusText}`);
    return response;
  },
  (error: AxiosError) => {
    console.error('[API] Erro na resposta:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

export default api;
