# 🛒 Ecosistema Backoffice TecStore

> [!NOTE]
> Este proyecto es de código cerrado por políticas de seguridad interna del negocio. Este documento sirve a modo ilustrativo sobre la arquitectura implementada y los procesos resueltos.

**TecStore** es una plataforma tecnológica integral desarrollada internamente para gestionar y optimizar toda la estructura operativa, contable y logística de *TecStore Argentina*. Su objetivo es centralizar fuentes de verdad que de otro modo estarían diseminadas.

## 🚀 Arquitectura y Tecnologías
- **Frontend Admin:** Interfaces en React diseñadas a medida para los empleados y directivos.
- **Backend Core:** Desarrollos bajo Node.js, apoyados fuertemente en macros y scripts serverless usando **Google Apps Script**.
- **Base de Datos Dinámica:** Google Sheets como Data Warehousing operativo para facilitar la visibilidad a ejecutivos en tiempo real, junto con bases de datos transaccionales de caché para el e-commerce.
- **Integraciones Críticas:** Shopify API, WhatsApp Business Web (BaaS), y MercadoLibre.

## ⚙️ Módulos de Operación

### 1. Módulo Financiero y Sistema de "Caja Parada"
Para auditar correctamente a los socios, se desarrolló un sofisticado motor financiero de asientos diarios:
- Seguimiento de saldos con balances positivos o deudores.
- Script de recálculo dinámico con interés compuesto/simple.
- Registro inmutable de penalizaciones e "Intereses a Pagar" automatizados en caso de "Caja Parada".

### 2. Logística Inteligente
A través de un portal propio, el negocio despacha sus envíos actualizando una base de datos maestra que impacta en los clientes:
- Panel backoffice de cambio masivo de estados logísticos con automatizaciones de WhatsApp para dar aviso instantáneo a empleados o clientes particulares.
- Plataforma pública de consulta de tracking vinculada mediante Node.js a la DB en Google Sheets (con UI y animaciones de progreso de envío).

### 3. Sincronización Masiva Cross-Plataforma
Dado el volumen de ventas e inventarios, el proyecto cuenta con un sistema de enlace bidireccional entre MercadoLibre y Shopify:
- Herramienta que supera desafíos técnicos (como los WAF limits / bloqueos de request) utilizando una API Proxy desplegada silenciosamente de forma gratuita, transformando la data e inyectándola al portal en tiempo real sin falsos negativos de stock.

---
[⬅️ Volver al Perfil Principal](./README.md)
