from django.db import models


class Conversation(models.Model):
    """Modelo para agrupar mensajes en una conversación"""
    title = models.CharField(max_length=200, blank=True, default="Nueva conversación")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Conversación"
        verbose_name_plural = "Conversaciones"

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"


class Message(models.Model):
    """Modelo para almacenar cada mensaje del chat"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    content = models.TextField()
    is_user = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Campo opcional para metadata adicional (modelo usado, tokens, etc.)
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"

    def __str__(self):
        sender = "Usuario" if self.is_user else "Asistente"
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"{sender}: {preview}"
