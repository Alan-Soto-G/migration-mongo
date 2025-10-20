# 🎯 Guía Rápida de Inicio - Sistema RAG

## 📦 Archivos Creados

```
migration-mongo/
├── mongodb_atlas_rag_agencia_viajes.py  ← Script principal RAG
├── .env.example                         ← Plantilla de configuración
├── README_RAG.md                        ← Documentación completa
└── .gitignore                           ← Protección de credenciales
```

## ⚡ Inicio Rápido (5 pasos)

### 1️⃣ Instalar Dependencias

```powershell
pip install pymongo[srv] python-dotenv openai
```

### 2️⃣ Configurar Credenciales

```powershell
# Copiar plantilla
copy .env.example .env

# Editar .env con tus credenciales:
# - MONGO_URI (desde MongoDB Atlas)
# - GROQ_API_KEY (desde https://console.groq.com)
```

### 3️⃣ Verificar Conexión MongoDB

Asegúrate de que tu base de datos tiene colecciones creadas:

```powershell
node migrar.js
```

### 4️⃣ Ejecutar el Sistema RAG

```powershell
python mongodb_atlas_rag_agencia_viajes.py
```

### 5️⃣ Probar las Funcionalidades

Selecciona una opción del menú:

- `1` → Consultar clientes activos
- `2` → Consultar hoteles disponibles
- `3` → Ver estadísticas del sistema
- `5` → Hacer consulta personalizada

## 🔑 Obtener Credenciales

### MongoDB Atlas URI

1. Ir a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Database → Connect → Drivers → Python
3. Copiar el URI y reemplazar `<password>` con tu contraseña
4. Formato: `mongodb+srv://usuario:password@cluster.mongodb.net/...`

### Groq API Key

1. Ir a [Groq Console](https://console.groq.com)
2. Crear cuenta (gratis)
3. API Keys → Create API Key
4. Copiar y guardar en `.env`

## 💡 Ejemplos de Consultas

### Ejemplo 1: Clientes

```
Pregunta: "¿Cuántos clientes activos tenemos?"
Respuesta: Información de los clientes con email, teléfono, etc.
```

### Ejemplo 2: Hoteles

```
Pregunta: "¿Qué hoteles de 5 estrellas hay disponibles?"
Respuesta: Lista de hoteles con categoría, ubicación, contacto
```

### Ejemplo 3: Estadísticas

```
Pregunta: "Dame un resumen ejecutivo del sistema"
Respuesta: Total de clientes, hoteles, viajes, reservas, etc.
```

## 🛠️ Solución de Problemas

### ❌ Error: "pymongo could not be resolved"

```powershell
pip install pymongo[srv]
```

### ❌ Error: "Connection refused"

- Verificar MONGO_URI en `.env`
- Verificar Network Access en MongoDB Atlas
- Verificar que tu IP está permitida

### ❌ Error: "No module named 'dotenv'"

```powershell
pip install python-dotenv
```

### ❌ Error: "openai module not found"

```powershell
pip install openai
```

## 📊 Estructura del Sistema

```
Usuario → Pregunta en lenguaje natural
    ↓
Sistema RAG → Consulta MongoDB Atlas
    ↓
Recupera datos relevantes → Construye contexto
    ↓
Groq LLM → Genera respuesta natural
    ↓
Respuesta al usuario
```

## 🎓 Conceptos Clave

### ¿Qué es RAG?

**Retrieval-Augmented Generation** = Recuperación + Generación con IA

1. **Retrieval (Recuperación)**: Busca información relevante en la base de datos
2. **Augmentation (Aumento)**: Construye contexto con los datos encontrados
3. **Generation (Generación)**: IA genera respuesta natural basada en el contexto

### ¿Por qué usar RAG?

- ✅ Respuestas basadas en datos reales
- ✅ No inventa información
- ✅ Actualizado con tu base de datos
- ✅ Lenguaje natural para consultas complejas

## 📚 Recursos Adicionales

- 📖 [README_RAG.md](README_RAG.md) - Documentación completa
- 🌐 [MongoDB Atlas Docs](https://www.mongodb.com/docs/atlas/)
- 🤖 [Groq API Docs](https://console.groq.com/docs)
- 🐍 [PyMongo Tutorial](https://pymongo.readthedocs.io/)

## ✅ Checklist de Verificación

Antes de ejecutar, verifica:

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pymongo`, `python-dotenv`, `openai`)
- [ ] Archivo `.env` creado y configurado
- [ ] MONGO_URI correcto en `.env`
- [ ] GROQ_API_KEY correcto en `.env`
- [ ] Conexión a internet activa
- [ ] MongoDB Atlas con colecciones creadas

## 🚀 ¡Listo para Empezar!

```powershell
python mongodb_atlas_rag_agencia_viajes.py
```

---

**Nota**: Si encuentras algún problema, consulta el [README_RAG.md](README_RAG.md) completo o revisa la sección de Solución de Problemas.
