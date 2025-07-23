# Solución: No se ven datos reales de blockchain.info

## Diagnóstico

El problema de no ver datos reales en el explorador de BTC se debe a que el frontend no está conectándose correctamente al backend cuando está desplegado en producción.

## Cambios Realizados

### 1. Configuración de Axios (Frontend)

Se creó un archivo de configuración de axios que maneja las URLs de desarrollo y producción:

**Archivo:** `btc-explorer/frontend/src/config/axios.ts`

```typescript
const baseURL = import.meta.env.PROD 
  ? import.meta.env.VITE_API_URL || 'https://your-backend-url.onrender.com'
  : '';
```

### 2. Mejoras en el Backend

Se mejoró el servicio de blockchain con:
- Mejor manejo de errores
- Logging detallado
- Headers apropiados para la API
- Manejo de rate limiting

### 3. Archivos de Configuración

Se crearon archivos de ejemplo para las variables de entorno:
- `btc-explorer/frontend/.env.example`
- Guía de despliegue en `btc-explorer/DEPLOYMENT.md`

## Pasos para Configurar en Render

### Backend

1. En tu servicio backend de Render, agrega la variable de entorno:
   ```
   ALLOWED_ORIGINS=https://tu-frontend.onrender.com,http://localhost:5173
   ```

2. Verifica que el backend esté funcionando visitando:
   ```
   https://tu-backend.onrender.com/docs
   ```

### Frontend

1. En tu sitio estático de Render, agrega la variable de entorno:
   ```
   VITE_API_URL=https://tu-backend.onrender.com
   ```

2. Reconstruye el frontend después de agregar la variable.

## Verificación

Para verificar que todo está funcionando:

1. **Prueba el backend directamente:**
   ```
   https://tu-backend.onrender.com/api/address/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
   ```

2. **Revisa la consola del navegador** en el frontend para ver si hay errores de CORS o conexión.

3. **Verifica los logs del backend** en Render para ver las peticiones entrantes.

## Direcciones de Prueba

Puedes probar con estas direcciones conocidas que tienen actividad:

- `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` - Dirección del bloque génesis (Satoshi)
- `3FpYfDGJSdkMAvZvCrwPHDqdmGqUkTsJys` - Una dirección con muchas transacciones
- `bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh` - Dirección SegWit

## Nota Importante

La API pública de blockchain.info puede tener límites de rate o estar temporalmente no disponible. Si encuentras errores 429 (Too Many Requests), espera un momento antes de intentar de nuevo.