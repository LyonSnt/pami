from django.utils import timezone

from apps.contact.models import ContactMessage


def create_contact_message(**data):
    return ContactMessage.objects.create(**data)


def mark_contact_message_in_review(message):
    message.status = ContactMessage.Status.IN_REVIEW
    message.save(update_fields=["status", "updated_at"])
    return message


def mark_contact_message_responded(message):
    message.status = ContactMessage.Status.RESPONDED
    message.responded_at = timezone.now()
    message.save(update_fields=["status", "responded_at", "updated_at"])
    return message


def close_contact_message(message):
    message.status = ContactMessage.Status.CLOSED
    message.save(update_fields=["status", "updated_at"])
    return message