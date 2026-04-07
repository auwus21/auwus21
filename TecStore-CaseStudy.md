<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=180&section=header&text=TecStore%20Backoffice&fontColor=58A6FF&fontSize=36&fontAlignY=35&desc=Caso%20de%20Estudio%20T%C3%A9cnico%20%E2%80%94%20Software%20Privado%20Empresarial&descAlignY=55&descSize=14&descColor=8B949E&animation=fadeIn"/>

<div align="center">

![Privado](https://img.shields.io/badge/Estado-Privado%20Empresarial-red?style=for-the-badge&logo=lock&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Google Apps Script](https://img.shields.io/badge/Apps%20Script-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Shopify](https://img.shields.io/badge/Shopify-96BF48?style=for-the-badge&logo=shopify&logoColor=white)

</div>

> [!NOTE]
> Este proyecto es de **código cerrado** por políticas de seguridad interna de TecStore Argentina. Este documento sirve como una vista ilustrativa de la arquitectura, los sistemas y los problemas resueltos.

---

## 🏢 Overview

**TecStore** es una plataforma tecnológica integral construida desde cero para gestionar y optimizar toda la infraestructura operativa, financiera y logística de *TecStore Argentina* — una de las marcas líderes de e-commerce tech del país con **+300.000 seguidores en Instagram**.

El sistema centraliza múltiples fuentes de verdad que de otro modo estarían dispersas entre planillas, procesos manuales y herramientas desconectadas — transformándolas en un hub de operaciones unificado y automatizado.

---

## 🏗️ Arquitectura y Tecnologías

```
┌─────────────────────────────────────────────────┐
│                CAPA FRONTEND                     │
│        React Admin Dashboards (Custom)           │
├──────────────────┬──────────────────────────────┤
│                  │                               │
│   BACKEND CORE   │     CAPA DE INTEGRACIONES     │
│   Node.js        │     Shopify API               │
│   Google Apps    │     MercadoLibre API           │
│   Script         │     WhatsApp Business (BaaS)   │
│                  │     Proxy Serverless           │
├──────────────────┴──────────────────────────────┤
│                  CAPA DE DATOS                   │
│   Google Sheets (Data Warehouse Operativo)       │
│   Bases de Datos Transaccionales (Caché)         │
└─────────────────────────────────────────────────┘
```

---

## ⚙️ Módulos de Operación

### 💰 Motor Financiero — Sistema de "Caja Parada"

Un sofisticado motor de asientos diarios diseñado para auditar las cuentas de los socios con precisión:

- **Seguimiento de saldos diario** con estados positivos y negativos (deudores)
- **Scripts de recálculo dinámico** soportando modelos de interés compuesto y simple
- **Registros inmutables de penalidades** y devengamientos automáticos de "Intereses a Pagar" activados en condiciones de caja inactiva
- Integración directa con el dashboard contable para visibilidad en tiempo real

### 🚚 Módulo de Logística Inteligente

Gestión logística de punta a punta que impulsa tanto las operaciones internas como la experiencia del cliente:

- **Panel de gestión masiva de estados** — herramienta de backoffice para actualización masiva de estados de envío de cientos de pedidos activos
- **Automatizaciones push por WhatsApp** — notificaciones instantáneas a empleados sobre llegadas y a clientes sobre cambios de estado
- **Plataforma pública de tracking** — una web app en React donde los clientes ingresan un código de seguimiento y ven barras de progreso animadas sincronizadas a la base logística en tiempo real

### 🔄 Syncer de Inventario Cross-Plataforma

Un motor de sincronización de alto volumen y alta fiabilidad que conecta Shopify con MercadoLibre:

- **Capa proxy serverless** — API proxy custom deployada en Google Cloud Functions que evita silenciosamente los rate limits WAF y bloqueos de requests
- **Flujo de datos bidireccional** — transforma e inyecta datos de inventario en ambas plataformas en tiempo real, eliminando falsos negativos de stock
- **Infraestructura a costo cero** — todo el proxy corre dentro del free-tier de cómputo serverless, optimizando costos operativos

---

## 📊 Impacto

| Métrica | Antes | Después |
|---------|-------|---------|
| Tiempo de carga manual de datos | ~4 hs/día | **Completamente automatizado** |
| Precisión de sincronización de inventario | ~85% (manual) | **99.9% en tiempo real** |
| Consultas logísticas de clientes | Respuestas manuales por WhatsApp | **Tracking autoservicio** |
| Auditoría financiera | Revisión manual mensual | **Libro diario automatizado** |

---

<div align="center">

**[⬅️ Volver al Perfil Principal](./README.md)**

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=120&section=footer"/>
