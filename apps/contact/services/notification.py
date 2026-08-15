import logging

from django.conf import settings
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


def notify_contact_message(contact_message):
    recipient = settings.CONTACT_NOTIFICATION_EMAIL
    if not recipient:
        return False

    business_name = (
        contact_message.business.name
        if contact_message.business
        else "Sin línea seleccionada"
    )
    body = "\n".join(
        (
            f"Nombre: {contact_message.name}",
            f"Correo: {contact_message.email}",
            f"Teléfono: {contact_message.phone or 'No indicado'}",
            f"Línea: {business_name}",
            f"Asunto: {contact_message.subject}",
            "",
            contact_message.message,
        )
    )

    try:
        send_mail(
            subject=f"Nuevo mensaje en Pámi: {contact_message.subject}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
        )
    except Exception:
        logger.exception(
            "No se pudo enviar la notificación del mensaje de contacto %s.",
            contact_message.pk,
        )
        return False

    return True
