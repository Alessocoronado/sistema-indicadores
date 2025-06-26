// 🔧 CONFIGURACIÓN FLEXIBLE DE ENTORNOS
const ENV_CONFIG = {
  development: {
    hostnames: ['localhost', '127.0.0.1'],
    backendUrl: 'http://localhost:8000',
    protocol: 'http'
  },
  production: {
    backendUrl: import.meta.env.VITE_API_URL,
    protocol: 'https',
    enforceHttps: true
  }
};

// 🔍 DETECCIÓN AUTOMÁTICA DE BACKEND URL
function detectBackendUrl() {
  const currentDomain = window.location.hostname;
  
  // Solo para desarrollo local
  if (currentDomain.includes('localhost')) {
    return ENV_CONFIG.development.backendUrl;
  }
  
  // En producción, siempre usar HTTPS
  return ENV_CONFIG.production.backendUrl;
}

/* ================================================================
   🚀 DETECCIÓN INTELIGENTE DE ENTORNO
   ================================================================ */
function detectEnvironment() {
  const hostname = window.location.hostname;
  
  // ✅ Desarrollo local
  if (ENV_CONFIG.development.hostnames.includes(hostname)) {
    console.log('🔧 [API] Entorno: DESARROLLO LOCAL');
    return {
      env: 'development',
      baseUrl: ENV_CONFIG.development.backendUrl,
      protocol: ENV_CONFIG.development.protocol
    };
  }
  
  // ✅ Producción (Railway)
  console.log('🚀 [API] Entorno: PRODUCCIÓN');
  const backendUrl = detectBackendUrl();
  console.log('✅ [API] URL del backend:', backendUrl);
  
  return {
    env: 'production',
    baseUrl: backendUrl,
    protocol: 'https'
  };
}

// 🌍 Configuración global
const API_CONFIG = detectEnvironment();
const BASE_URL = API_CONFIG.baseUrl;

console.log(`✅ [API] Configuración final: ${BASE_URL}`);

/* ================================================================
   🛡️ WRAPPER FETCH CON PROTECCIÓN MIXED CONTENT
   ================================================================ */
async function secureApiCall(endpoint, options = {}) {
  const fullUrl = `${BASE_URL}${endpoint}`;
  
  console.log(`📡 [API] Request: ${options.method || 'GET'} ${fullUrl}`);
  
  try {
    const defaultHeaders = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
      'Cache-Control': 'no-cache'
    };
    
    const response = await fetch(fullUrl, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...(options.headers || {})
      },
      mode: 'cors',
      credentials: 'omit',
      cache: 'no-cache'
    });
    
    if (!response.ok) {
      const errorBody = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorBody}`);
    }
    
    const data = await response.json();
    console.log(`✅ [API] Success:`, data);
    return { data, response };
    
  } catch (error) {
    console.error(`❌ [API] Error en ${endpoint}:`, error);
    throw error;
  }
}

/* ================================================================
   📋 API ENDPOINTS - SISTEMA DE INDICADORES
   ================================================================ */
export const indicadoresApi = {
  // 📊 GET /api/indicadores - Obtener todos los indicadores
  getIndicadores: async () => {
    const result = await secureApiCall('/api/indicadores');
    return result.data;
  },

  // 🏢 GET /api/indicadores/area/:area - Indicadores por área
  getIndicadoresByArea: async (area) => {
    const encodedArea = encodeURIComponent(area);
    const result = await secureApiCall(`/api/indicadores/area/${encodedArea}`);
    return result.data;
  },

  // 🔍 GET /api/indicadores/:id - Indicador específico
  getIndicador: async (id) => {
    const result = await secureApiCall(`/api/indicadores/${id}`);
    return result.data;
  },

  // ➕ POST /api/indicadores - Crear indicador
  createIndicador: async (data) => {
    const result = await secureApiCall('/api/indicadores', {
      method: 'POST',
      body: JSON.stringify(data)
    });
    return result.data;
  },

  // ✏️ PUT /api/indicadores/:id - Actualizar indicador
  updateIndicador: async (id, data) => {
    const result = await secureApiCall(`/api/indicadores/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
    return result.data;
  },

  // 🗑️ DELETE /api/indicadores/:id - Eliminar indicador
  deleteIndicador: async (id) => {
    const result = await secureApiCall(`/api/indicadores/${id}`, {
      method: 'DELETE'
    });
    return result.data;
  },

  // 📈 GET /api/indicadores/estadisticas/dashboard - Estadísticas
  getEstadisticas: async () => {
    const result = await secureApiCall('/api/indicadores/estadisticas/dashboard');
    return result.data;
  },

  // 🔍 GET /health - Health check del backend
  healthCheck: async () => {
    const result = await secureApiCall('/health');
    return result.data;
  },

  // 🧪 GET /test-cors - Test de CORS
  testCors: async () => {
    const result = await secureApiCall('/test-cors');
    return result.data;
  }
};

/* ================================================================
   🛠️ UTILIDADES ADICIONALES
   ================================================================ */

// 🧪 Test de conectividad
export const testConnection = async () => {
  try {
    console.log('🧪 [API] Probando conectividad...');
    const health = await indicadoresApi.healthCheck();
    console.log('✅ [API] Conectividad OK:', health);
    return { success: true, data: health };
  } catch (error) {
    console.error('❌ [API] Error de conectividad:', error);
    return { success: false, error: error.message };
  }
};

// Export por defecto
export default indicadoresApi;
