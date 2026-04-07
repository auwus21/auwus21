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
> Este proyecto es de **código cerrado** por políticas de seguridad interna del negocio. Este documento sirve como vista ilustrativa de la arquitectura, los módulos construidos y los problemas técnicos resueltos. Los datos sensibles de infraestructura y nombres de arquitecturas internas han sido ofuscados por privacidad.

---

## 📖 Tabla de Contenidos

- [El Problema](#-el-problema--por-qué-surgió-este-proyecto)
- [Arquitectura General](#-arquitectura-general)
- [La Web Pública](#-la-web-pública)
- [El Sistema Backoffice](#-el-sistema-backoffice)
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

El negocio originalmente funcionaba con herramientas genéricas. No existía un sistema centralizado: el stock se controlaba en planillas, los envíos se comunicaban manualmente, la contabilidad interna se revisaba esporádicamente, y los precios externos se actualizaban uno por uno.

**El negocio estaba creciendo más rápido que la infraestructura que lo sostenía.** Cada semana había riesgos de errores operativos: desincronización de inventario, precios desactualizados en marketplaces y falta de reportes financieros en tiempo real.

Surgió la necesidad de construir — desde cero — un **ecosistema tecnológico completo** con dos grandes pilares: un **sistema interno de gestión** (backoffice) y una **web pública e-commerce**, ambos conectados a una misma base de datos en la nube.

---

## 🏗️ Arquitectura General

El ecosistema se divide en dos aplicaciones independientes que comparten una capa de datos centralizada en **PostgreSQL (Supabase)**:

```
╔══════════════════════════════════════════════════════════════════════════╗
║                          ECOSISTEMA TECSTORE                            ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   ┌──────────────────────┐            ┌───────────────────────────┐     ║
║   │    🌐 LA WEB          │            │    ⚙️ EL SISTEMA           │     ║
║   │   (Cliente Final)     │            │   (Backoffice Interno)    │     ║
║   │                      │            │                           │     ║
║   │  Next.js 14 + TS     │            │  React 19 + Vite          │     ║
║   │  Framer Motion       │            │  Tailwind CSS             │     ║
║   │  Zustand             │◄──────────►│  Recharts                 │     ║
║   │  next-themes         │            │  SWR                      │     ║
║   │                      │            │  Visualización PDF        │     ║
║   │  ─────────────────   │            │  ─────────────────────    │     ║
║   │  • Catálogo público  │            │  • Dashboard General      │     ║
║   │  • Carrito + Checkout│            │  • Ventas + Pedidos Web   │     ║
║   │  • Seguimiento envíos│            │  • Compras + Proveedores  │     ║
║   │  • Rewards / Kiosco  │            │  • Logística + Inventario │     ║
║   │  • Ruleta promo      │            │  • Finanzas + Inversiones │     ║
║   │  • Cotizador usados  │            │  • Cotizador Interno      │     ║
║   │  • Perfil de usuario │            │  • Gestión de Fidelidad   │     ║
║   └──────────┬───────────┘            └─────────────┬─────────────┘     ║
║              │                                       │                   ║
║              └───────────────┬───────────────────────┘                   ║
║                              │                                           ║
║                 ┌────────────▼──────────────────┐                       ║
║                 │     🗄️ BACKEND CORE            │                       ║
║                 │                                │                       ║
║                 │  • Base de datos relacional    │                       ║
║                 │  • Políticas de acceso (RLS)   │                       ║
║                 │  • Edge Functions (IA)         │                       ║
║                 │  • Triggers para automatización│                       ║
║                 │  • Procedimientos almacenados  │                       ║
║                 └────────────────────────────────┘                       ║
║                              │                                           ║
║                 ┌────────────▼──────────────────┐                       ║
║                 │     🔗 INTEGRACIONES           │                       ║
║                 │                                │                       ║
║                 │  • Proxy para Marketplaces     │                       ║
║                 │  • Serverless Functions        │                       ║
║                 │  • Motor de IA (Google)        │                       ║
║                 └────────────────────────────────┘                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🌐 La Web Pública

La cara visible del negocio. Una **aplicación Next.js 14 con TypeScript** completa que funciona como e-commerce, portal de clientes y plataforma de fidelización.

### Tecnologías Utama
- **Framework:** Next.js 14 (App Router)
- **Lenguaje:** TypeScript
- **Estilos y Animaciones:** Tailwind CSS, Framer Motion
- **Estado Global:** Zustand
- **Modo Oscuro:** next-themes

### Componentes Clave del E-Commerce
- **Catálogo y Checkout:** Flujo de compra optimizado con sidebar persistente y búsqueda global de baja latencia.
- **Logística Integrada:** Portal de tracking (seguimiento) donde el cliente visualiza el estado animado de su paquete en tiempo real, conectado directamente al backoffice.
- **Cotizador de Dispositivos:** Aplicación web embebida que valora automáticamente los equipos usados de los clientes que deseen dejarlos en parte de pago.
- **Fidelización y Gamificación:** Un portal propio para los "TecPoints" con sistema de misiones, un kiosco de canje, y una ruleta interactiva para campañas promocionales mediante validación criptográfica de órdenes de compra.

---

## ⚙️ El Sistema Backoffice

El corazón operativo. Es una **Single Page Application en React 19** que el equipo y los directivos usan para operar el negocio minuto a minuto. 

### Tecnologías Utama
- **Framework:** React 19 (Vite)
- **Data Fetching:** SWR (stale-while-revalidate) para sincronización optimista.
- **Análisis de Datos:** Recharts para visualización de métricas.
- **Impresiones Físicas:** Generación dinámica de etiquetas, códigos de barras y resúmenes PDF.

### Funcionalidades Transversales
- **Búsqueda Global y Comandos:** Navegación por teclado (Ctrl+K) similar a un IDE para localizar rápidamente órdenes, productos o clientes.
- **Conectividad en Tiempo Real:** Indicadores de usuarios concurrentes operando en las sucursales.
- **Seguridad Perimetral:** Middleware interno para validar permisos y accesos específicos por rol directivo o empleado.

---

## 🛒 Módulo de Ventas

Gestiona todo el ciclo de vida de una transacción, integrando el flujo online y el punto de venta (POS).

- **Gestión Unificada:** Consolidación de los pedidos provenientes de la web con las ventas generadas en la sucursal física.
- **Formularios Dinámicos:** Alta de ventas complejas con cálculos automáticos de retenciones, cuotas, entregas parceladas y múltiples métodos de pago combinados.
- **Perfiles 360° del Cliente:** Consulta instantánea del historial comercial de cada persona (compras anteriores, puntos de fidelidad acumulados, disputas).
- **Asignación de Logística:** Preparación inmediata de la orden de envío directamente desde el POS.

---

## 📦 Módulo de Catálogo y Compras

Control integral del reabastecimiento y la vidriera comercial.

- **Administración del Catálogo:** Gestión de variantes, carga eficiente de multimedia (optimizada al vuelo) y estructuras jerárquicas de categorías.
- **Sincronizador Híbrido:** Gestión del inventario para la tienda online propia y publicación hacia marketplaces de terceros.
- **Motor de Compras a Proveedores:** Seguimiento de facturas, pagos paciales y automatización en la entrada del inventario cuando arriban los lotes físicos.

---

## 🚚 Módulo de Logística e Inventario

Control estricto con trazabilidad del 100% en las existencias físicas distribuidas en múltiples ubicaciones.

- **Matriz Analítica de Stock:** Cruce de datos entre productos y sucursales/depósitos para facilitar la reubicación de mercadería.
- **Auditorías Físicas (Censo):** Módulo tipo "escáner ciego" para conciliar el conteo físico del personal contra los números del sistema y ajustar discrepancias.
- **Despachos Masivos:** Panel estilo Kanban para armar grupos de envío y procesar estados de envíos ("Preparado", "Despachado") que dispara notificaciones automáticas al cliente.
- **Automatización SQL:** La base de datos opera con triggers nativos; toda venta, compra o devolución efectúa el ajuste de stock sin intervención de la capa de aplicación, asegurando integridad total (ACID).

---

## 💰 Módulo Financiero — Diagnósticos, Intereses y Cierres

El módulo más avanzado desde el punto de vista arquitectónico, que resuelve la necesidad de los inversores de mantener control exacto de su capital.

- **CashFlow Inmutable:** Un registro financiero donde ningún movimiento contable puede ser simplemente "borrado", operando bajo estrictos principios de partida doble y cierres periódicos.
- **Panel de Capital y Inversiones:** Análisis visual para directivos sobre rentabilidades y activos fijos.
- **Cierres Mensuales a 1 Click:** Rutina que compila automáticamente la facturación, los descuentos, las pérdidas de stock y liquida márgenes de rentabilidad, exportando la contabilidad.

### Motor de Intereses Prorrateados
El negocio fue implementado de modo que el capital que no está circulando activamente recibe recargos ("Caja inactiva"), mientras que hay balances de socios inversores fluctuando diariamente:

```
  📅 El motor financiero en la nube efectúa cortes en el tiempo:

  1. Reconstruye la curva de saldo para cada aportante desde sus movimientos.
  2. Determina exactamente cuántos días un saldo estuvo en positivo o negativo.
  3. Ejecuta cálculos de interés simple y compuesto para devengar montos.
  4. Genera automáticamente los asientos de reinversión para cuadrar el 
     balance general sin distorsionar la facturación del negocio.
```

---

## 📱 Módulo de Equipos Reacondicionados

Un segmento altamente dinámico orientado a dispositivos electrónicos usados.

- **Ciclo de Vida Individual:** Cada equipo se registra e ingresa al inventario mediante su código de serie (IMEI), especificando su estado cosmético, salud de batería e historial de reparaciones.
- **Cotizador Inteligente Interno:** Algoritmo que cruza el costo de reposición vigente en el mercado con las penalizaciones por desgaste, sugiriendo un margen de compra óptimo al vendedor que toma el equipo.
- **Generación de Etiquetas:** Creación instantánea de etiquetas en formato térmico para trazar el equipo por la trastienda.

---

## 🏆 Módulo de Rewards (Fidelización)

Mecanismo interno diseñado para incrementar el retorno recurrente del cliente (LTV).

- **Automatización Base de Datos:** La acumulación de puntos está blindada. Los disparadores de base de datos le dan un valor a la transacción y asignan puntos a la billetera digital del comprador.
- **Lógica de Misiones:** Un sistema asíncrono analiza los patrones (ej: "segunda compra en el mes") y desbloquea multiplicadores promocionales.
- **Soporte Administrativo:** Los supervisores cuentan con herramientas para otorgar puntos compensatorios, así como auditorías de canje para prevenir fraudes.

---

## 🔄 Sincronización Serverless de Precios Externos

Uno de los mayores desafíos del negocio era mantener miles de precios alineados con Marketplaces, dada la hiperinflación cambiaria periódica y los bloqueos por bots.

### Solución Serverless contra Firewalls
El marketplace de destino utiliza un Firewall de Aplicaciones Web (WAF) muy estricto que bloqueaba y banneaba las IPs de servidores comunes al intentar actualizar los listados automáticamente.

Se diseñó una arquitectura de mitigación de 3 capas:
1. **Frontend del Administrador:** Dictamina los márgenes de ganancia masivos deseados.
2. **Workers Intermedios:** Entorno serverless que orquesta la ejecución.
3. **Proxy de Nube Transparente:** Las peticiones son enrutadas a través de redes institucionales server-to-server externas gratuitas de alta reputación (que eluden los bloqueos).

**Resultado:** Se actualizaron catálogos inmensos con una latencia mínima de manera autónoma sin intervención manual, con un costo mensual de infraestructura externo de **$0**.

---

## 🛡️ Seguridad e IA (Inteligencia Artificial)

### Fases de Endurecimiento ("Hardening")
El sistema fue escalando sus políticas de seguridad (Row Level Security) hasta alcanzar un estándar corporativo:
- **Protección Perimetral:** Cada tabla valida la sesión a nivel de red antes de devolver un paquete de datos, garantizando que el personal de ventas no pueda alterar inventarios de otra sucursal u ojear finanzas.
- **Auditoría inmutable:** Todas las operaciones de alta jerarquía se replican en tablas de trazabilidad (Logs), adjuntando qué ID ejecutó la acción y bajo qué rol.
- **Sanitización Contra Ataques:** Protección contra Cross-Site Scripting (XSS) y parametrización de consultas nativas por la capa de acceso a datos.

### Empoderamiento por Inteligencia Artificial
La infraestructura integra LLMs (Large Language Models) para asistir en la confección de productos:
- Se levantó un microservicio (Edge Function) protegido que aloja las credenciales criptográficas, el cual oficia de intermediario para el modelo de IA de Google.
- Se utiliza la IA para categorizar y autocompletar especificaciones técnicas complejas en el catálogo, ahorrando horas operativas de data entry o formateo manual.

---

## 🔗 Relación Simbiótica (Web ↔ Sistema)

La arquitectura garantiza un flujo ininterrumpido sin APIs intermedias que sufran demoras de sincronización, compartiendo el mismo centro de datos en tiempo real:

```
  CLIENTE (Next.js)      ◄──────►      CAPA DE DATOS       ◄──────►      EMPLEADO (React)
  • Carga su carrito                   • Asegura el stock                • Ve que bajó el inventario
  • Completa la compra                 • Transacciona                    • Preparan el paquete y pulsan "Despachar"
  • Recibe "Puntos"                    • Registra métricas               • Finanzas lo ve liquidado en su flujo
```

Cada interacción del usuario final resuena de fondo generando **indicadores clave de rendimiento (KPIs)** en las pantallas gerenciales al instante.

---

## 📊 Impacto de la Implementación

| Proceso Manual (Anterior) | Mejora Autómata (Actual) |
|---------------------------|--------------------------|
| **Cierres Contables:** Complejos cruces a mano que llevaban una tarde. | **Un Clic:** Arroja proyecciones, rentabilidad neta y pasivos instantáneamente. |
| **Integridad de Inventario:** Inconsistencias, doble venta y quiebres de stock continuos. | **Tiempo Real Constricto:** El stock es el amo absoluto de la web y el mostrador simultáneamente. |
| **Campañas de Fidelización:** Proactivas y difíciles de contabilizar. | **Algorítmica:** Ruletas, incentivos, TecPoints — todo sucede solo de fondo. |
| **Control Societario:** Registros difusos sobre quién retiró fondos o cuándo. | **Motor Financiero Matemático:** Penaliza capital ocioso y premia al equipo, evitando desbalances ocultos. |
| **Soporte Postventa (Envíos):** Mensajes intermitentes uno a uno. | **Tracking Self-Service:** El cliente posee control de interfaz total que se mueve según el deósito empaca. |

### Conclusión Técnica
Esta infraestructura representa algo superior a una tienda online tradicional; es un **ERP operativo asíncrono y a escala**, orquestando desde el pricing externo en marketplaces hasta el control minucioso de stock usado, utilizando servicios gratuitos y arquitecturas serverless state-of-the-art para reducir el costo de servidor virtualmente a cero.

---

<div align="center">

<br>

**[⬅️ Volver al Perfil Principal](./README.md)**

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=120&section=footer"/>
