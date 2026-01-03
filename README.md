# Chatbot con OpenAI y Django

Sistema de chatbot conversacional desarrollado con Django y OpenAI que mantiene el contexto de conversación completo.
<img width="1402" height="902" alt="image" src="https://github.com/user-attachments/assets/3941b00d-a8f0-4ff0-a1f1-c01125bf2854" />

## Descripción

Este proyecto implementa un chatbot interactivo que utiliza un modelo fine-tuned personalizado basado en GPT-4o Nano de OpenAI. El modelo fue ajustado mediante la API de Fine-tuning de OpenAI para responder consultas específicas del dominio. El sistema mantiene el historial completo de conversación, permitiendo que el modelo tenga contexto de todos los mensajes anteriores.

## Características

- Modelo fine-tuned personalizado basado en GPT-4o Nano
- Conversaciones persistentes con historial completo
- Interfaz web responsive con diseño de chat moderno
- Gestión de múltiples conversaciones mediante sesiones de Django
- Base de datos SQLite para almacenamiento de mensajes
- Envío de contexto completo a OpenAI en cada interacción
- Sistema de avatares para distinguir usuario y asistente

## Estructura del Proyecto

```
chat-bot/
├── chatbot_openai/                 # Proyecto Django principal
│   ├── manage.py                   # Utilidad de administración Django
│   ├── db.sqlite3                  # Base de datos SQLite
│   │
│   ├── chatbot_openai/             # Configuración del proyecto
│   │   ├── settings.py             # Configuración general
│   │   ├── urls.py                 # Rutas principales
│   │   ├── wsgi.py                 # Configuración WSGI
│   │   └── asgi.py                 # Configuración ASGI
│   │
│   └── chat/                       # Aplicación del chatbot
│       ├── models.py               # Modelos de datos (Conversation, Message)
│       ├── views.py                # Lógica de vistas (HolaMundoView)
│       ├── urls.py                 # Rutas de la aplicación
│       ├── admin.py                # Configuración del admin
│       ├── migrations/             # Migraciones de base de datos
│       └── templates/
│           └── chat/
│               └── hola_mundo.html # Template principal del chat
│
└── chatenv/                        # Entorno virtual Python
```

## Modelos de Datos

### Conversation
Representa una conversación completa entre el usuario y el asistente.

```python
- id: Identificador único
- title: Título de la conversación (default: "Nueva conversación")
- created_at: Fecha de creación
- updated_at: Fecha de última actualización
```

### Message
Representa un mensaje individual dentro de una conversación.

```python
- id: Identificador único
- conversation: Referencia a la conversación (ForeignKey)
- content: Contenido del mensaje (texto)
- is_user: Boolean (True = usuario, False = asistente)
- timestamp: Fecha y hora del mensaje
- metadata: Información adicional en formato JSON (modelo usado, tokens, etc.)
```

## Flujo de Funcionamiento

### 1. Inicio de Conversación
- El usuario accede a la aplicación
- Se crea o recupera una conversación activa mediante sesiones Django
- Se cargan todos los mensajes previos de la conversación

### 2. Envío de Mensaje
1. Usuario escribe mensaje en el formulario
2. Se guarda el mensaje en la base de datos con `is_user=True`
3. Se recuperan TODOS los mensajes de la conversación
4. Se formatea el historial completo en formato de OpenAI:
   ```python
   [
       {"role": "user", "content": "mensaje 1"},
       {"role": "assistant", "content": "respuesta 1"},
       {"role": "user", "content": "mensaje 2"},
       ...
   ]
   ```
5. Se envía el contexto completo a la API de OpenAI
6. Se recibe y guarda la respuesta con `is_user=False`
7. Se actualiza la interfaz con todos los mensajes

### 3. Gestión del Contexto
- Cada mensaje incluye el historial completo de la conversación
- El modelo de OpenAI tiene acceso a todos los mensajes anteriores
- Permite respuestas contextuales y coherentes a lo largo de la conversación

## Requisitos

- Python 3.8+
- Django 4.x
- openai (biblioteca oficial de Python)
- SQLite (incluido con Python)

## Instalación

1. Crear y activar entorno virtual:
```bash
python -m venv chatenv
chatenv\Scripts\activate  # En Windows
```

2. Instalar dependencias:
```bash
pip install django openai
```

3. Ejecutar migraciones:
```bash
python manage.py migrate
```

4. Configurar API Key de OpenAI en `chat/views.py` (línea 6-7)

5. Iniciar servidor de desarrollo:
```bash
python manage.py runserver
```

6. Acceder a la aplicación:
```
http://localhost:8000/
```

## Uso

1. Abre la aplicación en tu navegador
2. Escribe un mensaje en el campo de texto
3. Presiona "Enviar" o Enter
4. El chatbot responderá manteniendo el contexto de la conversación
5. Para iniciar una nueva conversación, utiliza la función DELETE (si está implementada en el frontend)

## Detalles Técnicos

### Vista Principal (HolaMundoView)

**Métodos:**
- `GET`: Carga y muestra la conversación activa
- `POST`: Procesa mensajes nuevos y obtiene respuestas del modelo
- `DELETE`: Limpia la sesión para iniciar nueva conversación
- `_get_or_create_conversation()`: Gestiona conversaciones mediante sesiones

### Integración con OpenAI

**Endpoint usado:**
```python
client.chat.completions.create(
    model="",
    messages=messages_for_api
)
```

**Modelo:**
- Fine-tuned GPT-4.1 Nano personalizado
- Basado en: GPT-4o Nano
- Proceso: Fine-tuning realizado mediante OpenAI API Fine-tuning
- El modelo fue entrenado con datos específicos del dominio para mejorar las respuestas en casos de uso particulares

### Gestión de Sesiones

- Django maneja automáticamente las sesiones mediante cookies
- El ID de conversación se almacena en `request.session['conversation_id']`
- Permite mantener conversaciones activas entre peticiones

### Modelo Fine-tuned

Este proyecto utiliza un modelo personalizado creado mediante el proceso de **Fine-tuning de OpenAI**.

**Características del modelo:**
- **Modelo base:** GPT-4o Nano (modelo base de OpenAI)
- **Proceso:** Fine-tuning mediante OpenAI API Fine-tuning
- **Propósito:** Adaptación del modelo para responder de manera más precisa y contextual según necesidades específicas del proyecto. En el caso de prueba la idea
era hacer un bot de atención al cliente sobre temas relacionados a celulares moviles.

**Ventajas del Fine-tuning:**
1. Respuestas más precisas y alineadas al caso de uso específico
2. Mejor comprensión del dominio y contexto del proyecto
3. Consistencia en el tono y estilo de las respuestas
4. Optimización de costos al usar un modelo Nano ajustado

**Cómo se realizó:**
- Preparación de dataset de entrenamiento con ejemplos específicos
- Upload del dataset mediante OpenAI API
- Creación del job de fine-tuning
- Validación y deployment del modelo resultante

Para más información sobre fine-tuning: [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)

## Consideraciones de Seguridad

⚠️ **Importante:** Antes de pasar a producción:

1. **API Key:** Mover la clave de OpenAI a variables de entorno
   ```python
   import os
   api_key = os.environ.get('OPENAI_API_KEY')
   ```

2. **Base de datos:** Cambiar SQLite por PostgreSQL o MySQL

3. **Secret Key:** Cambiar `SECRET_KEY` en settings.py

4. **Debug Mode:** Establecer `DEBUG = False` en producción

5. **HTTPS:** Usar certificados SSL en producción
