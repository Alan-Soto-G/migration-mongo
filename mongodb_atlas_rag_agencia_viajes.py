# -*- coding: utf-8 -*-
"""
MongoDB Atlas RAG - Sistema de Gestión de Viajes Turísticos
=============================================================

Este script implementa un sistema RAG (Retrieval-Augmented Generation) para 
consultar información de una agencia de viajes usando MongoDB Atlas con búsqueda vectorial.

Proyecto: Sistema de Gestión de Viajes Turísticos
Base de datos: MongoDB Atlas
Colecciones principales: cliente, hotel, vehiculo, viaje, plan, reserva, factura, etc.
"""

# ================================
# 1) INSTALACIÓN DE DEPENDENCIAS
# ================================
"""
Ejecuta esto primero si es necesario:

pip install --quiet "pymongo[srv]" pillow tqdm transformers sentencepiece ftfy regex python-dotenv
pip install --quiet torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install --quiet openai
"""

# ================================
# 2) IMPORTACIONES
# ================================
import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from datetime import datetime
import torch
from transformers import CLIPProcessor, CLIPModel
import numpy as np
from typing import List, Dict
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ================================
# 3) CONFIGURACIÓN DE MONGODB ATLAS
# ================================

# IMPORTANTE: Configura estas variables en un archivo .env o directamente aquí
# Ejemplo de .env:
# MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/?retryWrites=true&w=majority

MONGODB_URI = os.getenv("MONGO_URI", "mongodb+srv://usuario:password@cluster.mongodb.net/?retryWrites=true&w=majority")

# Nombre de la base de datos del proyecto
DB_NAME = "agencia_viajes_turisticos"

# Colecciones principales del sistema
COLLECTIONS = {
    "clientes": "cliente",
    "hoteles": "hotel",
    "vehiculos": "vehiculo",
    "viajes": "viaje",
    "planes": "plan",
    "reservas": "reserva",
    "facturas": "factura",
    "municipios": "municipio",
    "guias": "guia",
    "actividades": "actividadturistica"
}

# Conectar a MongoDB Atlas
try:
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    print(f"✅ Conectado a MongoDB Atlas")
    print(f"📊 Base de datos: {DB_NAME}")
    print(f"📁 Colecciones disponibles: {db.list_collection_names()[:10]}")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("💡 Verifica tu MONGO_URI en el archivo .env o en la variable MONGODB_URI")

# ================================
# 4) CONFIGURACIÓN DE GROQ LLM
# ================================

from openai import OpenAI

# Configura tu API Key de Groq (obtén una gratis en https://console.groq.com)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "tu_api_key_aqui")

os.environ["OPENAI_API_KEY"] = GROQ_API_KEY
groq_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

print(f"✅ Cliente Groq configurado")

# ================================
# 5) MODELO DE EMBEDDINGS (OPCIONAL)
# ================================
"""
Si deseas implementar búsqueda vectorial semántica, descomenta esta sección
y crea índices vectoriales en MongoDB Atlas.

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "openai/clip-vit-base-patch32"

clip_model = CLIPModel.from_pretrained(model_name).to(device)
clip_proc = CLIPProcessor.from_pretrained(model_name)

def embed_texts_clip(texts):
    inputs = clip_proc(text=texts, return_tensors="pt", padding=True)
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)
    with torch.no_grad():
        txt_emb = clip_model.get_text_features(input_ids=input_ids, attention_mask=attention_mask)
    txt_emb = txt_emb / txt_emb.norm(p=2, dim=-1, keepdim=True)
    return txt_emb.cpu().numpy().astype("float32")

print("✅ Modelo CLIP cargado para embeddings")
"""

# ================================
# 6) FUNCIONES DE CONSULTA A MONGODB
# ================================

def buscar_clientes_por_criterio(criterio: Dict = None, limite: int = 10) -> List[Dict]:
    """
    Busca clientes en la base de datos según criterios específicos.
    
    Args:
        criterio: Diccionario con filtros (ej: {"estado": "Activo"})
        limite: Número máximo de resultados
    
    Returns:
        Lista de documentos de clientes
    """
    try:
        if criterio is None:
            criterio = {}
        
        resultados = list(db[COLLECTIONS["clientes"]].find(criterio).limit(limite))
        print(f"🔍 Encontrados {len(resultados)} clientes")
        return resultados
    except Exception as e:
        print(f"❌ Error buscando clientes: {e}")
        return []

