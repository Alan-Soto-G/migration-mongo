# 🔒 Guía de Schema Validation Rules - MongoDB con Mongoose

**Sistema de Gestión de Viajes Turísticos**

---

## 📍 **RESPUESTA DIRECTA: ¿Dónde implementar las validaciones?**

### **UBICACIÓN: En los archivos `entidades/*_Mongoose.js`**

Cada archivo de entidad debe tener validaciones en el Schema de Mongoose.

---

## ✅ **YA IMPLEMENTADAS (Ejemplos completos)**

Los siguientes archivos YA TIENEN validaciones completas como referencia:

1. ✅ `entidades/cliente_Mongoose.js` - Validaciones de datos personales
2. ✅ `entidades/hotel_Mongoose.js` - Validaciones de categorías y referencias
3. ✅ `entidades/tarjetabancaria_Mongoose.js` - Validaciones de seguridad
4. ✅ `entidades/factura_Mongoose.js` - Validaciones condicionales

---

## 📋 **Tipos de Validaciones Disponibles en Mongoose**

### 1️⃣ **Validaciones Básicas**

```javascript
{
    campo: {
        type: String,           // Tipo de dato
        required: [true, 'Mensaje de error'],  // Campo obligatorio
        unique: true,           // Valor único en la colección
        default: 'valor',       // Valor por defecto
    }
}
```

### 2️⃣ **Validaciones de Strings**

```javascript
{
    nombre: {
        type: String,
        trim: true,             // Quita espacios al inicio/final
        lowercase: true,        // Convierte a minúsculas
        uppercase: true,        // Convierte a mayúsculas
        minlength: [2, 'Muy corto'],
        maxlength: [100, 'Muy largo'],
        match: [/regex/, 'Formato inválido'],  // Expresión regular
        enum: {                 // Solo valores permitidos
            values: ['Valor1', 'Valor2'],
            message: '{VALUE} no es válido'
        }
    }
}
```

### 3️⃣ **Validaciones de Números**

```javascript
{
    precio: {
        type: Number,
        min: [0, 'No puede ser negativo'],
        max: [1000000, 'Muy alto'],
        validate: {             // Validación personalizada
            validator: function(v) {
                return v >= 0 && Number.isFinite(v);
            },
            message: 'Debe ser un número válido'
        }
    }
}
```

### 4️⃣ **Validaciones de Fechas**

```javascript
{
    fechaVencimiento: {
        type: Date,
        validate: {
            validator: function(v) {
                return v > new Date();  // Fecha futura
            },
            message: 'La fecha debe ser futura'
        }
    }
}
```

### 5️⃣ **Referencias a otras colecciones**

```javascript
{
    idHotel: {
        type: Number,
        required: true,
        ref: 'hotel_Mongoose'   // Nombre del modelo referenciado
    }
}
```

### 6️⃣ **Validaciones Condicionales**

```javascript
{
    idTarjeta: {
        type: Number,
        ref: 'tarjetabancaria_Mongoose',
        validate: {
            validator: function(v) {
                // Solo requerido si metodoPago es 'Tarjeta'
                if (this.metodoPago === 'Tarjeta') {
                    return v != null && v > 0;
                }
                return true;
            },
            message: 'Tarjeta obligatoria para pago con tarjeta'
        }
    }
}
```

---

## 🎯 **PLANTILLA PARA APLICAR A TUS ENTIDADES**

### **Ejemplo: habitacion_Mongoose.js**

```javascript
import mongoose from "mongoose";

const Schema = mongoose.Schema;
const model = mongoose.model;

export const habitacion_Mongoose = new Schema({
    "_id": mongoose.ObjectId,
    "idHabitacion": {
        type: Number,
        required: [true, 'El ID es obligatorio'],
        unique: true,
        min: [1, 'El ID debe ser mayor a 0']
    },
    "numero": {
        type: String,
        required: [true, 'El número de habitación es obligatorio'],
        trim: true,
        maxlength: [10, 'Máximo 10 caracteres']
    },
    "tipo": {
        type: String,
        required: [true, 'El tipo es obligatorio'],
        enum: {
            values: ['Simple', 'Doble', 'Suite', 'Presidencial'],
            message: '{VALUE} no es un tipo válido'
        }
    },
    "precioNoche": {
        type: Number,
        required: [true, 'El precio es obligatorio'],
        min: [0, 'El precio no puede ser negativo']
    },
    "capacidad": {
        type: Number,
        required: [true, 'La capacidad es obligatoria'],
        min: [1, 'Mínimo 1 persona'],
        max: [10, 'Máximo 10 personas']
    },
    "idHotel": {
        type: Number,
        required: [true, 'El hotel es obligatorio'],
        ref: 'hotel_Mongoose'
    }
}, { 
    collection: "habitacion",
    timestamps: true
})

// Índices
habitacion_Mongoose.index({ idHotel: 1 });
habitacion_Mongoose.index({ tipo: 1 });

export const habitacion_MongooseModel = model("habitacion_Mongoose", habitacion_Mongoose);
```

---

## 📊 **ENTIDADES PENDIENTES DE VALIDAR**

Debes aplicar validaciones similares a:

