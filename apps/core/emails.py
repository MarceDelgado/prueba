# apps/core/emails.py
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

def enviar_correo_html(subject, template_name, context, to_emails, from_email=None, attachments=None):
    """
    Envía un correo HTML renderizando una plantilla.
    - subject: str
    - template_name: 'emails/mi_template.html'
    - context: dict para render_to_string
    - to_emails: list[str] o str
    - from_email: opcional, usa DEFAULT_FROM_EMAIL si es None
    - attachments: iterable de (filename, content, mimetype) o paths
    """
    if isinstance(to_emails, str):
        to_emails = [to_emails]

    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,  # si es None, Django usa DEFAULT_FROM_EMAIL
        to=to_emails
    )
    msg.attach_alternative(html_content, "text/html")

    if attachments:
        for a in attachments:
            if isinstance(a, tuple) and len(a) in (2, 3):
                # (filename, content[, mimetype])
                msg.attach(*a)
            else:
                # si te pasan un path
                msg.attach_file(a)
    msg.send()
