# app/utils.py
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def enviar_correo(asunto, destinatarios, texto, html=None):
    """
    Envía correos con soporte para versión HTML

    Args:
        asunto: Título del correo
        destinatarios: Lista de direcciones email
        texto: Contenido en texto plano
        html: Contenido HTML opcional
    """
    email = EmailMultiAlternatives(
        subject=asunto,
        body=texto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=destinatarios
    )
    if html:
        email.attach_alternative(html, 'text/html')
    email.send()
    return True
