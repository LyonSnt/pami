from urllib.parse import urlencode

from django.urls import reverse


def build_contact_url(*, business, subject):
    query = urlencode({"business": business.pk, "subject": subject})
    return f"{reverse('contact:form')}?{query}"
