<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=180&section=header&text=TecStore%20Argentina&fontColor=58A6FF&fontSize=36&fontAlignY=35&desc=Caso%20de%20Estudio%20T%C3%A9cnico%20%E2%80%94%20Infraestructura%20E-commerce&descAlignY=55&descSize=14&descColor=8B949E&animation=fadeIn"/>

<div align="center">

![Privado](https://img.shields.io/badge/Estado-Privado%20Empresarial-red?style=for-the-badge&logo=lock&logoColor=white)
![En Producción](https://img.shields.io/badge/Producción-Activo-brightgreen?style=for-the-badge&logo=vercel&logoColor=white)

<br>

![React](https://img.shields.io/badge/React_19-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Next.js](https://img.shields.io/badge/Next.js_14-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-18181A?style=for-the-badge&logo=supabase&logoColor=3ECF8E)
![Tailwind](https://img.shields.io/badge/Tailwind-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)

</div>

> [!NOTE]
> Este proyecto es de **código cerrado** por políticas de seguridad interna del negocio. Este documento sirve como vista ilustrativa de la arquitectura, los módulos construidos y los problemas técnicos resueltos.

---

## 📖 Tabla de Contenidos

- [El Problema](#-el-problema--por-qué-surgió-este-proyecto)
- [Arquitectura General](#-arquitectura-general)
- [La Web — tecstore-web](#-la-web--tecstore-web)
- [El Sistema — SistemaVentaTec](#-el-sistema--sistemaventatec)
- [Módulo de Ventas](#-módulo-de-ventas)
- [Módulo de Catálogo y Compras](#-módulo-de-catálogo-y-compras)
- [Módulo de Logística e Inventario](#-módulo-de-logística-e-inventario)
- [Módulo Financiero](#-módulo-financiero--caja-parada-intereses-y-cierres)
- [Módulo de iPhones Usados](#-módulo-de-iphones-usados)
- [Módulo de Rewards (TecPoints)](#-módulo-de-rewards-tecpoints)
- [Sincronización con MercadoLibre](#-sincronización-con-mercadolibre)
- [Seguridad e Inteligencia Artificial](#-seguridad-e-inteligencia-artificial)
- [Cómo se Relacionan Web y Sistema](#-cómo-se-relacionan-web-y-sistema)
- [Impacto Real](#-impacto-real)
- [Stack Tecnológico Completo](#-stack-tecnológico-completo)

---

## 🔥 El Problema — ¿Por qué surgió este proyecto?

**TecStore Argentina** es una empresa de e-commerce de tecnología que creció de forma exponencial en redes sociales, acumulando **+300.000 seguidores en Instagram** y procesando cientos de operaciones diarias entre ventas, logística, compras a proveedores y gestión de socios inversores.

El negocio originalmente funcionaba con herramientas genéricas. No existía un sistema centralizado: el stock se controlaba en planillas, los envíos se comunicaban manualmente, la contabilidad entre socios se revisaba cuando se podía, y los precios de MercadoLibre se actualizaban uno por uno.

**El negocio estaba creciendo más rápido que la infraestructura que lo sostenía.** Cada semana había errores humanos: envíos sin avisar, precios desactualizados, stock fantasma, y una total invisibilidad financiera.

Surgió la necesidad de construir — desde cero — un **ecosistema tecnológico completo** con dos grandes pilares: un **sistema interno de gestión** (backoffice) y una **web pública e-commerce**, ambos conectados a una misma base de datos en la nube.

---

## 🏗️ Arquitectura General

El ecosistema se divide en dos aplicaciones independientes que comparten la misma capa de datos en **Supabase (PostgreSQL)**:

```
╔══════════════════════════════════════════════════════════════════════════╗
║                          ECOSISTEMA TECSTORE                            ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   ┌──────────────────────┐            ┌───────────────────────────┐     ║
║   │    🌐 LA WEB          │            │    ⚙️ EL SISTEMA           │     ║
║   │   tecstore-web        │            │   SistemaVentaTec         │     ║
║   │   (Cliente Final)     │            │   (Backoffice Interno)    │     ║
║   │                      │            │                           │     ║
║   │  Next.js 14 + TS     │            │  React 19 + Vite          │     ║
║   │  Framer Motion       │            │  Tailwind CSS             │     ║
║   │  Zustand             │◄──────────►│  Recharts                 │     ║
║   │  next-themes         │            │  SWR                      │     ║
║   │                      │            │  jsPDF + html2canvas      │     ║
║   │  ─────────────────   │            │  ─────────────────────    │     ║
║   │  • Catálogo público  │            │  • Dashboard              │     ║
║   │  • Carrito + Checkout│            │  • Ventas + Pedidos Web   │     ║
║   │  • Seguimiento envíos│            │  • Compras + Proveedores  │     ║
║   │  • Rewards / Kiosco  │            │  • Logística + Inventario │     ║
║   │  • Ruleta promo      │            │  • Finanzas + Caja Parada │     ║
║   │  • Cotizador usados  │            │  • iPhones Usados         │     ║
║   │  • Perfil de usuario │            │  • Rewards Admin          │     ║
║   │  • Dark Mode         │            │  • Auditoría + Logs       │     ║
║   └──────────┬───────────┘            └─────────────┬─────────────┘     ║
║              │                                       │                   ║
║              └───────────────┬───────────────────────┘                   ║
║                              │                                           ║
║                 ┌────────────▼──────────────────┐                       ║
║                 │     🗄️ SUPABASE (PostgreSQL)   │                       ║
║                 │                                │                       ║
║                 │  • 70+ migraciones SQL         │                       ║
║                 │  • Row Level Security (RLS)    │                       ║
║                 │  • Edge Functions (Gemini AI)  │                       ║
║                 │  • Triggers automáticos        │                       ║
║                 │  • Stored Procedures (RPCs)    │                       ║
║                 │  • Realtime subscriptions      │                       ║
║                 └────────────────────────────────┘                       ║
║                              │                                           ║
║                 ┌────────────▼──────────────────┐                       ║
║                 │     🔗 INTEGRACIONES           │                       ║
║                 │                                │                       ║
║                 │  • MercadoLibre API (Proxy)    │                       ║
║                 │  • Google Apps Script (WAF)    │                       ║
║                 │  • Google Gemini (IA)          │                       ║
║                 │  • Vercel Analytics            │                       ║
║                 └────────────────────────────────┘                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🌐 La Web — tecstore-web

La cara visible del negocio. Una **aplicación Next.js 14 con TypeScript** completa que funciona como e-commerce, portal de clientes y plataforma de fidelización.

### Stack de la Web

| Componente | Tecnología |
|:----------:|:----------:|
| Framework | **Next.js 14** (App Router) |
| Lenguaje | **TypeScript** |
| Estilos | **Tailwind CSS** |
| Animaciones | **Framer Motion** |
| State Management | **Zustand** |
| Base de Datos | **Supabase** (PostgreSQL) |
| Tema | **next-themes** (Dark/Light Mode) |
| SEO | sitemap.ts, robots.ts dinámicos |
| Deploy | **Vercel** |

### Rutas y Funcionalidades de la Web

| Ruta | Funcionalidad |
|------|--------------|
| `/` | **Home Page** — Hero carousel animado, catálogo destacado, robot animado interactivo |
| `/catalogo` | **Catálogo Público** — Todos los productos disponibles con búsqueda, filtros y variantes |
| `/checkout` | **Carrito y Checkout** — Flujo de compra completo con sidebar de carrito persistente |
| `/seguimiento` | **Tracking de Envíos** — El cliente ingresa su número de pedido y ve el estado animado en tiempo real |
| `/rewards` | **Programa TecPoints** — Dashboard del programa de fidelización con puntos acumulados y misiones |
| `/kiosco` | **Kiosco de Premios** — Canje de TecPoints por descuentos y beneficios |
| `/ruleta` | **Ruleta Promocional** — Ruleta interactiva con validación de código de compra y premios al azar |
| `/cotizar` | **Cotizador de Usados** — Herramienta para cotizar iPhones y dispositivos usados |
| `/usados` | **Catálogo de Usados** — Listado de dispositivos reacondicionados en venta |
| `/perfil` | **Perfil del Usuario** — Historial de compras, datos personales, avatares |
| `/auth` | **Autenticación** — Login/Registro integrado con Supabase Auth |
| `/ayuda` | **Centro de Ayuda** — FAQ y soporte |

### Componentes Destacados de la Web
- **`HeroCarousel.tsx`** (18KB) — Carrusel hero con transiciones animadas
- **`CartSidebar.tsx`** — Panel lateral de carrito persistente
- **`GlobalSearch.tsx`** — Búsqueda global en tiempo real
- **`AnimatedRobot.tsx`** — Robot mascota animado con CSS puro
- **`ThemeToggle.tsx`** — Toggle dark/light mode

---

## ⚙️ El Sistema — SistemaVentaTec

El corazón operativo. Es una **SPA en React 19 + Vite** que el equipo y los directivos usan para operar el negocio diariamente. Cada módulo fue construido a medida.

### Stack del Sistema

| Componente | Tecnología |
|:----------:|:----------:|
| Framework | **React 19** |
| Bundler | **Vite** |
| Estilos | **Tailwind CSS** |
| Base de Datos | **Supabase** (PostgreSQL) |
| Gráficos | **Recharts** |
| Data Fetching | **SWR** (stale-while-revalidate) |
| PDFs | **jsPDF + jsPDF-AutoTable** |
| Capturas | **html2canvas** |
| Códigos de barra | **react-barcode** |
| Iconos | **Lucide React** |
| Notificaciones | **SweetAlert2** |
| Analytics | **Vercel Analytics + React GA4** |
| Sanitización | **DOMPurify** |
| Deploy | **Vercel** |

### Rutas del Sistema (con control de acceso)

| Ruta | Módulo | Acceso |
|------|--------|:------:|
| `/` | Dashboard General | Todos |
| `/ventas` | Gestión de Ventas | Todos |
| `/compras` | Catálogo, Compras y Productos | Todos |
| `/logistica` | Inventario, Despachos, Transferencias | Todos |
| `/iphones` | Gestión de iPhones Usados | Todos |
| `/rewards` | Administrar TecPoints / Rewards | Todos |
| `/finanzas` | Finanzas, Caja Parada, Intereses | 🔒 Solo Admin |
| `/configuracion` | Configuración del Sistema | 🔒 Solo Admin |
| `/auditoria` | Logs y Auditoría del Sistema | 🔒 Solo Admin |

### Funcionalidades Transversales
- **`GlobalSearch`** — Buscador global por teclado (Ctrl+K) para encontrar productos, ventas o clientes
- **`PresenceToast`** — Indicador en tiempo real de qué usuarios están conectados al sistema
- **Rutas protegidas** — Middleware `ProtectedRoute` con validación de rol admin
- **Títulos dinámicos** — Cada ruta actualiza el `document.title` automáticamente

---

## 🛒 Módulo de Ventas

El módulo más operativo del día a día. Gestiona todo el ciclo de vida de una venta.

**Componentes principales** (12 archivos, ~280KB de código):

| Componente | Función |
|------------|---------|
| **`SalesManager`** | Panel principal: listado de ventas con filtros, búsqueda y estados |
| **`NewSaleForm`** (47KB) | Formulario completo de nueva venta: selección de productos, cliente, envío, pagos |
| **`SaleDetailsModal`** (44KB) | Modal de detalle con vista completa de cada venta |
| **`WebOrdersManager`** (32KB) | Gestión de pedidos que llegan desde la web pública |
| **`CustomerModal`** | ABM de clientes con datos de contacto |
| **`CustomerProfileModal`** | Perfil completo del cliente: historial de compras, puntos, etc. |
| **`DeliverySection`** / **`DeliveryItemsSection`** | Configuración de envío dentro de la venta |
| **`PaymentSection`** / **`PaymentsSection`** | Gestión de formas de pago (efectivo, transferencia, cuotas) |
| **`PurchasesPanel`** | Vista rápida de compras asociadas |
| **`RewardsManager`** (43KB) | Administración completa del programa TecPoints |

---

## 📦 Módulo de Catálogo y Compras

Gestiona los productos, proveedores y el abastecimiento del negocio.

**Componentes principales** (7 archivos, ~248KB de código):

| Componente | Función |
|------------|---------|
| **`ProductsManager`** (30KB) | ABM completo de productos con categorías, subcategorías, precios, costos y fees |
| **`WebStoreManager`** (115KB) | **El componente más grande del sistema.** Panel de gestión de la tienda online: sincronización de precios con MercadoLibre, gestión de variantes, imágenes, slugs, ofertas y publicación hacia la web |
| **`PurchasesManager`** | Listado y gestión de órdenes de compra a proveedores |
| **`NewPurchaseForm`** (25KB) | Formulario de nueva compra con ingreso parcial de productos |
| **`PurchaseDetailsModal`** (57KB) | Detalle exhaustivo de cada compra con estado de pagos |
| **`PurchasePayments`** | Gestión de pagos a proveedores |
| **`ProviderModal`** | ABM de proveedores |

---

## 🚚 Módulo de Logística e Inventario

Control total del stock en múltiples ubicaciones físicas y movimiento de mercadería.

**Componentes principales** (9 archivos, ~192KB de código):

| Componente | Función |
|------------|---------|
| **`LogisticsDashboard`** (19KB) | Dashboard de logística con métricas y estado general |
| **`StockMatrix`** (25KB) | **Matriz de stock** — Vista cruzada producto × ubicación con cantidades en tiempo real |
| **`StockCensus`** (39KB) | **Censo de stock** — Herramienta de auditoría física para verificar stock real vs. sistema |
| **`InventoryManager`** | Gestión de movimientos de inventario automáticos |
| **`StockMovementsHistory`** (17KB) | Historial completo de todos los movimientos de stock |
| **`TransfersManager`** (24KB) | Gestión de transferencias de mercadería entre sucursales |
| **`NewTransferForm`** (19KB) | Formulario de nueva transferencia entre ubicaciones |
| **`TransferModal`** | Detalle de cada transferencia |
| **`PendingDispatchView`** (26KB) | Vista de despachos pendientes con acciones masivas |

### Lógica de Base de Datos para Inventario
El sistema cuenta con **triggers automáticos en PostgreSQL** que actualizan el stock en tiempo real cada vez que se registra una venta, compra, transferencia o ajuste. Las migraciones SQL incluyen:
- `setup_inventory_movements_trigger.sql` — Trigger de movimientos automáticos
- `setup_stock_controls.sql` — Controles de stock con RLS
- `fix_ghost_transit_stock.sql` — Corrección de stock fantasma en tránsito
- `sync_iphones_batches.sql` — Sincronización de lotes de iPhones

---

## 💰 Módulo Financiero — Caja Parada, Intereses y Cierres

El módulo más complejo del ecosistema. Gestiona la contabilidad entre socios, el flujo de caja, gastos, y el sistema de penalidades.

**Componentes principales** (10 archivos, ~263KB de código):

| Componente | Función |
|------------|---------|
| **`FinanceManager`** (28KB) | Panel central financiero con navegación entre submódulos |
| **`CashFlowView`** (41KB) | **Flujo de Caja** — Vista completa de ingresos y egresos con filtros temporales |
| **`PenaltyDashboard`** (54KB) | **Caja Parada** — Dashboard de penalidades por capital inactivo por sucursal |
| **`PartnerInterests`** (27KB) | **Intereses de Socios** — Motor financiero que calcula interés prorateado (2% mensual) sobre el capital diario de cada socio |
| **`InterestDashboard`** | Vista resumida del módulo de intereses |
| **`ExpensesList`** (15KB) | Listado de gastos del negocio |
| **`NewExpenseModal`** (36KB) | Formulario para registrar nuevos gastos con categorización |
| **`MonthlyClosingModal`** (32KB) | **Cierre Mensual** — Proceso que consolida todas las operaciones del mes y genera el balance |
| **`ClosingHistory`** (14KB) | Historial de cierres mensuales anteriores |
| **`CompanyAssetsManager`** (13KB) | Gestión de activos de la empresa |

### Sistema de Caja Parada e Intereses

Este módulo implementa un **motor financiero de asientos diarios**:

```
  📅 El motor financiero calcula automáticamente:

  Para cada socio (Agustín, Lautaro, Matías):
  ┌─────────────────────────────────────────────────────────┐
  │  1. Lee el historial de aportes y retiros               │
  │  2. Arma la curva del capital día por día                │
  │  3. Determina si el saldo es POSITIVO o NEGATIVO        │
  │  4. Proratea el 2% mensual de interés por día           │
  │  5. Si hay capital ocioso → Penalidad "Caja Parada"     │
  │  6. Si hay deuda → Intereses a pagar                    │
  │  7. Asientos dobles de inversión/reinversión             │
  │     (ingreso + egreso cruzado sin romper el cashflow)    │
  └─────────────────────────────────────────────────────────┘
```

### Migraciones SQL Financieras
- `diagnostico_financiero.sql` — Procedimientos de diagnóstico
- `penalty_records.sql` — Estructura de registros de penalidades
- `penalty_improvements.sql` — Mejoras al sistema
- `monthly_closings.sql` — Estructura de cierres mensuales
- `system_settings.sql` — Configuraciones del sistema (tasas, fechas de corte)

---

## 📱 Módulo de iPhones Usados

Un módulo completo y especializado para la **compra-venta de dispositivos Apple reacondicionados**.

**Componentes principales** (9 archivos, ~170KB de código):

| Componente | Función |
|------------|---------|
| **`IphonesManager`** (40KB) | Panel principal: listado de todos los dispositivos con estados, filtros y dashboard de métricas |
| **`PhoneModalForm`** (51KB) | Formulario completo de ingreso/edición de un dispositivo con campos dinámicos por modelo |
| **`PhoneQuoterModal`** (20KB) | **Cotizador inteligente** — Herramienta que calcula el precio de compra sugerido basado en modelo, capacidad, batería y estado |
| **`PhoneSettingsModal`** (28KB) | Configuración de modelos, colores y precios de referencia |
| **`LabelPrinter`** | Generador de etiquetas con código de barras para cada dispositivo |
| **`AnimatedGuides`** | Guías visuales animadas para el checkout de dispositivos |

### Base de Datos para iPhones
- `setup_iphone_model_colors.sql` — Catálogo de modelos y colores disponibles
- `sync_iphones_batches.sql` — Sincronización de lotes
- Cada iPhone se trackea individualmente con IMEI, estado de batería, estado cosmético y precio

---

## 🏆 Módulo de Rewards (TecPoints)

Sistema de **fidelización gamificado** que premia a los clientes por sus compras y actividad.

### En el Sistema (Admin)
- **`RewardsManager`** (43KB) — Panel de administración: ver todos los puntos otorgados, gestionar misiones, auditar logs de rewards

### En la Web (Cliente)
- **`/rewards`** (19KB) — Dashboard personal con puntos acumulados y misiones disponibles
- **`/kiosco`** — Tienda de canje: los clientes intercambian TecPoints por descuentos y premios
- **`/ruleta`** (19KB) — Ruleta promocional con validación de código de compra

### Base de Datos de Rewards (8 migraciones SQL)
- `tecstore_rewards_schema.sql` — Esquema completo
- `rewards_trigger.sql` — Trigger que otorga puntos automáticamente al procesar una venta
- `missions_trigger.sql` — Sistema de misiones (comprar X veces, etc.)
- `rewards_kiosco.sql` — Catálogo de premios canjeables
- `sale_spins.sql` — Giros de ruleta vinculados a ventas
- `ruleta_premios.sql` + `dynamic_ruleta_prizes.sql` — Premios dinámicos configurables

---

## 🔄 Sincronización con MercadoLibre

El módulo **WebStoreManager** (115KB — el componente más grande del sistema) gestiona la presencia de TecStore en MercadoLibre.

### El Desafío
MercadoLibre tiene protecciones **WAF agresivas** que bloquean requests automatizados desde servidores (como Vercel).

### La Solución

```
  ┌──────────────────┐     ┌──────────────────────┐     ┌────────────────┐
  │  WebStoreManager  │     │   Proxy Serverless    │     │  MercadoLibre  │
  │  (React)          │────►│  (Google Apps Script) │────►│    API         │
  │                   │     │                       │     │                │
  │  Gestión de:      │     │  • Bypass WAF         │     │  • Precios     │
  │  • Precios        │     │  • Free tier          │     │  • Stock       │
  │  • Variantes      │     │  • Requests desde IP  │     │                │
  │  • Ofertas        │     │    de Google           │     │                │
  │  • Imágenes       │     │                       │     │                │
  └──────────────────┘     └───────────────────────┘     └────────────────┘
```

- **`api/ml-price.js`** — Endpoint serverless en Vercel que orquesta la consulta
- **Google Apps Script** — Proxy intermedio que evita bloqueos WAF
- **`ml_price_reference.sql`** — Tabla de referencia de precios MercadoLibre en la DB
- Soporte de conversión de tipos (`"$15.990,50"` → `15990.50`) para evitar errores de casting

---

## 🛡️ Seguridad e Inteligencia Artificial

### Seguridad (3 fases de hardening)
El sistema pasó por **tres fases de endurecimiento de seguridad** documentadas en las migraciones SQL:

- **`security_hardening.sql`** (9.4KB) — Fase 1: Políticas RLS iniciales
- **`security_hardening_phase2.sql`** (3.4KB) — Fase 2: Refuerzo de políticas
- **`security_hardening_phase3.sql`** (14KB) — Fase 3: Hardening completo con control granular por acción y rol

Además:
- **`audit_logs.sql`** — Sistema de auditoría que registra cada acción crítica
- **`trigger_audit_rewards.sql`** — Auditoría específica para movimientos de rewards
- **Sanitización XSS** — Uso de `DOMPurify` para prevenir inyecciones, eliminación de `dangerouslySetInnerHTML`
- **Protección de secretos** — Migración de API keys al servidor (Edge Functions)

### Inteligencia Artificial
- **`gemini-proxy`** (Supabase Edge Function) — Proxy seguro para consultas a Google Gemini
- Utilizado para **autocompletado inteligente** de datos de productos (especificaciones, descripciones)
- La lógica de IA fue removida del frontend y migrada a Edge Functions para proteger las API keys y límites de facturación

---

## 🔗 Cómo se Relacionan Web y Sistema

La Web y el Sistema son dos aplicaciones separadas que comparten la **misma base de datos Supabase**:

```
  CLIENTE compra en tecstore-web (Next.js)
        │
        ▼
  Supabase registra el pedido (web_orders)
        │
        ├──► Trigger calcula TecPoints automáticamente
        │         rewards_trigger.sql
        │
        ▼
  SistemaVentaTec muestra el pedido en WebOrdersManager
        │
        ▼
  Empleado procesa la venta → NewSaleForm
        │
        ├──► Stock se actualiza vía trigger
        │         inventory_movements_trigger.sql
        │
        ├──► Cliente ve el estado en /seguimiento
        │
        ├──► Finanzas registra el ingreso en CashFlow
        │
        └──► Rewards otorga puntos automáticamente
                  → Cliente los ve en /rewards y puede
                    canjear en /kiosco
```

**Todo está interconectado.** Una sola venta dispara una cadena automática de actualización de stock, cálculo de puntos, registro financiero y tracking de envío.

---

## 📊 Impacto Real

| Métrica | Antes | Después | Mejora |
|---------|:-----:|:-------:|:------:|
| Registro de una venta | ~8 min (manual) | **< 1 min** (formulario guiado) | **87%** |
| Control de stock | Planilla con errores | **Tiempo real multi-sucursal** con triggers | **~100%** |
| Sincronización de precios ML | ~2 hs/día (uno por uno) | **Masivo en minutos** | **97%** |
| Auditoría financiera de socios | 1 vez/mes (manual) | **Automática diaria** con interés prorrateado | **30x** |
| Cierre mensual contable | ~1 día completo | **1 click** (MonthlyClosingModal) | **95%** |
| Consultas de tracking | Respuestas manuales | **Autoservicio en /seguimiento** | **100%** |
| Fidelización de clientes | Inexistente | **TecPoints + Misiones + Kiosco + Ruleta** | ∞ |
| Cotización de usados | A ojo / experiencia | **Cotizador con fórmula** por modelo y estado | **100%** |
| Errores de stock fantasma | ~15/semana | **< 1/mes** | **98%** |

### Impacto en el Negocio

| Área | Resultado |
|------|-----------|
| **Código** | +600KB solo de componentes React entre ambos proyectos. 70+ migraciones SQL. |
| **Escalabilidad** | El negocio triplicó su volumen sin agregar personal operativo |
| **Transparencia** | Los socios ven su estado contable con precisión diaria |
| **Experiencia del cliente** | Tracking, rewards, cotizador, dark mode, carrito — todo self-service |
| **Seguridad** | 3 fases de hardening, RLS granular, Edge Functions para IA, sanitización XSS |
| **Infraestructura** | Todo en Supabase free tier + Vercel — costos operativos mínimos |

---

## 🛠️ Stack Tecnológico Completo

<div align="center">

| Categoría | Web (tecstore-web) | Sistema (SistemaVentaTec) |
|:---------:|:------------------:|:-------------------------:|
| **Framework** | Next.js 14 | React 19 + Vite |
| **Lenguaje** | TypeScript | JavaScript (JSX) |
| **Estilos** | Tailwind CSS | Tailwind CSS |
| **Base de Datos** | Supabase (PostgreSQL) | Supabase (PostgreSQL) |
| **State** | Zustand | React Context + SWR |
| **Animaciones** | Framer Motion | CSS + SweetAlert2 |
| **Gráficos** | — | Recharts |
| **PDFs** | — | jsPDF + AutoTable |
| **Barcodes** | — | react-barcode |
| **Temas** | next-themes | — |
| **Auth** | Supabase Auth | Supabase Auth |
| **IA** | — | Gemini (Edge Function) |
| **Deploy** | Vercel | Vercel |
| **SEO** | sitemap.ts + robots.ts | — |
| **Analytics** | — | Vercel Analytics + GA4 |
| **Security** | RLS + Auth | RLS + DOMPurify + Admin Routes |

</div>

---

<div align="center">

<br>

> *"TecStore no es solo un e-commerce. Es un ecosistema de software construido internamente que conecta cada operación del negocio — desde que un proveedor factura hasta que el cliente recibe su paquete y acumula puntos por ello."*

<br>

**[⬅️ Volver al Perfil Principal](./README.md)**

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=120&section=footer"/>
