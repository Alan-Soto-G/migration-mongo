# 🚀 Sistema RAG - Agencia de Viajes Turísticos

Sistema de Recuperación Aumentada con Generación (RAG) para consultar la base de datos de MongoDB Atlas usando IA.

## 📋 Descripción

Este script implementa un sistema RAG que permite hacer consultas en lenguaje natural sobre la base de datos de la agencia de viajes turísticos, utilizando:

- **MongoDB Atlas**: Base de datos NoSQL con las colecciones del sistema
- **Groq LLM**: Modelo de lenguaje para generar respuestas naturales
- **Python**: Lenguaje de programación principal

## 🔧 Requisitos Previos

### 1. Python 3.8 o superior

```bash
python --version
```

### 2. Cuenta en MongoDB Atlas

- Crear un cluster gratuito en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Configurar Network Access (permitir tu IP)
- Crear usuario con permisos de lectura/escritura

### 3. API Key de Groq

- Registrarse en [Groq Console](https://console.groq.com)
- Crear una API Key gratuita

## 📦 Instalación

### Paso 1: Instalar dependencias

```bash
# Navegar al directorio del proyecto
cd "c:\Users\User\Documents\Manu\ucaldas\2025-2 Quinto Semestre\bases de datos no relacionales\proyectoAgencia\migration-mongo"

# Instalar paquetes necesarios
pip install pymongo[srv] python-dotenv openai
```

### Paso 2: Configurar variables de entorno

1. Copia el archivo `.env.example` a `.env`:

```bash
copy .env.example .env
```

2. Edita el archivo `.env` con tus credenciales:

```env
MONGO_URI=tu_uri_de_mongodb_atlas_aqui
GROQ_API_KEY=tu_api_key_de_groq_aqui
```

### Paso 3: Verificar colecciones en MongoDB

Asegúrate de que tu base de datos tenga las colecciones creadas. Ejecuta el script de migración si es necesario:

```bash
node migrar.js
```

## 🚀 Uso

### Ejecutar el script

```bash
python mongodb_atlas_rag_agencia_viajes.py
```

### Menú de opciones

El script presenta un menú interactivo:

```
📋 MENÚ DE OPCIONES:
1. Consultar clientes activos
2. Consultar hoteles disponibles
3. Ver estadísticas del sistema
4. Consultar viajes disponibles
5. Consulta personalizada
6. Ejecutar todas las demos
0. Salir
```

## 💡 Ejemplos de Uso

### Ejemplo 1: Consultar clientes activos

```
👉 Selecciona una opción: 1

📝 Pregunta: ¿Cuántos clientes activos hay y cuáles son sus datos de contacto principales?

🤖 Respuesta del LLM:
Actualmente tenemos 5 clientes activos en el sistema:
1. Juan Pérez - Email: juan@email.com - Tel: +57 300 1234567
2. María García - Email: maria@email.com - Tel: +57 301 2345678
...
```

### Ejemplo 2: Consulta personalizada

```
👉 Selecciona una opción: 5

Tipos disponibles: clientes, hoteles, viajes, estadisticas
Tipo de consulta: hoteles
Tu pregunta: ¿Qué hoteles de 5 estrellas tenemos disponibles?

🤖 Respuesta del LLM:
Según la información disponible, los hoteles de 5 estrellas son:
- Hotel Luxury Palace (Bogotá)
- Grand Resort & Spa (Cartagena)
...
```

## 📊 Funcionalidades Principales

### 1. Consultas a Base de Datos

- ✅ Búsqueda de clientes por criterios
- ✅ Búsqueda de hoteles por ubicación
- ✅ Consulta de viajes disponibles
- ✅ Obtención de reservas por cliente
- ✅ Estadísticas generales del sistema

### 2. Generación de Respuestas con IA

- ✅ Construcción automática de contexto desde MongoDB
- ✅ Generación de respuestas naturales con Groq LLM
- ✅ Respuestas basadas únicamente en datos reales

### 3. Tipos de Consultas Soportadas

| Tipo         | Colecciones          | Ejemplo de Pregunta              |
| ------------ | -------------------- | -------------------------------- |
| Clientes     | `cliente`            | "¿Cuántos clientes activos hay?" |
| Hoteles      | `hotel`, `municipio` | "¿Qué hoteles hay en Bogotá?"    |
| Viajes       | `viaje`              | "¿Qué viajes están disponibles?" |
| Estadísticas | Todas                | "Dame un resumen del sistema"    |

## 🏗️ Estructura del Código

```python
mongodb_atlas_rag_agencia_viajes.py
├── Sección 1: Instalación de dependencias (comentada)
├── Sección 2: Importaciones
├── Sección 3: Configuración MongoDB Atlas
├── Sección 4: Configuración Groq LLM
├── Sección 5: Modelo de embeddings (opcional)
├── Sección 6: Funciones de consulta a MongoDB
│   ├── buscar_clientes_por_criterio()
│   ├── buscar_hoteles_por_ubicacion()
│   ├── buscar_viajes_disponibles()
│   ├── obtener_reservas_cliente()
│   └── estadisticas_generales()
├── Sección 7: Construcción de contexto
│   ├── construir_contexto_clientes()
│   ├── construir_contexto_hoteles()
│   ├── construir_contexto_viajes()
│   └── construir_contexto_estadisticas()
├── Sección 8: Generación con LLM
│   └── generar_respuesta_con_llm()
├── Sección 9: Funciones de demostración
│   ├── demo_consulta_clientes()
│   ├── demo_consulta_hoteles()
│   ├── demo_estadisticas_sistema()
│   └── demo_consulta_personalizada()
├── Sección 10: Función principal con menú
│   └── main()
└── Sección 11: Ejecución
```

## 🔐 Seguridad

### Protección de Credenciales

- ✅ Usar archivo `.env` para credenciales
- ✅ **NUNCA** compartir el archivo `.env` en repositorios públicos
- ✅ Agregar `.env` al `.gitignore`

### Ejemplo de .gitignore

```gitignore
# Variables de entorno
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
```

## 🛠️ Personalización

### Agregar nuevas funciones de consulta

```python
def buscar_actividades_turisticas(categoria: str = None) -> List[Dict]:
    """Busca actividades turísticas por categoría."""
    criterio = {}
    if categoria:
        criterio["categoria"] = categoria

    return list(db["actividadturistica"].find(criterio).limit(10))
```

### Agregar nuevos constructores de contexto

```python
def construir_contexto_actividades(documentos: List[Dict]) -> str:
    """Construye contexto desde actividades turísticas."""
    lineas = ["=== ACTIVIDADES TURÍSTICAS ===\n"]
    for doc in documentos:
        lineas.append(f"- {doc.get('nombre')}: {doc.get('descripcion')}")
    return "\n".join(lineas)
```

## 🐛 Solución de Problemas

### Error: "pymongo could not be resolved"

**Solución:** Instalar pymongo

```bash
pip install pymongo[srv]
```

### Error: "Connection refused"

**Soluciones:**

1. Verificar que el URI de MongoDB es correcto
2. Verificar Network Access en MongoDB Atlas
3. Verificar que tu IP está permitida

### Error: "API Key invalid"

**Solución:** Verificar que la API Key de Groq es correcta en el archivo `.env`

### Las consultas no devuelven resultados

**Soluciones:**

1. Verificar que las colecciones existen en MongoDB
2. Verificar que hay datos en las colecciones
3. Ejecutar `node migrar.js` para crear las colecciones

## 📈 Próximas Mejoras

- [ ] Implementar búsqueda vectorial con embeddings (CLIP)
- [ ] Agregar soporte para imágenes (hoteles, destinos)
- [ ] Implementar caché de consultas frecuentes
- [ ] Agregar historial de conversación
- [ ] Crear interfaz web con Streamlit/Gradio
- [ ] Implementar autenticación de usuarios

## 📚 Referencias

- [MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/)
- [Groq API Documentation](https://console.groq.com/docs)
- [PyMongo Tutorial](https://pymongo.readthedocs.io/)

## 📝 Licencia

Este proyecto es parte del curso de Bases de Datos No Relacionales - Universidad de Caldas.

## 👥 Autores

- Proyecto desarrollado para el curso 2025-2 Quinto Semestre
- Universidad de Caldas

---

¿Necesitas ayuda? Revisa la documentación o contacta al equipo de desarrollo. 🚀
