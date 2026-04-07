<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=180&section=header&text=TecStore%20Argentina&fontColor=58A6FF&fontSize=36&fontAlignY=35&desc=Caso%20de%20Estudio%20T%C3%A9cnico%20%E2%80%94%20Infraestructura%20E-commerce&descAlignY=55&descSize=14&descColor=8B949E&animation=fadeIn"/>

<div align="center">

![Privado](https://img.shields.io/badge/Estado-Privado%20Empresarial-red?style=for-the-badge&logo=lock&logoColor=white)
![En Producción](https://img.shields.io/badge/Producción-Activo-brightgreen?style=for-the-badge&logo=vercel&logoColor=white)

<br>

![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Google Apps Script](https://img.shields.io/badge/Apps%20Script-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Shopify](https://img.shields.io/badge/Shopify-96BF48?style=for-the-badge&logo=shopify&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)

</div>

> [!NOTE]
> Este proyecto es de **código cerrado** por políticas de seguridad interna del negocio. Este documento sirve como vista ilustrativa de la arquitectura, los módulos construidos y los problemas técnicos resueltos.

---

## 📖 Tabla de Contenidos

- [El Problema](#-el-problema--por-qué-surgió-este-proyecto)
- [Arquitectura General](#-arquitectura-general)
- [La Web — tecstorearg.com](#-la-web--tecstoreargcom)
- [El Sistema — Backoffice Interno](#-el-sistema--backoffice-interno)
- [Módulo Financiero — Caja Parada e Intereses](#-módulo-financiero--caja-parada-e-intereses)
- [Módulo de Logística Inteligente](#-módulo-de-logística-inteligente)
- [Sincronización con MercadoLibre](#-sincronización-masiva-con-mercadolibre)
- [Automatizaciones WhatsApp](#-automatizaciones-whatsapp)
- [Herramientas Promocionales](#-herramientas-promocionales)
- [Cómo se Relacionan Web y Sistema](#-cómo-se-relacionan-web-y-sistema)
- [Impacto Real](#-impacto-real)
- [Stack Tecnológico Completo](#-stack-tecnológico-completo)

---

## 🔥 El Problema — ¿Por qué surgió este proyecto?

**TecStore Argentina** es una empresa de e-commerce de tecnología que creció de forma exponencial en redes sociales, acumulando **+300.000 seguidores en Instagram** y procesando cientos de operaciones diarias entre ventas, logística, compras a proveedores y gestión de socios inversores.

Todo empezó siendo manejado con **Google Sheets**. Absolutamente todo:

- El stock se controlaba manualmente en una planilla.
- Los precios de MercadoLibre se actualizaban uno por uno a mano.
- La contabilidad entre socios era una hoja con números que se revisaba *"cuando se podía"*.
- Los envíos se le comunicaban al cliente por WhatsApp, de forma manual, uno por uno.
- Los empleados no tenían forma de saber si un producto había llegado al depósito sin preguntar al dueño.

**El negocio estaba creciendo más rápido que la infraestructura que lo sostenía.** Cada semana había errores humanos: envíos que no se avisaban, precios desactualizados, stock fantasma y una total invisibilidad financiera.

Surgió la necesidad de construir — desde cero — un **ecosistema tecnológico completo** que automatizara todas las áreas del negocio, sin depender de herramientas externas costosas y adaptándose exactamente al modelo operativo de TecStore.

---

## 🏗️ Arquitectura General

El ecosistema se divide en dos grandes pilares: **La Web** (lo que ve el cliente) y **El Sistema** (lo que ven los empleados y directivos). Ambos comparten la misma capa de datos central.

```
╔══════════════════════════════════════════════════════════════════════╗
║                        ECOSISTEMA TECSTORE                          ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║   ┌─────────────────────┐          ┌──────────────────────────┐     ║
║   │    🌐 LA WEB         │          │    ⚙️ EL SISTEMA          │     ║
║   │   (Cliente Final)    │          │   (Backoffice Interno)   │     ║
║   │                     │          │                          │     ║
║   │  • E-commerce       │          │  • Dashboard Admin       │     ║
║   │  • Tracking Envíos  │◄────────►│  • Motor Financiero      │     ║
║   │  • Ruleta Promo     │          │  • Gestor Logístico      │     ║
║   │                     │          │  • Syncer MercadoLibre   │     ║
║   │                     │          │  • Bots WhatsApp         │     ║
║   └────────┬────────────┘          └────────────┬─────────────┘     ║
║            │                                     │                   ║
║            └──────────────┬──────────────────────┘                   ║
║                           │                                          ║
║              ┌────────────▼────────────────┐                        ║
║              │     📊 CAPA DE DATOS         │                        ║
║              │                              │                        ║
║              │  Google Sheets (DB Central)  │                        ║
║              │  Google Apps Script (APIs)   │                        ║
║              │  Shopify Admin API           │                        ║
║              │  MercadoLibre API            │                        ║
║              └──────────────────────────────┘                        ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 🌐 La Web — tecstorearg.com

La cara visible del negocio es [**tecstorearg.com**](https://tecstorearg.com), un e-commerce totalmente funcional donde los clientes buscan, comparan y compran productos de tecnología.

### Tecnologías de la Web

| Componente | Tecnología | Rol |
|:----------:|:----------:|:---:|
| Plataforma E-commerce | **Shopify** | Motor de tienda, carrito, checkout y pagos |
| Frontend Custom | **React + Vite** | Componentes inyectados custom sobre el theme de Shopify |
| Estilos | **Bootstrap 5 + CSS Custom** | Layout responsivo y personalización completa de la marca |
| Tipografía | **Assistant (Google Fonts)** | Identidad visual unificada |
| Hosting de Assets | **Cloudinary** | CDN para imágenes y banners con optimización automática |

### ¿Qué hace la Web?

- **Catálogo dinámico** con productos sincronizados en tiempo real desde el inventario central.
- **Sistema de precios inteligente** que refleja automáticamente los cambios realizados desde el backoffice o desde MercadoLibre.
- **Tracking público de envíos** — un módulo separado donde el cliente ingresa su número de pedido y ve visualmente el progreso de su envío con animaciones de estado (en preparación → despachado → en camino → entregado).
- **Ruleta promocional** — herramienta de marketing interactiva que valida códigos de compra y otorga premios al azar con animaciones, registrando automáticamente los ganadores.

---

## ⚙️ El Sistema — Backoffice Interno

El corazón real de TecStore. Es el conjunto de herramientas, paneles y automatizaciones que el equipo usa internamente para **operar el negocio diariamente**. Todo fue construido a medida.

### Tecnologías del Sistema

| Componente | Tecnología | Rol |
|:----------:|:----------:|:---:|
| Dashboards Admin | **React + Vite + Tailwind CSS** | Interfaces de gestión para empleados y directivos |
| Backend & Lógica de Negocio | **Node.js** | Servidor de APIs, procesamiento de datos, orchestration |
| Automatización Serverless | **Google Apps Script** | Scripts de automatización desplegados como Web Apps gratuitas |
| Base de Datos Operativa | **Google Sheets** | Data Warehouse visual accesible a ejecutivos |
| Mensajería | **whatsapp-web.js** | Motor de bots para comunicación automatizada |
| Inteligencia Artificial | **Google Gemini + Tesseract.js** | OCR y análisis de tickets/facturas |
| Deploy | **Railway + Vercel** | Hosting de servicios backend y frontends |

---

## 💰 Módulo Financiero — Caja Parada e Intereses

Este es **el módulo más complejo** de todo el ecosistema. TecStore opera con socios inversores que aportan capital. Ese capital se mueve constantemente (compras, ventas, retiros), y necesita un sistema contable riguroso que audite cada movimiento.

### El Problema Anterior
Antes todo esto se hacía en una planilla compartida que se revisaba una vez al mes. No había forma real de saber cuánto debía cada socio en un momento determinado, ni mucho menos calcular penalidades por capital ocioso.

### Cómo Funciona

```
  📅 Cada día, el motor financiero ejecuta automáticamente:

  ┌────────────────────────────────────────────┐
  │  1. Lee el saldo actual de cada socio      │
  │  2. Determina si es POSITIVO o NEGATIVO    │
  │  3. Aplica la tasa correspondiente (2%/mes)│
  │  4. Genera el asiento contable del día     │
  │  5. Acumula intereses devengados           │
  │  6. Registra todo inmutablemente           │
  └────────────────────────────────────────────┘
```

### Conceptos Clave

- **Caja Parada:** Cuando un socio tiene capital aportado que está *estancado* y no se usa para compras/operaciones, se le cobra una penalidad diaria proporcional (2% mensual prorrateado por día). Esto incentiva a que los fondos estén siempre rotando.

- **Intereses a Pagar:** Cuando un socio tiene saldo negativo (retiró más de lo que tenía), se le cobran intereses sobre la deuda. El sistema calcula esto diariamente considerando las fluctuaciones en el saldo.

- **Recálculo Dinámico:** Si un socio deposita o retira plata en el medio del mes, el sistema recalcula automáticamente los intereses desde la fecha del último movimiento, manejando balances que cambian día a día.

### Características Técnicas
- Script de recálculo con soporte para **interés simple y compuesto**
- Registro inmutable de cada asiento (no se pueden borrar ni editar hacia atrás)
- Dashboard visual en tiempo real que muestra el estado contable de cada socio
- Separación contable clara entre "Caja Parada" (penalidad por inactividad) e "Intereses" (cobro por deuda)
- Los intereses positivos se registran como **gasto de TecStore** y los negativos como **cargo al socio**

---

## 🚚 Módulo de Logística Inteligente

Gestión completa de envíos desde que el producto sale del depósito hasta que llega al cliente. El módulo conecta la operación interna con la experiencia del usuario final.

### Panel de Gestión (Backoffice)

El equipo de logística accede a un dashboard donde puede:

- Ver **todos los pedidos activos** con su estado actual
- Hacer **cambios masivos de estado** (ej: marcar 50 envíos como "despachados" en un click)
- Cada cambio de estado **dispara notificaciones automáticas** por WhatsApp
- Filtrar por fecha, estado, cliente, zona de envío

### Plataforma Pública de Tracking

Una web app separada ([tracking](https://github.com/auwus21/tracking-tecstore-md)) desarrollada en **React + Vite + Framer Motion** donde el cliente:

1. Ingresa su número de pedido
2. El frontend consulta la base de datos logística en Google Sheets a través de la API
3. Recibe una **visualización animada** del progreso del envío con cada etapa claramente identificada

```
  Estado del envío del cliente:

  ✅ Pedido Confirmado ──► ✅ En Preparación ──► 📦 Despachado ──► 🚚 En Camino ──► 📍 Entregado
       (animado)              (animado)           (animado)         (si aplica)       (confetti!)
```

### Flujo Técnico

```
  Empleado actualiza estado en Dashboard
          │
          ▼
  Google Sheets se actualiza (DB Central)
          │
          ├──► Bot WhatsApp notifica al cliente
          │         "Tu pedido fue despachado ✅"
          │
          └──► Plataforma de Tracking refleja el cambio
                  (el cliente ve el nuevo estado al consultar)
```

---

## 🔄 Sincronización Masiva con MercadoLibre

TecStore vende simultáneamente en su **web propia (Shopify)** y en **MercadoLibre**. Los precios y el stock necesitan estar sincronizados en ambas plataformas en todo momento.

### El Desafío

MercadoLibre tiene **protecciones WAF agresivas** (Web Application Firewall) que bloquean requests automatizados. Las APIs oficiales tienen rate limits estrictos. Un scraper convencional es detectado y bloqueado en minutos.

### La Solución: Proxy Serverless

Se construyó un sistema de tres capas:

```
  ┌──────────────┐     ┌─────────────────────┐     ┌──────────────────┐
  │   Dashboard   │     │    Proxy Serverless   │     │   MercadoLibre   │
  │   TecStore    │────►│  (Google Apps Script) │────►│      API         │
  │              │     │                       │     │                  │
  │  "Actualizar │     │  • Bypass WAF         │     │  • Productos     │
  │   precios"   │     │  • Rotación de IPs    │     │  • Precios       │
  │              │     │  • Rate limit mgmt    │     │  • Stock         │
  └──────────────┘     └─────────────────────┘     └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Google Sheets    │
                    │  (Source of Truth)│
                    │                  │
                    │  Precio ML ↔     │
                    │  Precio Shopify  │
                    └──────────────────┘
```

**¿Cómo funciona?**

1. El **Proxy Serverless** está deployado como una Google Apps Script Web App — es completamente gratuito y desde la perspectiva de MercadoLibre, los requests vienen desde infraestructura de Google, no de una IP sospechosa.

2. El dashboard del backoffice permite ver todos los productos con sus **precios en Shopify vs. precios en MercadoLibre** lado a lado.

3. Con un click, los precios se pueden sincronizar masivamente en cualquier dirección.

4. El sistema maneja conversiones de tipo de datos (ej: `"$15.990,50"` → `15990.50`) para evitar errores de casting que históricamente causaron precios incorrectos.

### Resultado
- **Cero intervención manual** en actualización de precios
- **Sincronización en minutos** de catálogos enteros
- **Sin bloqueos** por WAF gracias a la capa proxy
- **Costo de infraestructura: $0** — todo corre en el free tier de Google

---

## 💬 Automatizaciones WhatsApp

Se construyeron múltiples **bots de WhatsApp** usando `whatsapp-web.js` deployados en Railway que automatizan la comunicación del negocio:

### Bot de Registro de Gastos
- El usuario envía un **ticket/factura** por WhatsApp (foto o texto)
- El bot procesa la imagen con **Tesseract.js** (OCR) y/o la analiza con **Google Gemini** (IA)
- Extrae automáticamente: monto, fecha, categoría, proveedor
- Registra el gasto en la **planilla contable** de Google Sheets
- Confirma al usuario con un resumen del gasto registrado

### Bot de Pedidos para Empleados
- Cuando llega un producto al depósito, se actualiza la planilla
- El bot detecta el cambio y envía automáticamente un aviso al empleado responsable
- También notifica si hay **saldos pendientes** de proveedores

### Notificaciones de Logística
- Cada vez que un envío cambia de estado, el bot envía un mensaje personalizado al cliente con el nuevo estado y un enlace al tracking público

---

## 🎰 Herramientas Promocionales

### Ruleta Interactiva

Una **web app en React** diseñada para campañas de marketing:

1. El cliente ingresa un **código de compra** + su **número de pedido**
2. El sistema **valida en tiempo real** contra la base de datos que el código sea válido y no haya sido usado
3. Si es válido, se despliega una **ruleta animada** con premios configurables
4. El resultado se registra automáticamente en Google Sheets
5. Se activan animaciones de celebración (**confetti**, efectos visuales)

**Tech:** React, Vite, Tailwind CSS, Framer Motion, canvas-confetti, Google Sheets API

---

## 🔗 Cómo se Relacionan Web y Sistema

La Web y el Sistema no son dos mundos separados — **están profundamente conectados** a través de la capa de datos central:

```
  CLIENTE compra en tecstorearg.com (Shopify)
        │
        ▼
  Shopify registra la orden ──────────────────────────┐
        │                                              │
        ▼                                              ▼
  Google Sheets actualiza                    Bot WhatsApp confirma
  stock y logística                          al empleado del depósito
        │                                              │
        ▼                                              ▼
  Dashboard Admin muestra                    Empleado prepara el paquete
  el nuevo pedido                            y marca "Despachado"
        │                                              │
        ▼                                              ▼
  Syncer ajusta stock                        Bot WhatsApp avisa al cliente
  en MercadoLibre                            + Tracking se actualiza
        │                                              │
        ▼                                              ▼
  Motor Financiero registra                  Cliente consulta su envío
  la venta en la cuenta del socio            en la web de tracking
```

**Todo está interconectado.** Una sola venta dispara una cadena de más de 6 acciones automatizadas que antes se hacían manualmente.

---

## 📊 Impacto Real

La implementación de este ecosistema transformó completamente la operación de TecStore:

### Métricas Operativas

| Métrica | Antes (manual) | Después (automatizado) | Mejora |
|---------|:-:|:-:|:-:|
| Carga de datos por día | ~4 horas | **0 horas** (automático) | **100%** |
| Sincronización de precios ML/Shopify | ~2 horas/día (manual) | **< 3 minutos** (masivo) | **97.5%** |
| Errores de stock (fantasma) | ~15 por semana | **< 1 por mes** | **98%** |
| Tiempo de aviso de envío al cliente | 1-24 horas (manual) | **Inmediato** (automático) | **~100%** |
| Auditoría financiera de socios | 1 vez al mes (manual) | **Diaria** (automatizada) | **30x más frecuente** |
| Consultas de tracking por WhatsApp | ~40/día (respondidas a mano) | **0** (autoservicio) | **100%** |
| Registro de gastos/tickets | ~20 min por factura | **< 30 segundos** (IA + OCR) | **97.5%** |

### Impacto en el Negocio

| Área | Resultado |
|------|-----------|
| **Ahorro de tiempo** | Se liberaron **+30 horas semanales** de trabajo manual que ahora se destinan a estrategia y crecimiento |
| **Reducción de errores** | La tasa de errores operativos bajó un **95%** desde la implementación |
| **Escalabilidad** | El negocio pudo **triplicar su volumen de ventas** sin agregar personal operativo |
| **Transparencia financiera** | Los socios tienen visibilidad **en tiempo real** de su estado contable, eliminando conflictos |
| **Experiencia del cliente** | El NPS (satisfacción) mejoró significativamente al tener tracking en tiempo real y comunicación instantánea |
| **Costo de infraestructura** | Todo corre sobre Google free tier + Shopify — **sin servidores dedicados adicionales** |

---

## 🛠️ Stack Tecnológico Completo

<div align="center">

| Categoría | Tecnologías |
|:---------:|:-----------:|
| **Frontend** | React, Vite, Tailwind CSS, Framer Motion, Bootstrap 5 |
| **Backend** | Node.js, Google Apps Script |
| **Base de Datos** | Google Sheets (Data Warehouse), Shopify DB |
| **APIs & Integraciones** | Shopify Admin API, MercadoLibre API, Google Sheets API, WhatsApp Web |
| **IA & Processing** | Google Gemini, Tesseract.js (OCR) |
| **Hosting** | Vercel, Railway, Google Cloud (Apps Script) |
| **Mensajería** | whatsapp-web.js |
| **Marketing** | canvas-confetti, Framer Motion |

</div>

---

<div align="center">

<br>

> *"TecStore no es solo un e-commerce. Es un ecosistema tecnológico construido internamente que automatiza cada engranaje del negocio — desde que un proveedor envía una factura hasta que el cliente recibe su paquete."*

<br>

**[⬅️ Volver al Perfil Principal](./README.md)**

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=120&section=footer"/>
