<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=180&section=header&text=TecStore%20Backoffice&fontColor=58A6FF&fontSize=36&fontAlignY=35&desc=Technical%20Case%20Study%20%E2%80%94%20Private%20Enterprise%20Software&descAlignY=55&descSize=14&descColor=8B949E&animation=fadeIn"/>

<div align="center">

![Private](https://img.shields.io/badge/Status-Private%20Enterprise-red?style=for-the-badge&logo=lock&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Google Apps Script](https://img.shields.io/badge/Apps%20Script-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Shopify](https://img.shields.io/badge/Shopify-96BF48?style=for-the-badge&logo=shopify&logoColor=white)

</div>

> [!NOTE]
> This project is **closed-source** due to internal business security policies at TecStore Argentina. This document serves as an illustrative overview of the architecture, systems, and problems solved.

---

## 🏢 Overview

**TecStore** is a comprehensive internal technology platform built from the ground up to manage and optimize the entire operational, financial, and logistics infrastructure of *TecStore Argentina* — one of the country's leading tech e-commerce brands with **300,000+ followers on Instagram**.

The system centralizes multiple sources of truth that would otherwise be scattered across spreadsheets, manual processes, and disconnected tools — transforming them into a unified, automated operations hub.

---

## 🏗️ Architecture & Technologies

```
┌─────────────────────────────────────────────────┐
│                  FRONTEND LAYER                  │
│          React Admin Dashboards (Custom)         │
├──────────────────┬──────────────────────────────┤
│                  │                               │
│   BACKEND CORE   │     INTEGRATIONS LAYER        │
│   Node.js        │     Shopify API               │
│   Google Apps    │     MercadoLibre API           │
│   Script         │     WhatsApp Business (BaaS)   │
│                  │     Serverless Proxy           │
├──────────────────┴──────────────────────────────┤
│                  DATA LAYER                      │
│   Google Sheets (Operational Data Warehouse)     │
│   Transactional Cache DBs                        │
└─────────────────────────────────────────────────┘
```

---

## ⚙️ Core Modules

### 💰 Financial Engine — "Caja Parada" System

A sophisticated daily-ledger financial engine designed to audit partner accounts with precision:

- **Daily balance tracking** across positive and negative (debtor) states
- **Dynamic recalculation scripts** supporting both compound and simple interest models
- **Immutable penalty records** and automated "Intereses a Pagar" accruals triggered on idle-cash conditions
- Seamless integration with the accounting dashboard for real-time visibility

### 🚚 Intelligent Logistics Module

End-to-end logistics management powering both the internal operations team and customer-facing experiences:

- **Bulk status management panel** — backoffice tool for mass-updating shipment states across hundreds of active orders
- **WhatsApp push automations** — instant notifications to employees on arrivals and to customers on status changes
- **Public tracking platform** — a React-powered web app where customers enter a tracking code and see animated progress bars synced to the logistics database in real time

### 🔄 Cross-Platform Inventory Syncer

A high-volume, high-reliability synchronization engine bridging the gap between Shopify and MercadoLibre:

- **Serverless proxy layer** — custom API proxy deployed on Google Cloud Functions that silently bypasses WAF rate limiting and request blocks
- **Bidirectional data flow** — transforms and injects inventory data into both platforms in real time, eliminating false-negative stock-outs
- **Zero-cost infrastructure** — the entire proxy runs within free-tier serverless compute, optimizing operational costs

---

## 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Manual data entry time | ~4 hrs/day | **Fully automated** |
| Inventory sync accuracy | ~85% (manual) | **99.9% real-time** |
| Customer logistics queries | Manual WhatsApp replies | **Self-service tracking** |
| Financial auditing | Monthly manual review | **Daily automated ledger** |

---

<div align="center">

**[⬅️ Back to Main Profile](./README.md)**

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=120&section=footer"/>
