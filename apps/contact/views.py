from django.contrib import messages
from django.shortcuts import redirect, render

from apps.audit.models import AuditLog
from apps.audit.services import create_audit_log
from apps.contact.forms import ContactMessageForm
from apps.contact.services.message import create_contact_message


def contact_form(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            contact_message = create_contact_message(**form.cleaned_data)
            create_audit_log(
                request=request,
                action=AuditLog.Action.CREATE,
                instance=contact_message,
            )
            messages.success(request, "Tu mensaje fue enviado correctamente.")
            return redirect("contact:success")
    else:
        form = ContactMessageForm()

    context = {
        "form": form,
    }

    return render(request, "contact/form.html", context)


def contact_success(request):
    return render(request, "contact/success.html")
