from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(
        label="Buscar",
        max_length=100,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "type": "search",
                "class": (
                    "w-full rounded-lg border border-slate-300 bg-white px-5 py-4 "
                    "text-lg text-slate-900 placeholder:text-slate-500 "
                    "focus-visible:outline-none focus-visible:ring-2 "
                    "focus-visible:ring-primary"
                ),
                "placeholder": "Busca chaquetas, buzos, proyectos o artículos",
                "autocomplete": "off",
            }
        ),
    )
