# 🚀 **HORIZONS - Sistema de Indicadores Empresariales**

[![React](https://img.shields.io/badge/React-18.2.0-blue)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)](https://fastapi.tiangolo.com/)
[![Railway](https://img.shields.io/badge/Deploy-Railway-purple)](https://railway.app/)
[![Security](https://img.shields.io/badge/Security-Enterprise%20Grade-red)](./docs/SECURITY-CHECKLIST.md)

> 📊 **Plataforma profesional** para gestión y seguimiento de indicadores empresariales con dashboard interactivo, cronogramas Gantt y análisis de progreso en tiempo real.

---

## 🎯 **CARACTERÍSTICAS PRINCIPALES**

### 🏢 **Gestión Empresarial**
- **📊 Dashboard Ejecutivo** con métricas en tiempo real
- **📈 Cronogramas Gantt** interactivos con Syncfusion
- **🎯 Seguimiento de Hitos** y progreso automatizado
- **📋 Gestión por VP/Área** con filtros dinámicos

### 🔐 **Seguridad Enterprise**
- **🛡️ Autenticación JWT** con bcrypt
- **🔒 CORS Configurado** para producción
- **⚡ Rate Limiting** anti-ataques
- **🛡️ Headers Seguridad** (HSTS, CSP, XSS)

### 🚀 **Arquitectura Moderna**
- **⚡ Frontend React** con Vite y Tailwind CSS
- **🔥 Backend FastAPI** con PostgreSQL
- **☁️ Deploy Railway** con auto-configuración
- **📱 Responsive Design** mobile-first

---

## 🏗️ **ESTRUCTURA DEL PROYECTO**

```
📁 Horizons/
├── 📁 frontend/                 # React + Vite Application
│   ├── 📁 src/
│   │   ├── 📁 components/       # UI Components
│   │   │   ├── 📁 ui/          # Radix UI Components
│   │   │   ├── Dashboard.jsx   # Main Dashboard
│   │   │   ├── Layout.jsx      # App Layout
│   │   │   └── Sidebar.jsx     # Navigation
│   │   ├── 📁 pages/           # Page Components
│   │   │   ├── Dashboard.jsx   # Dashboard Page
│   │   │   ├── NuevoIndicador.jsx
│   │   │   ├── ActualizarIndicador.jsx
│   │   │   ├── HistorialIndicadores.jsx
│   │   │   └── GanttSyncfusion.jsx
│   │   ├── 📁 lib/             # Utilities
│   │   │   ├── api.js          # API Client (Unified)
│   │   │   └── utils.js        # Helper Functions
│   │   ├── 📁 context/         # React Context
│   │   │   └── IndicadoresContext.jsx
│   │   └── 📁 hooks/           # Custom Hooks
│   ├── package.json            # Frontend Dependencies
│   └── vite.config.js          # Vite Configuration
│
├── 📁 backend/                  # FastAPI Application
│   ├── 📁 app/
│   │   ├── 📁 models/          # SQLAlchemy Models
│   │   │   └── indicador.py    # Indicador & Hito Models
│   │   ├── 📁 routers/         # FastAPI Routers
│   │   │   └── indicadores.py  # API Endpoints
│   │   ├── 📁 schemas/         # Pydantic Schemas
│   │   │   └── indicador.py    # Request/Response Models
│   │   ├── 📁 crud/            # Database Operations
│   │   │   └── indicador.py    # CRUD Functions
│   │   ├── main.py             # FastAPI App
│   │   ├── auth.py             # JWT Authentication
│   │   ├── security.py         # Security Middleware
│   │   └── database.py         # Database Configuration
│   ├── cargar_datos.py         # Data Loading (Unified)
│   ├── init_db.py              # Database Initialization
│   ├── requirements.txt        # Python Dependencies
│   └── Procfile               # Railway Deployment
│
├── 📁 docs/                    # Documentation
│   ├── RAILWAY-DEPLOYMENT-GUIDE.md  # Deploy Guide
│   ├── SECURITY-CHECKLIST.md        # Security Guide
│   ├── env.production.example       # Environment Template
│   └── PROJECT-CLEANUP-ANALYSIS.md  # Cleanup Analysis
│
├── start.bat                   # Development Startup
├── install_dependencies.bat    # Dependencies Installer
├── debug-mixed-content.html    # Debug Tool
└── README.md                   # This File
```

---

## 🚀 **INICIO RÁPIDO**

### **1️⃣ Instalación de Dependencias**

```bash
# 🎯 Un solo comando para instalar todo
./install_dependencies.bat
```

### **2️⃣ Inicio del Sistema**

```bash
# 🚀 Iniciar frontend + backend simultáneamente
./start.bat
```

### **3️⃣ Acceso a la Aplicación**

- **🌐 Frontend**: http://localhost:5173
- **📡 Backend**: http://localhost:8000
- **📚 API Docs**: http://localhost:8000/docs

---

## 🔧 **CONFIGURACIÓN AVANZADA**

### **🔐 Variables de Entorno (Desarrollo)**

Crear `.env` en `backend/`:

```env
# Base de datos local
DATABASE_URL=sqlite:///./indicadores.db

# Seguridad
SECRET_KEY=tu-clave-secreta-desarrollo
ALLOWED_ORIGINS=["http://localhost:5173"]

# Rate limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

### **☁️ Configuración de Producción**

Ver guía completa: [`docs/RAILWAY-DEPLOYMENT-GUIDE.md`](./docs/RAILWAY-DEPLOYMENT-GUIDE.md)

### **🛡️ Configuración de Seguridad**

Ver checklist: [`docs/SECURITY-CHECKLIST.md`](./docs/SECURITY-CHECKLIST.md)

---

## 📊 **FUNCIONALIDADES DEL DASHBOARD**

### **📈 Métricas Principales**
- Total de Indicadores
- Hitos Completados
- Progreso Promedio
- Indicadores por Estado

### **🎯 Gestión de Indicadores**
- ✅ **Crear** nuevos indicadores
- ✏️ **Editar** indicadores existentes
- 📊 **Seguimiento** de progreso
- 🗑️ **Eliminar** indicadores

### **📅 Cronograma Gantt**
- 📊 **Vista Gantt** con Syncfusion
- 🎯 **Hitos** con fechas específicas
- 📈 **Progreso visual** por barras
- 🔄 **Filtros** por VP y Área

### **📋 Filtros Avanzados**
- **🏢 Por VP**: VPD, VPE, PRE
- **🏗️ Por Área**: Específicas por VP
- **📊 Por Tipo**: Estratégico, Gestión
- **📅 Por Fechas**: Rangos personalizados

---

## 🏢 **ESTRUCTURA ORGANIZACIONAL**

### **VPs Soportados**
- **VPD**: Vicepresidencia de Desarrollo
- **VPE**: Vicepresidencia Ejecutiva  
- **PRE**: Presidencia

### **Áreas por VP**
```
🏢 VPD
├── Alianza Estratégica
├── Análisis y Estudios Económicos
└── Efectividad y Desarrollo

🏢 VPE  
├── TEI (Tecnología)
└── Talento Humano

🏢 PRE
├── Auditoría
├── Comunicación
├── Gestión de Riesgos
└── Legal
```

---

## 🔐 **SEGURIDAD Y AUTENTICACIÓN**

### **🛡️ Características de Seguridad**
- **JWT Authentication** con expiración
- **Password Hashing** con bcrypt
- **Rate Limiting** por IP
- **CORS** configurado para producción
- **Security Headers** completos

### **📊 Monitoreo de Seguridad**
- **Logs de acceso** detallados
- **Detección de ataques** automática
- **Bloqueo temporal** por intentos fallidos
- **Auditoría** de cambios

---

## 🚀 **DEPLOY EN RAILWAY**

### **📦 Servicios Requeridos**
1. **Backend Service** (FastAPI)
2. **Frontend Service** (React)  
3. **PostgreSQL Database**

### **🔧 Variables de Entorno**

**Backend:**
```env
SECRET_KEY=clave-super-secreta-256-bits
ALLOWED_ORIGINS=["https://tu-frontend.railway.app"]
RATE_LIMIT_REQUESTS=1000
ENVIRONMENT=production
AZURE_CLIENT_ID=tu-cliente-azure-id
AZURE_TENANT_ID=tu-tenant-azure-id
AZURE_CLIENT_SECRET=tu-secreto-azure
```

**Frontend:**
```env
VITE_API_URL=https://tu-backend.railway.app
VITE_AZURE_CLIENT_ID=tu-cliente-azure-id
VITE_AZURE_TENANT_ID=tu-tenant-azure-id
```

Ver guía completa: [`docs/RAILWAY-DEPLOYMENT-GUIDE.md`](./docs/RAILWAY-DEPLOYMENT-GUIDE.md)

---

## 🧪 **TESTING Y DEBUG**

### **🔍 Debug de Conectividad**
```bash
# Abrir debug-mixed-content.html en el navegador
# para probar conectividad frontend ↔ backend
```

### **📊 Verificación de Datos**
```bash
cd backend
python cargar_datos.py
```

### **🚀 Build de Producción**
```bash
cd frontend
npm run build
```

---

## 📚 **DOCUMENTACIÓN ADICIONAL**

| Documento | Descripción |
|-----------|-------------|
| [`docs/RAILWAY-DEPLOYMENT-GUIDE.md`](./docs/RAILWAY-DEPLOYMENT-GUIDE.md) | Guía completa de deployment |
| [`docs/SECURITY-CHECKLIST.md`](./docs/SECURITY-CHECKLIST.md) | Checklist de seguridad |
| [`docs/PROJECT-CLEANUP-ANALYSIS.md`](./docs/PROJECT-CLEANUP-ANALYSIS.md) | Análisis de limpieza |

---

## 🛠️ **TECNOLOGÍAS UTILIZADAS**

### **Frontend**
- **React 18.2** - Framework UI
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Radix UI** - Component library
- **Syncfusion Gantt** - Cronogramas
- **Recharts** - Gráficos

### **Backend**
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de datos
- **JWT** - Autenticación
- **bcrypt** - Hash passwords

### **DevOps**
- **Railway** - Hosting
- **Git** - Control de versiones
- **npm/pip** - Package managers

---

## 📈 **ROADMAP**

### **🔜 Próximas Funcionalidades**
- [ ] **📧 Notificaciones** por email
- [ ] **📱 App móvil** nativa
- [ ] **🤖 IA** para predicciones
- [ ] **📊 Analytics** avanzados
- [ ] **🔄 Integración** con herramientas externas

### **🎯 Mejoras Planeadas**
- [ ] **⚡ Performance** optimizations
- [ ] **🎨 UI/UX** improvements
- [ ] **🔐 SSO** integration
- [ ] **📋 Reportes** automáticos

---

## 👥 **CONTRIBUCIÓN**

Para contribuir al proyecto:

1. **Fork** el repositorio
2. **Crear** rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crear** Pull Request

---

## 📄 **LICENCIA**

Este proyecto es **privado** y propietario de la organización.

---

## 🆘 **SOPORTE**

Para soporte técnico o preguntas:

- 📧 **Email**: soporte@empresa.com
- 📱 **Slack**: #horizons-support
- 📋 **Issues**: GitHub Issues

---

**🎉 ¡Horizons - Impulsando el éxito empresarial con datos!** 
 Añadir Loggin