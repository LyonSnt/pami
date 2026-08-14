from django import forms

from apps.businesses.selectors import get_published_businesses
from apps.contact.models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["business"].queryset = get_published_businesses()

        control_classes = (
            "w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 "
            "text-base text-slate-900 focus-visible:outline-none "
            "focus-visible:ring-2 focus-visible:ring-primary"
        )

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = control_classes

            described_by = []
            if field.help_text:
                described_by.append(f"id_{field_name}_help")
            if self[field_name].errors:
                field.widget.attrs["aria-invalid"] = "true"
                described_by.append(f"id_{field_name}_errors")
            if described_by:
                field.widget.attrs["aria-describedby"] = " ".join(described_by)

        self.fields["message"].widget.attrs["rows"] = 5

    class Meta:
        model = ContactMessage
        fields = (
            "business",
            "name",
            "email",
            "phone",
            "subject",
            "message",
        )
