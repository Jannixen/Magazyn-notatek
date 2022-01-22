from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, Textarea, BooleanField, CharField, PasswordInput


class NoteForm(Form):
    text = CharField(required=True, label="Treść notatki", widget=Textarea(attrs={
        'cols': 60,
        'rows': 15}))
    if_encrypted = BooleanField(required=False, label="Czy notatka ma być szyfrowana?")
    if_public = BooleanField(required=False, label="Czy notatka ma być publiczna?")
    password = CharField(widget=PasswordInput(), required=False)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class ShareNoteForm(Form):
    user_to_share = CharField(required=False, label="Udostępnij notatkę znajomym (wpisz nazwę użytkownika")


class NotePasswordForm(Form):
    password = CharField(widget=PasswordInput(), required=False)
