from django.shortcuts import render
from django.views import View
from openai import OpenAI
from .models import Conversation, Message
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

class HolaMundoView(View):
    def get(self, request):
        # Obtener o crear una conversación activa
        conversation = self._get_or_create_conversation(request)

        # Obtener todos los mensajes de la conversación
        messages = conversation.messages.all()

        return render(request, "chat/index.html", {
            "messages": messages,
            "conversation_id": conversation.id
        })

    def post(self, request):
        input_text = request.POST.get("inputfirst")

        if not input_text or not input_text.strip():
            # Si no hay texto, redirigir al GET
            return self.get(request)

        # Obtener o crear conversación
        conversation = self._get_or_create_conversation(request)

        # Guardar mensaje del usuario
        user_message = Message.objects.create(
            conversation=conversation,
            content=input_text.strip(),
            is_user=True
        )

        # Recuperar todos los mensajes anteriores para enviar como contexto
        previous_messages = conversation.messages.all()

        # Formatear mensajes en el formato que espera OpenAI
        messages_for_api = []
        for msg in previous_messages:
            role = "user" if msg.is_user else "assistant"
            messages_for_api.append({
                "role": role,
                "content": msg.content
            })

        # Obtener respuesta del modelo con todo el contexto
        response = client.chat.completions.create(
            model="ft:gpt-4.1-nano-2025-04-14:facufunctions:pruebatienda:CshSJDGz",
            messages=messages_for_api
        )

        # Guardar respuesta del asistente
        assistant_message = Message.objects.create(
            conversation=conversation,
            content=response.choices[0].message.content,
            is_user=False,
            metadata={
                "model": "ft:gpt-4.1-nano-2025-04-14:facufunctions:pruebatienda:CshSJDGz"
            }
        )

        # Obtener todos los mensajes para mostrar
        messages = conversation.messages.all()

        return render(request, "chat/index.html", {
            "messages": messages,
            "conversation_id": conversation.id
        })

    def delete(self, request):
        """Limpiar la conversación actual y crear una nueva"""
        # Limpiar el conversation_id de la sesión
        if 'conversation_id' in request.session:
            del request.session['conversation_id']

        from django.http import JsonResponse
        return JsonResponse({'status': 'ok'})

    def _get_or_create_conversation(self, request):
        """Obtener conversación actual o crear una nueva"""
        # Por ahora usamos la sesión para mantener la conversación activa
        conversation_id = request.session.get('conversation_id')

        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                conversation = Conversation.objects.create()
                request.session['conversation_id'] = conversation.id
        else:
            conversation = Conversation.objects.create()
            request.session['conversation_id'] = conversation.id

        return conversation