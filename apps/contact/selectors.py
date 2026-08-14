from apps.contact.models import ContactMessage


def get_contact_messages():
    return ContactMessage.objects.select_related("business").all()


def get_new_contact_messages():
    return (
        ContactMessage.objects
        .select_related("business")
        .filter(status=ContactMessage.Status.NEW)
    )


def get_contact_messages_by_business(business):
    return (
        ContactMessage.objects
        .select_related("business")
        .filter(business=business)
    )