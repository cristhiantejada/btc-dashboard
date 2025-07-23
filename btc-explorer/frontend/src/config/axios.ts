import axios from 'axios';

// En producción, usar la URL del backend desplegado en Render
// En desarrollo, el proxy de Vite manejará las rutas /api
const baseURL = import.meta.env.PROD 
  ? import.meta.env.VITE_API_URL || 'https://your-backend-url.onrender.com'
  : '';

const axiosInstance = axios.create({
  baseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejar errores
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default axiosInstance;