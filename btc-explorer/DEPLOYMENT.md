# Guía de Despliegue en Render

## Configuración del Backend

1. **Crear un nuevo Web Service en Render**
   - Conectar tu repositorio de GitHub
   - Branch: `main` (o tu branch principal)
   - Root Directory: `btc-explorer/backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Variables de Entorno del Backend**
   ```
   ALLOWED_ORIGINS=https://tu-frontend.onrender.com,http://localhost:5173
   ```
   - Reemplaza `tu-frontend.onrender.com` con la URL real de tu frontend

3. **Tomar nota de la URL del backend**
   - Será algo como: `https://tu-backend-service.onrender.com`

## Configuración del Frontend

1. **Crear un nuevo Static Site en Render**
   - Conectar el mismo repositorio
   - Branch: `main` (o tu branch principal)
   - Root Directory: `btc-explorer/frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

2. **Variables de Entorno del Frontend**
   ```
   VITE_API_URL=https://tu-backend-service.onrender.com
   ```
   - Usa la URL del backend que obtuviste en el paso anterior

## Solución de Problemas

### No se ven datos de blockchain

1. **Verificar que el backend esté funcionando:**
   - Visita `https://tu-backend-service.onrender.com/docs`
   - Deberías ver la documentación de FastAPI

2. **Probar la API directamente:**
   - Prueba: `https://tu-backend-service.onrender.com/api/address/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`
   - Esta es la dirección del bloque génesis de Bitcoin

3. **Verificar CORS:**
   - Asegúrate de que `ALLOWED_ORIGINS` en el backend incluya la URL de tu frontend
   - Puedes agregar temporalmente `*` para permitir todos los orígenes (solo para debugging)

4. **Revisar los logs:**
   - En el dashboard de Render, revisa los logs del backend
   - Busca errores relacionados con las llamadas a blockchain.info

### La API de blockchain.info no responde

La API pública de blockchain.info puede tener límites de rate o estar temporalmente no disponible. Si encuentras este problema:

1. **Implementar retry logic** en el backend
2. **Considerar usar una API alternativa** como:
   - BlockCypher
   - Blockstream.info
   - Tu propio nodo de Bitcoin

### Errores de CORS

Si ves errores de CORS en la consola del navegador:

1. Verifica que la URL del frontend esté en `ALLOWED_ORIGINS`
2. Asegúrate de no tener trailing slashes en las URLs
3. Si usas un dominio personalizado, agrégalo también a `ALLOWED_ORIGINS`

## Ejemplo de Configuración Completa

### Backend (.env)
```
ALLOWED_ORIGINS=https://btc-explorer-frontend.onrender.com,http://localhost:5173
```

### Frontend (.env)
```
VITE_API_URL=https://btc-explorer-backend.onrender.com
```