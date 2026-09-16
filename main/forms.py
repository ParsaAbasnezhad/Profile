from django import forms

from .security import sanitize_text
from .views_constants import EMAIL_RE, PHONE_RE, normalize_phone


class ContactMessageForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=100)
    contact = forms.CharField(min_length=3, max_length=150)
    message = forms.CharField(min_length=1, max_length=2000)
    company_website = forms.CharField(required=False, max_length=200)

    def clean_name(self):
        name = sanitize_text(self.cleaned_data["name"])
        if not name:
            raise forms.ValidationError("Please enter your name.")
        return name

    def clean_contact(self):
        contact = sanitize_text(self.cleaned_data["contact"])
        phone = normalize_phone(contact)
        if EMAIL_RE.match(contact) or PHONE_RE.match(phone):
            return contact
        raise forms.ValidationError("Please enter a valid email address or phone number.")

    def clean_message(self):
        message = sanitize_text(self.cleaned_data["message"], keep_newlines=True)
        if not message:
            raise forms.ValidationError("Please enter a short message.")
        return message

    def is_honeypot_triggered(self) -> bool:
        return bool(sanitize_text(self.cleaned_data.get("company_website") or ""))


class VisitRequestForm(forms.Form):
    phone = forms.CharField(min_length=7, max_length=20)
    company_website = forms.CharField(required=False, max_length=200)

    def clean_phone(self):
        phone = normalize_phone(sanitize_text(self.cleaned_data["phone"]))
        if not PHONE_RE.match(phone):
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone

    def is_honeypot_triggered(self) -> bool:
        return bool(sanitize_text(self.cleaned_data.get("company_website") or ""))
