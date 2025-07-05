# 🤖 Chatbot Asistente con Agendamiento Inteligente

MCP de un chatbot inteligente que permite a los usuarios interactuar en lenguaje natural, programar reuniones automáticamente y recibir notificaciones, con soporte para recuperación semántica usando Qdrant (RAG).

![Python](https://img.shields.io/badge/backend-FastAPI-green?logo=fastapi)
![MongoDB](https://img.shields.io/badge/database-MongoDB-brightgreen?logo=mongodb)
![Qdrant](https://img.shields.io/badge/semantic%20search-Qdrant-purple?logo=qdrant)
![Slack](https://img.shields.io/badge/integration-Slack-blue?logo=slack)
![Google Calendar](https://img.shields.io/badge/calendar-Google--Calendar-red?logo=google-calendar)

---

## 🎯 Objetivo del Proyecto

Construir un chatbot conversacional que pueda:

- Responder preguntas en lenguaje natural
- Programar reuniones automáticamente en Google Calendar
- Enviar notificaciones o recordatorios por Slack
- Recordar conversaciones pasadas (memoria) por usuario
- Utilizar recuperación semántica (RAG) con Qdrant para sugerencias inteligentes

---

## 🧠 Tecnologías Usadas

| Componente     | Tecnología                        |
|----------------|-----------------------------------|
| Backend        | FastAPI + FastAPI-MCP             |
| Base de Datos  | MongoDB                           |
| Vector DB      | Qdrant                            |
| Embeddings     | SentenceTransformers + Groq       |
| Autenticación  | JWT (OAuth2 Bearer)               |
| Notificaciones | Slack API                         |
| Calendario     | Google Calendar API               |

---

## ⚙️ Funcionalidades Clave

### 1. 🗣️ Chatbot Interactivo
- Procesamiento de mensajes de usuario
- Respuestas personalizadas usando LLM
- Contexto dinámico vía RAG

### 2. 📅 Agendamiento Automático
- Crear eventos en Google Calendar desde el chat
- Herramienta conectada mediante `GoogleCalendarTool`

### 3. 🔔 Notificaciones Programadas
- Envío de recordatorios a Slack usando `SlackTool`
- Personalización de mensajes y canal

### 4. 🧠 RAG (Retrieval-Augmented Generation)
- Recuperación semántica con Qdrant
- Embeddings vectoriales y búsqueda contextual

### 5. 👤 Gestión de Usuarios
- Registro e inicio de sesión
- Autenticación JWT
- Roles: `admin`, `usuario`

---
