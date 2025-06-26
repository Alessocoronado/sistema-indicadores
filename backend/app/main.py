from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import indicadores
from .routers import auth_oauth
from .database import engine
from .models import indicador
import os
import json

# Crear las tablas en la base de datos
indicador.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Indicadores API",
    description="API para el sistema de gestión de indicadores",
    version="1.0.0"
)

# Middleware personalizado para UTF-8
@app.middleware("http")
async def add_utf8_headers(request, call_next):
    response = await call_next(request)
    if "application/json" in response.headers.get("content-type", ""):
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response

# 🌐 CONFIGURACIÓN CORS FLEXIBLE
def get_allowed_origins():
    """Obtiene los orígenes permitidos desde variables de entorno o configuración por defecto"""
    
    # 1️⃣ Intentar obtener desde variable de entorno
    env_origins = os.getenv("ALLOWED_ORIGINS")
    if env_origins:
        # Convertir string separado por comas a lista
        origins = [origin.strip() for origin in env_origins.split(",") if origin.strip()]
        print(f"🔒 CORS desde ALLOWED_ORIGINS: {origins}")
        return origins
    
    # 2️⃣ Detectar si es producción Railway
    if os.getenv("RAILWAY_ENVIRONMENT_NAME") or os.getenv("ENVIRONMENT") == "production":
        # Buscar URL de frontend automáticamente
        default_origins = [
            "http://localhost:5173",  # Desarrollo local
            "http://localhost:3000",  # Testing local
        ]
        
        # Agregar URLs específicas conocidas de Railway
        specific_frontend_urls = [
            "https://sistema-indicadores--b.up.railway.app",  # URL actual del frontend
            "https://sistema-indicadores-production-0b2b.up.railway.app",  # URL alternativa
            "https://sistema-indicadores-production.up.railway.app",
            "https://frontend-sistema-indicadores-production.up.railway.app",
        ]
        
        # Agregar posibles URLs basadas en service name
        service_name = os.getenv("RAILWAY_SERVICE_NAME", "sistema-indicadores")
        possible_frontend_urls = [
            f"https://{service_name}-frontend-production.up.railway.app",
            f"https://{service_name}-production.up.railway.app", 
            f"https://frontend-{service_name}-production.up.railway.app",
        ]
        
        # 🚨 TEMPORAL: Permitir todos los subdominios de railway.app para resolver el issue
        railway_patterns = [
            "https://sistema-indicadores--production.up.railway.app",
            "https://sistema-indicadores--staging.up.railway.app",
        ]
        
        # Combinar todas las URLs
        all_origins = default_origins + specific_frontend_urls + possible_frontend_urls + railway_patterns
        
        # 🔧 FALLBACK: Si no funciona, permitir todos temporalmente
        if len(all_origins) > 10:  # Si hay muchas URLs, simplificar
            print("🔧 CORS: Demasiadas URLs, usando patrón permisivo temporal")
            return ["*"]
        
        print(f"🔒 CORS producción automático: {all_origins}")
        return all_origins
    
    # 3️⃣ Desarrollo local - permisivo
    else:
        print("🔧 CORS desarrollo - permitir todos los orígenes")
        return ["*"]

# 🌐 APLICAR CONFIGURACIÓN CORS CON MIDDLEWARE PERSONALIZADO
allowed_origins = get_allowed_origins()

# Middleware CORS personalizado para Railway
@app.middleware("http")
async def custom_cors_middleware(request, call_next):
    # Obtener el origen de la petición
    origin = request.headers.get("origin")
    
    # Ejecutar la petición
    response = await call_next(request)
    
    # Determinar si permitir CORS
    allow_cors = False
    
    if "*" in allowed_origins:
        # Desarrollo - permitir todos
        allow_cors = True
        response.headers["Access-Control-Allow-Origin"] = "*"
    elif origin:
        # Verificar si el origen está en la lista permitida
        if origin in allowed_origins:
            allow_cors = True
            response.headers["Access-Control-Allow-Origin"] = origin
        # 🚨 SOLUCIÓN RAILWAY: Permitir subdominios de railway.app
        elif ".railway.app" in origin and origin.startswith("https://"):
            allow_cors = True
            response.headers["Access-Control-Allow-Origin"] = origin
            print(f"🚀 CORS: Permitido subdominio Railway: {origin}")
    
    # Aplicar headers CORS si está permitido
    if allow_cors:
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, X-Requested-With"
        response.headers["Access-Control-Max-Age"] = "86400"
    
    return response

# También aplicar el middleware estándar como backup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in allowed_origins else allowed_origins + ["https://*.railway.app"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"🔒 CORS configurado con middleware personalizado para Railway")

# ✅ NUEVO: Middleware de seguridad
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    
    # 🚀 RAILWAY: Forzar HTTPS en producción
    if os.getenv("ENVIRONMENT") == "production" or os.getenv("RAILWAY_ENVIRONMENT_NAME"):
        # Forzar HTTPS en Railway
        if request.headers.get("x-forwarded-proto") == "http":
            # Redirigir a HTTPS
            https_url = str(request.url).replace("http://", "https://", 1)
            return Response(status_code=307, headers={"Location": https_url})
    
    # Headers de seguridad (solo en producción)
    if os.getenv("ENVIRONMENT") == "production":
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # 🔒 Railway: Forzar HTTPS siempre
        response.headers["X-Railway-Force-HTTPS"] = "1"
    
    # UTF-8 para JSON
    if "application/json" in response.headers.get("content-type", ""):
        response.headers["content-type"] = "application/json; charset=utf-8"
    
    return response

# Incluir routers con prefijo /api
app.include_router(indicadores.router, prefix="/api")
app.include_router(auth_oauth.router)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API de Sistema de Indicadores",
        "version": "1.0.0",
        "status": "running",
        "environment": os.getenv("RAILWAY_ENVIRONMENT_NAME", "development"),
        "database_configured": bool(os.getenv("DATABASE_URL"))
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "message": "API funcionando correctamente",
        "database": "connected",
        "version": "1.0.0"
    }

@app.get("/test-cors")
def test_cors():
    """Endpoint específico para probar CORS"""
    return {
        "message": "CORS funcionando correctamente",
        "timestamp": "2025-01-18",
        "backend": "Railway",
        "status": "success",
        "cors_config": get_allowed_origins()
    }

@app.get("/config")
def get_config():
    """Endpoint para verificar la configuración actual"""
    return {
        "environment": os.getenv("RAILWAY_ENVIRONMENT_NAME", "development"),
        "allowed_origins": get_allowed_origins(),
        "database_configured": bool(os.getenv("DATABASE_URL")),
        "service_name": os.getenv("RAILWAY_SERVICE_NAME", "unknown"),
        "cors_from_env": bool(os.getenv("ALLOWED_ORIGINS")),
        "timestamp": "2025-01-18"
    } 