- [ ] `actividadturistica_Mongoose.js`
- [ ] `administrador_Mongoose.js`
- [ ] `aeronave_aerolinea_Mongoose.js`
- [ ] `aeronave_Mongoose.js`
- [ ] `carro_Mongoose.js`
- [ ] `clienteViaje_Mongoose.js`
- [ ] `cuota_Mongoose.js`
- [ ] `guia_Mongoose.js`
- [ ] `guiaActividad_Mongoose.js`
- [ ] `habitacion_Mongoose.js`
- [ ] `itinerariotransporte_Mongoose.js`
- [ ] `municipio_Mongoose.js`
- [ ] `plan_Mongoose.js`
- [ ] `planActividad_Mongoose.js`
- [ ] `reserva_Mongoose.js`
- [ ] `serviciotransporte_Mongoose.js`
- [ ] `trayecto_Mongoose.js`
- [ ] `vehiculo_gps_Mongoose.js`
- [ ] `vehiculo_Mongoose.js`
- [ ] `viaje_Mongoose.js`
- [ ] `viajePlan_Mongoose.js`

---

## 🔧 **VALIDACIONES RECOMENDADAS POR TIPO DE ENTIDAD**

### **Entidades Maestras (Cliente, Hotel, Guía, etc.)**
- `required: true` en campos clave
- `unique: true` en identificadores
- `enum` para estados y categorías
- `match` para emails y teléfonos
- `min/max` para rangos numéricos

### **Entidades de Relación (ClienteViaje, GuiaActividad, etc.)**
- `required: true` en todas las referencias
- `ref` apuntando a las colecciones relacionadas
- `enum` para roles y estados
- Validaciones de fechas

### **Entidades con Datos Sensibles (Tarjeta, Factura)**
- Validaciones estrictas con `match`
- Middleware `pre-save` para verificaciones adicionales
- `uppercase` o `lowercase` según corresponda
- Validaciones condicionales

---

## 🚀 **BENEFICIOS DE LAS VALIDACIONES**

| Beneficio | Descripción |
|-----------|-------------|
| ✅ **Integridad de datos** | Evita datos inválidos en MongoDB |
| ✅ **Mensajes claros** | Errores descriptivos para el usuario |
| ✅ **Validación automática** | Mongoose valida antes de guardar |
| ✅ **Seguridad** | Previene inyecciones y datos maliciosos |
| ✅ **Documentación** | El schema documenta la estructura |
| ✅ **Menos bugs** | Errores detectados antes de llegar a BD |

---

## ⚡ **ÍNDICES RECOMENDADOS**

```javascript
// Al final del schema, antes del export del modelo

// Índices simples
schema.index({ campoFrecuenteEnConsultas: 1 });

// Índices compuestos
schema.index({ campo1: 1, campo2: 1 });

// Índices de texto para búsquedas
schema.index({ nombre: 'text', descripcion: 'text' });

// Índices únicos
schema.index({ email: 1 }, { unique: true });
```

---

## 📌 **MIDDLEWARES ÚTILES**

```javascript
// Pre-save: ejecuta antes de guardar
schema.pre('save', function(next) {
    // Validaciones personalizadas
    if (this.fechaInicio > this.fechaFin) {
        return next(new Error('Fecha inicio debe ser anterior a fecha fin'));
    }
    next();
});

// Pre-update: ejecuta antes de actualizar
schema.pre('findOneAndUpdate', function(next) {
    this.options.runValidators = true; // Importante: ejecutar validaciones en updates
    next();
});

// Post-save: ejecuta después de guardar
schema.post('save', function(doc, next) {
    console.log(`✅ ${this.nombre} guardado correctamente`);
    next();
});
```

---

## 🎯 **PASOS PARA VALIDAR CADA ENTIDAD**

1. **Abrir el archivo** `entidades/[nombre]_Mongoose.js`
2. **Identificar campos obligatorios** del modelo de negocio
3. **Aplicar validaciones básicas**: `required`, `type`
4. **Agregar validaciones específicas**: `enum`, `min/max`, `match`
5. **Definir referencias**: usar `ref` para relacionar colecciones
6. **Crear índices** en campos de consulta frecuente
7. **Probar** creando documentos inválidos para verificar errores

---

## ✅ **VERIFICAR QUE FUNCIONAN**

```javascript
// Ejemplo de prueba de validación
import { cliente_MongooseModel } from './entidades/cliente_Mongoose.js';

async function probarValidacion() {
    try {
        const clienteInvalido = new cliente_MongooseModel({
            idCliente: -1,  // ❌ Menor a 1
            email: 'no-es-email',  // ❌ Formato inválido
            estado: 'NoExiste'  // ❌ No está en enum
        });
        await clienteInvalido.save();
    } catch (error) {
        console.log('✅ Validación funcionando:', error.message);
    }
}
```

---

## 📞 **RESUMEN EJECUTIVO**

### ¿DÓNDE implementar?
**En cada archivo `entidades/*_Mongoose.js`**

### ¿CÓMO implementar?
**Cambiando cada campo de:**
```javascript
"campo": String
```
**A:**
```javascript
"campo": {
    type: String,
    required: [true, 'Error personalizado'],
    // ... más validaciones
}
```

### ¿Cuándo se ejecutan?
**Automáticamente al hacer `.save()` o `.create()`**

### ¿Ejemplos completos?
**Ver: cliente_Mongoose.js, hotel_Mongoose.js, tarjetabancaria_Mongoose.js, factura_Mongoose.js**

---

<div align="center">

**📅 Fecha:** 20 de Octubre de 2025  
**🔧 Framework:** Mongoose 8.19.1  
**💾 Base de datos:** MongoDB Atlas

---

*Documento técnico - Sistema de Gestión de Viajes Turísticos*

</div>