def buscar_hoteles_por_ubicacion(municipio: str = None, limite: int = 10) -> List[Dict]:
    """
    Busca hoteles por ubicación (municipio).
    
    Args:
        municipio: Nombre del municipio
        limite: Número máximo de resultados
    
    Returns:
        Lista de documentos de hoteles
    """
    try:
        criterio = {}
        if municipio:
            # Primero buscar el ID del municipio
            municipio_doc = db[COLLECTIONS["municipios"]].find_one({"nombre": {"$regex": municipio, "$options": "i"}})
            if municipio_doc:
                criterio["idMunicipio"] = municipio_doc.get("idMunicipio")
        
        resultados = list(db[COLLECTIONS["hoteles"]].find(criterio).limit(limite))
        print(f"🏨 Encontrados {len(resultados)} hoteles")
        return resultados
    except Exception as e:
        print(f"❌ Error buscando hoteles: {e}")
        return []

def buscar_viajes_disponibles(limite: int = 10) -> List[Dict]:
    """
    Busca viajes disponibles en el sistema.
    
    Args:
        limite: Número máximo de resultados
    
    Returns:
        Lista de documentos de viajes
    """
    try:
        resultados = list(db[COLLECTIONS["viajes"]].find().limit(limite))
        print(f"✈️ Encontrados {len(resultados)} viajes")
        return resultados
    except Exception as e:
        print(f"❌ Error buscando viajes: {e}")
        return []

def obtener_reservas_cliente(id_cliente: int) -> List[Dict]:
    """
    Obtiene todas las reservas de un cliente específico.
    
    Args:
        id_cliente: ID del cliente
    
    Returns:
        Lista de reservas del cliente
    """
    try:
        pipeline = [
            {"$match": {"idCliente": id_cliente}},
            {"$lookup": {
                "from": COLLECTIONS["viajes"],
                "localField": "idViaje",
                "foreignField": "idViaje",
                "as": "viaje_info"
            }},
            {"$limit": 20}
        ]
        
        resultados = list(db[COLLECTIONS["reservas"]].aggregate(pipeline))
        print(f"📋 Encontradas {len(resultados)} reservas para cliente {id_cliente}")
        return resultados
    except Exception as e:
        print(f"❌ Error obteniendo reservas: {e}")
        return []

def estadisticas_generales() -> Dict:
    """
    Obtiene estadísticas generales del sistema.
    
    Returns:
        Diccionario con estadísticas
    """
    try:
        stats = {
            "total_clientes": db[COLLECTIONS["clientes"]].count_documents({}),
            "total_hoteles": db[COLLECTIONS["hoteles"]].count_documents({}),
            "total_viajes": db[COLLECTIONS["viajes"]].count_documents({}),
            "total_reservas": db[COLLECTIONS["reservas"]].count_documents({}),
            "total_vehiculos": db[COLLECTIONS["vehiculos"]].count_documents({}),
            "clientes_activos": db[COLLECTIONS["clientes"]].count_documents({"estado": "Activo"}),
        }
        return stats
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
        return {}

# ================================
# 7) CONSTRUCCIÓN DE CONTEXTO PARA LLM
# ================================

def construir_contexto_clientes(documentos: List[Dict], max_items: int = 5) -> str:
    """Construye contexto textual desde documentos de clientes."""
    if not documentos:
        return "No se encontraron clientes en la búsqueda."
    
    lineas = ["=== INFORMACIÓN DE CLIENTES ===\n"]
    for i, doc in enumerate(documentos[:max_items], 1):
        nombre_completo = f"{doc.get('nombre', 'N/A')} {doc.get('apellido', 'N/A')}"
        email = doc.get('email', 'N/A')
        estado = doc.get('estado', 'N/A')
        telefono = doc.get('telefono', 'N/A')
        tipo_doc = doc.get('tipoDocumento', 'N/A')
        num_doc = doc.get('numeroDocumento', 'N/A')
        
        lineas.append(f"{i}. {nombre_completo}")
        lineas.append(f"   - Email: {email}")
        lineas.append(f"   - Teléfono: {telefono}")
        lineas.append(f"   - Documento: {tipo_doc} {num_doc}")
        lineas.append(f"   - Estado: {estado}\n")
    
    return "\n".join(lineas)

def construir_contexto_hoteles(documentos: List[Dict], max_items: int = 5) -> str:
    """Construye contexto textual desde documentos de hoteles."""
    if not documentos:
        return "No se encontraron hoteles en la búsqueda."
    
    lineas = ["=== INFORMACIÓN DE HOTELES ===\n"]
    for i, doc in enumerate(documentos[:max_items], 1):
        nombre = doc.get('nombre', 'N/A')
        direccion = doc.get('direccion', 'N/A')
        categoria = doc.get('categoria', 'N/A')
        telefono = doc.get('telefono', 'N/A')
        
        lineas.append(f"{i}. {nombre}")
        lineas.append(f"   - Categoría: {categoria}")
        lineas.append(f"   - Dirección: {direccion}")
        lineas.append(f"   - Teléfono: {telefono}\n")
    
    return "\n".join(lineas)

