from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def enviar_correo(asunto, destinatarios, texto, html=None):
    email=EmailMultiAlternatives(
        subject=asunto,
        body=texto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=destinatarios
    )
    if html:
        email.attach_alternative(html,'text/html')
    email.send()
    return True

