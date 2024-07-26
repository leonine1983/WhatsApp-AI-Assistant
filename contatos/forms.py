from django import forms
from .models import Message, Contacts

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'image', 'video']

class ContactsForm(forms.Form):
    contacts = forms.ModelMultipleChoiceField(queryset=Contacts.objects.all(), widget=forms.CheckboxSelectMultiple)
    neighborhoods = forms.CharField(required=False)
    city = forms.CharField(required=False)
