from django import forms
from users import forms as users_forms

class MyForm(RegistrationFormHoneypot):

    """Docstring for MyForm. """

    name = forms.CharField()
