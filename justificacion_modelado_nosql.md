# 📊 Justificación de Decisiones de Modelado NoSQL

**Sistema de Gestión de Viajes Turísticos - MongoDB**

---

## 📋 Tabla de Contenidos

- [1. Justificación de Decisiones de Modelado NoSQL](#1-justificación-de-decisiones-de-modelado-nosql)
  - [1.1 Enfoque Adoptado](#11-enfoque-adoptado-híbrido-referencing--embedding)
  - [1.2 Clasificación de Entidades](#12-clasificación-de-entidades)
  - [1.3 Ventajas y Limitaciones](#13-ventajas-y-limitaciones)
- [2. Comparación Embedding vs. Referencing](#2-comparación-embedding-vs-referencing)
  - [2.1 Diferencias Fundamentales](#21-diferencias-fundamentales)
  - [2.2 Aplicación en el Sistema](#22-aplicación-en-el-sistema-casos-específicos)
  - [2.3 Tabla Resumen de Decisiones](#23-tabla-resumen-de-decisiones)
  - [2.4 Regla de Decisión](#24-regla-de-decisión)
  - [2.5 Conclusión](#25-conclusión)

---

## 1. Justificación de Decisiones de Modelado NoSQL

### 1.1 Enfoque Adoptado: HÍBRIDO (REFERENCING + EMBEDDING)

#### 🎯 Estrategia Principal: REFERENCING (Referencias entre colecciones)

- Usado en el **95%** de las relaciones del sistema
- Mantiene separadas las **25 colecciones** del modelo

#### ✅ Razones de la Decisión

| Razón | Descripción |
|-------|-------------|
| **Migración estructurada** | Proviene de modelo relacional bien diseñado |
| **Flexibilidad** | Actualizaciones independientes por entidad |
| **Reutilización** | Entidades maestras (hoteles, clientes, municipios) compartidas |
| **Sin duplicación** | Evita redundancia de datos |
| **Tamaño controlado** | Documentos < 16MB |
| **Consultas independientes** | Facilita reportes y análisis |

---

### 1.2 Clasificación de Entidades

#### 🏛️ A) ENTIDADES MAESTRAS - Totalmente independientes (8)

```
Cliente, Hotel, Municipio, Guía, Plan, Administrador, Vehículo, Aeronave
```

> **Justificación:** Se reutilizan en múltiples contextos, requieren actualizaciones centralizadas

---

#### 🔗 B) ENTIDADES DE RELACIÓN - Muchos-a-muchos (5)

```
ClienteViaje, GuiaActividad, PlanActividad, ViajePlan, AeronaveAerolinea
```

> **Justificación:** Relaciones N:M con metadatos adicionales (rol, estado, fechas)

---

#### 📎 C) ENTIDADES DEPENDIENTES - Con referencias (11)

```
Habitación→Hotel, Reserva→Viaje/Habitación, Factura→Tarjeta, etc.
```

> **Justificación:** Alta cardinalidad, actualizaciones independientes

---

#### ⭐ D) CASO ESPECIAL - EMBEDDING (1)

```
Vehículo → GPS (documento embebido)
```

> **Justificación:** Relación 1:1, siempre juntos, datos pequeños, no se reutiliza

---

### 1.3 Ventajas y Limitaciones

#### ✅ VENTAJAS

| Ventaja | Beneficio |
|---------|-----------|
| **Consistencia** | Cambios centralizados se reflejan automáticamente |
| **Escalabilidad** | Documentos de tamaño controlado |
| **Mantenibilidad** | Fácil actualizar entidades maestras |
| **Flexibilidad** | Agregar relaciones sin reestructurar |

#### ⚠️ LIMITACIONES

| Limitación | Solución |
|------------|----------|
| Requiere múltiples consultas | Usar `$lookup` y aggregation pipeline |
| No hay integridad referencial automática | Validar en capa de aplicación |
| Mayor complejidad en queries | Mitigar con índices estratégicos |

---

## 2. Comparación Embedding vs. Referencing

### 2.1 Diferencias Fundamentales

<table>
<tr>
<th>🔹 EMBEDDING (Documentos embebidos)</th>
<th>🔹 REFERENCING (Referencias)</th>
</tr>
<tr>
<td>

**✅ Ventajas:**
- Una sola consulta
- Mejor rendimiento en lectura
- Atomicidad garantizada
- Localidad de datos

**❌ Desventajas:**
- Duplicación de datos
- Documentos grandes
- Dificulta actualizaciones

</td>
<td>

**✅ Ventajas:**
- Sin duplicación
- Documentos controlados
- Actualizaciones centralizadas
- Flexibilidad en consultas

**❌ Desventajas:**
- Múltiples consultas
- Mayor complejidad
- No hay integridad automática

</td>
</tr>
</table>

---

### 2.2 Aplicación en el Sistema (Casos Específicos)

#### 📍 CASO 1: VEHÍCULO → GPS (EMBEDDING ✓)

```json
{
  "idVehiculo": 123,
  "tipo": "Bus",
  "placa": "ABC123",
  "modelo": "Mercedes 2020",
  "capacidad": 45,
  "estado": "Activo",
  "gps": {
    "latitud": 4.6097,
    "longitud": -74.0817,
    "ultimaActualizacion": "2025-10-19T10:30:00Z"
  }
}
```

**💡 Razón:** Relación 1:1, siempre juntos, datos pequeños, actualizaciones atómicas

---

#### 📍 CASO 2: HOTEL → HABITACIONES (REFERENCING ✓)

```json
// Colección: hotel
{
  "idHotel": 1,
  "nombre": "Hotel Paradise",
  "direccion": "Calle 100 #15-20",
  "categoria": 5,
  "municipioId": 10
}

// Colección: habitacion (SEPARADA)
{
  "idHabitacion": 101,
  "numero": "101",
  "tipo": "Suite",
  "precioNoche": 250000,
  "capacidad": 2,
  "idHotel": 1  // ← Referencia
}
```

**💡 Razón:** Alta cardinalidad (100+ habitaciones), actualizaciones independientes, evita documentos gigantes, permite filtros y paginación

---

#### 📍 CASO 3: CLIENTE → TARJETAS BANCARIAS (REFERENCING ✓)

```json
// Colección: cliente
{
  "idCliente": 1,
  "nombre": "Juan",
  "email": "juan@email.com"
}

// Colección: tarjetabancaria (SEPARADA)
{
  "idTarjeta": 1,
  "tipo": "Crédito",
  "numeroEnmascarado": "****1234",
  "idCliente": 1  // ← Referencia
}
```

**💡 Razón:** 🔒 **SEGURIDAD** (datos sensibles aislados), múltiples tarjetas por cliente

---

#### 📍 CASO 4: VIAJE → CLIENTES (REFERENCING con tabla intermedia ✓)

```json
// Colección: viaje
{
  "idViaje": 1,
  "nombre": "Tour Caribe",
  "fechaInicio": "2025-12-01",
  "costoTotal": 2000000
}

// Colección: clienteViaje (INTERMEDIA)
{
  "idCliente": 5,
  "idViaje": 1,
  "rolViajero": "Principal",
  "estado": "Confirmado",
  "fechaParticipacion": "2025-10-19"
}

// Colección: cliente
{
  "idCliente": 5,
  "nombre": "María"
}
```

**💡 Razón:** Relación N:M con metadatos (rol, estado), consultas bidireccionales

---

#### 📍 CASO 5: ACTIVIDAD → MUNICIPIO (REFERENCING ✓)

```json
// Colección: actividadturistica
{
  "idActividad": 1,
  "nombre": "City Tour",
  "descripcion": "Recorrido por el centro histórico",
  "duracionHoras": 3,
  "costo": 50000,
  "idMunicipio": 10  // ← Referencia
}

// Colección: municipio
{
  "idMunicipio": 10,
  "nombre": "Cartagena",
  "departamento": "Bolívar",
  "pais": "Colombia",
  "descripcionTuristica": "Ciudad histórica amurallada..."
}
```

**💡 Razón:** Municipio se reutiliza en actividades, hoteles, trayectos; evita duplicación

---

#### 📍 CASO 6: FACTURA → TARJETA (REFERENCING ✓)

```json
{
  "idFactura": 1,
  "numeroFactura": "F-2025-001",
  "fechaEmision": "2025-10-19",
  "total": 500000,
  "metodoPago": "Tarjeta",
  "estado": "Pagada",
  "idTarjeta": 1  // ← Referencia
}
```

**💡 Razón:** Auditoría, integridad histórica, seguridad

---

### 2.3 Tabla Resumen de Decisiones

| Relación | Estrategia | Razón Principal |
|----------|-----------|----------------|
| Vehículo → GPS | `EMBEDDING` | 1:1, siempre juntos |
| Hotel → Habitaciones | `REFERENCING` | Alta cardinalidad (100+) |
| Cliente → Tarjetas | `REFERENCING` | Seguridad, múltiples tarjetas |
| Viaje → Clientes | `REFERENCING` | N:M con metadatos |
| Actividad → Municipio | `REFERENCING` | Reutilización |
| Factura → Tarjeta | `REFERENCING` | Auditoría |
| Habitación → Hotel | `REFERENCING` | Consultas independientes |
| Reserva → Viaje/Habitación | `REFERENCING` | Múltiples referencias |
| Plan → Actividades | `REFERENCING` | N:M variable |

---

### 2.4 Regla de Decisión

#### 🔵 USAR EMBEDDING cuando:

```
✓ Relación 1:1 o 1:pocos (< 10 elementos)
✓ Datos siempre se consultan juntos
✓ Sin reutilización en otros contextos
✓ Datos pequeños y relativamente estáticos
```

#### 🔵 USAR REFERENCING cuando:

```
✓ Relación 1:muchos (cardinalidad alta)
✓ Relación N:M (muchos-a-muchos)
✓ Entidades se reutilizan en múltiples contextos
✓ Actualizaciones independientes frecuentes
✓ Datos sensibles que requieren aislamiento
```

---

### 2.5 Conclusión

#### ✅ El modelo REFERENCING predominante es CORRECTO para este sistema porque:

- [x] Sistema migrado de modelo relacional bien estructurado
- [x] Entidades maestras (cliente, hotel, municipio) se reutilizan extensamente
- [x] Actualizaciones frecuentes requieren datos centralizados
- [x] Relaciones N:M necesitan colecciones intermedias
- [x] El único EMBEDDING (vehículo→gps) está justificado correctamente

---

#### 💡 RECOMENDACIONES

1. **Índices estratégicos**
   - Crear índices en campos de referencia (`idHotel`, `idCliente`, `idMunicipio`)
   - Índices compuestos para consultas frecuentes

2. **Aggregation Pipeline**
   - Usar `$lookup` para joins eficientes cuando sea necesario
   - Implementar pipelines predefinidos para queries comunes

3. **Validaciones**
   - Implementar validaciones de integridad referencial en aplicación
   - Middleware para verificar existencia de referencias

4. **Optimización selectiva**
   - Considerar desnormalización parcial (cache de nombres)
   - Vistas materializadas para consultas complejas frecuentes

---

<div align="center">

**📅 Fecha:** 20 de Octubre de 2025  
**💾 Base de datos:** MongoDB Atlas  
**📊 Total de colecciones:** 25

---

*Documento generado para el Sistema de Gestión de Viajes Turísticos*

</div>

