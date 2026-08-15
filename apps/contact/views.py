from django.contrib import messages
from django.shortcuts import redirect, render

from apps.audit.models import AuditLog
from apps.audit.services import create_audit_log
from apps.contact.forms import ContactMessageForm
from apps.contact.services.message import create_contact_message
from apps.contact.services.notification import notify_contact_message
from apps.contact.services.submission import (
    is_duplicate_submission,
    remember_submission,
)


def contact_form(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            submission_data = {
                key: value
                for key, value in form.cleaned_data.items()
                if key != "honeypot"
            }

            if form.cleaned_data["honeypot"] or is_duplicate_submission(
                request,
                submission_data,
            ):
                messages.success(request, "Tu mensaje fue enviado correctamente.")
                return redirect("contact:success")

            contact_message = create_contact_message(**submission_data)
            create_audit_log(
                request=request,
                action=AuditLog.Action.CREATE,
                instance=contact_message,
            )
            remember_submission(request, submission_data)
            notify_contact_message(contact_message)
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