def construir_contexto_viajes(documentos: List[Dict], max_items: int = 5) -> str:
    """Construye contexto textual desde documentos de viajes."""
    if not documentos:
        return "No se encontraron viajes en la búsqueda."
    
    lineas = ["=== INFORMACIÓN DE VIAJES ===\n"]
    for i, doc in enumerate(documentos[:max_items], 1):
        destino = doc.get('destino', 'N/A')
        fecha_inicio = doc.get('fechaInicio', 'N/A')
        fecha_fin = doc.get('fechaFin', 'N/A')
        estado = doc.get('estado', 'N/A')
        
        lineas.append(f"{i}. Destino: {destino}")
        lineas.append(f"   - Fecha inicio: {fecha_inicio}")
        lineas.append(f"   - Fecha fin: {fecha_fin}")
        lineas.append(f"   - Estado: {estado}\n")
    
    return "\n".join(lineas)

def construir_contexto_estadisticas(stats: Dict) -> str:
    """Construye contexto textual desde estadísticas."""
    if not stats:
        return "No se pudieron obtener estadísticas."
    
    lineas = ["=== ESTADÍSTICAS DEL SISTEMA ===\n"]
    lineas.append(f"📊 Total de clientes: {stats.get('total_clientes', 0)}")
    lineas.append(f"✅ Clientes activos: {stats.get('clientes_activos', 0)}")
    lineas.append(f"🏨 Total de hoteles: {stats.get('total_hoteles', 0)}")
    lineas.append(f"✈️ Total de viajes: {stats.get('total_viajes', 0)}")
    lineas.append(f"📋 Total de reservas: {stats.get('total_reservas', 0)}")
    lineas.append(f"🚗 Total de vehículos: {stats.get('total_vehiculos', 0)}")
    
    return "\n".join(lineas)

# ================================
# 8) GENERACIÓN DE RESPUESTAS CON GROQ
# ================================

def generar_respuesta_con_llm(contexto: str, pregunta: str, model: str = "llama-3.1-8b-instant") -> str:
    """
    Genera una respuesta usando Groq LLM basándose en el contexto proporcionado.
    
    Args:
        contexto: Información recuperada de MongoDB
        pregunta: Pregunta del usuario
        model: Modelo de Groq a utilizar
    
    Returns:
        Respuesta generada por el LLM
    """
    system_prompt = """Eres un asistente experto del Sistema de Gestión de Viajes Turísticos. 
Tu trabajo es ayudar a los usuarios con información sobre clientes, hoteles, viajes, reservas y servicios turísticos.
Responde de forma clara, profesional y amigable, usando SOLO la información del contexto proporcionado.
Si no tienes información suficiente en el contexto, dilo explícitamente."""

    full_prompt = f"""[CONTEXTO DE LA BASE DE DATOS]
{contexto}

[PREGUNTA DEL USUARIO]
{pregunta}

[INSTRUCCIONES]
Responde la pregunta basándote ÚNICAMENTE en el contexto anterior.
- Sé claro y conciso
- Usa un tono profesional pero amigable
- Si falta información, indícalo
- Organiza la respuesta con viñetas o numeración si es apropiado
"""

    try:
        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.4,
            max_tokens=512
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error al generar respuesta: {e}"

# ================================
# 9) FUNCIONES DE DEMOSTRACIÓN
# ================================

def demo_consulta_clientes():
    """Demo: Consultar clientes activos y generar respuesta."""
    print("\n" + "="*60)
    print("DEMO 1: Consulta de Clientes Activos")
    print("="*60)
    
    # Buscar clientes activos
    clientes = buscar_clientes_por_criterio({"estado": "Activo"}, limite=5)
    
    # Construir contexto
    contexto = construir_contexto_clientes(clientes)
    
    # Pregunta
    pregunta = "¿Cuántos clientes activos hay y cuáles son sus datos de contacto principales?"
    
    print(f"\n📝 Pregunta: {pregunta}")
    print("\n🤖 Respuesta del LLM:")
    print("-" * 60)
    
    respuesta = generar_respuesta_con_llm(contexto, pregunta)
    print(respuesta)

def demo_consulta_hoteles():
    """Demo: Consultar hoteles disponibles."""
    print("\n" + "="*60)
    print("DEMO 2: Consulta de Hoteles")
    print("="*60)
    
    # Buscar hoteles
    hoteles = buscar_hoteles_por_ubicacion(limite=5)
    
    # Construir contexto
    contexto = construir_contexto_hoteles(hoteles)
    
    # Pregunta
    pregunta = "Dame una lista de los hoteles disponibles con sus características principales."
    
    print(f"\n📝 Pregunta: {pregunta}")
    print("\n🤖 Respuesta del LLM:")
    print("-" * 60)
    
    respuesta = generar_respuesta_con_llm(contexto, pregunta)
    print(respuesta)

def demo_estadisticas_sistema():
    """Demo: Estadísticas generales del sistema."""
    print("\n" + "="*60)
    print("DEMO 3: Estadísticas del Sistema")
    print("="*60)
    
    # Obtener estadísticas
    stats = estadisticas_generales()
    
    # Construir contexto
    contexto = construir_contexto_estadisticas(stats)
    
    # Pregunta
    pregunta = "Dame un resumen ejecutivo del estado actual del sistema de gestión de viajes."
    
    print(f"\n📝 Pregunta: {pregunta}")
    print("\n🤖 Respuesta del LLM:")
    print("-" * 60)
    
    respuesta = generar_respuesta_con_llm(contexto, pregunta)
    print(respuesta)

def demo_consulta_personalizada(tipo_consulta: str, pregunta: str):
    """Demo: Consulta personalizada."""
    print("\n" + "="*60)
    print(f"DEMO: Consulta Personalizada - {tipo_consulta}")
    print("="*60)
    
    contexto = ""
    
    if tipo_consulta == "clientes":
        docs = buscar_clientes_por_criterio(limite=10)
        contexto = construir_contexto_clientes(docs)
    elif tipo_consulta == "hoteles":
        docs = buscar_hoteles_por_ubicacion(limite=10)
        contexto = construir_contexto_hoteles(docs)
    elif tipo_consulta == "viajes":
        docs = buscar_viajes_disponibles(limite=10)
        contexto = construir_contexto_viajes(docs)
    elif tipo_consulta == "estadisticas":
        stats = estadisticas_generales()
        contexto = construir_contexto_estadisticas(stats)
    else:
        print(f"❌ Tipo de consulta no reconocido: {tipo_consulta}")
        return
    
    print(f"\n📝 Pregunta: {pregunta}")
    print("\n🤖 Respuesta del LLM:")
    print("-" * 60)
    
    respuesta = generar_respuesta_con_llm(contexto, pregunta)
    print(respuesta)

# ================================
# 10) FUNCIÓN PRINCIPAL
# ================================

def main():
    """Función principal con menú de opciones."""
    print("\n" + "="*60)
    print("🌟 SISTEMA RAG - AGENCIA DE VIAJES TURÍSTICOS")
    print("="*60)
    
    while True:
        print("\n📋 MENÚ DE OPCIONES:")
        print("1. Consultar clientes activos")
        print("2. Consultar hoteles disponibles")
        print("3. Ver estadísticas del sistema")
        print("4. Consultar viajes disponibles")
        print("5. Consulta personalizada")
        print("6. Ejecutar todas las demos")
        print("0. Salir")
        
        opcion = input("\n👉 Selecciona una opción: ").strip()
        
        if opcion == "1":
            demo_consulta_clientes()
        elif opcion == "2":
            demo_consulta_hoteles()
        elif opcion == "3":
            demo_estadisticas_sistema()
        elif opcion == "4":
            docs = buscar_viajes_disponibles(limite=10)
            contexto = construir_contexto_viajes(docs)
            pregunta = "¿Qué viajes están disponibles actualmente?"
            print(f"\n📝 Pregunta: {pregunta}")
            print("\n🤖 Respuesta del LLM:")
            print("-" * 60)
            respuesta = generar_respuesta_con_llm(contexto, pregunta)
            print(respuesta)
        elif opcion == "5":
            print("\nTipos disponibles: clientes, hoteles, viajes, estadisticas")
            tipo = input("Tipo de consulta: ").strip().lower()
            pregunta = input("Tu pregunta: ").strip()
            demo_consulta_personalizada(tipo, pregunta)
        elif opcion == "6":
            demo_consulta_clientes()
            demo_consulta_hoteles()
            demo_estadisticas_sistema()
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")

# ================================
# 11) EJECUCIÓN
# ================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║  MongoDB Atlas RAG - Sistema de Gestión de Viajes Turísticos  ║
    ║                                                                ║
    ║  📋 Configuración necesaria:                                  ║
    ║  1. Archivo .env con MONGO_URI y GROQ_API_KEY                ║
    ║  2. Conexión activa a MongoDB Atlas                           ║
    ║  3. Colecciones creadas en la base de datos                   ║
    ║                                                                ║
    ║  🚀 Funcionalidades:                                          ║
    ║  - Consultas a clientes, hoteles, viajes                      ║
    ║  - Estadísticas del sistema                                   ║
    ║  - Respuestas generadas con IA (Groq)                         ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error general: {e}")
