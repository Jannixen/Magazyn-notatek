import hashlib
import os

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from storage.AESCipher import AESCipher
from storage.forms import NoteForm, CustomUserCreationForm, ShareNoteForm, NotePasswordForm
from storage.models import Note, EncryptedNote

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


SALT_SIZE = int(128 / 8)


def main_page(request):
    return render(request, "main.html")


@login_required
def storage_page(request):
    notes = Note.objects.filter(author=request.user)
    encrypted_notes = EncryptedNote.objects.filter(author=request.user)
    context = {"notes": notes, "encrypted_notes": encrypted_notes}
    return render(request, "user_page.html", context=context)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, "Rejestracja pomyślna.")
            return render(request, "user_page.html")
    else:
        form = CustomUserCreationForm()
    return render(
        request, "registration/register.html",
        {"form": form}
    )


@login_required
def add_note_page(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['if_encrypted'] and form.cleaned_data['if_public']:
                messages.info(request, "Notatka może być albo publiczna albo szyfrowana")
            elif form.cleaned_data['if_encrypted']:
                password = form.cleaned_data['password']
                try:
                    validate_password(password, request.user)
                    create_note_encrypted(request, form)
                except ValidationError as e:
                    form.add_error('password', e)
                    return render(request, "note_add_page.html", {'form': form})
            elif form.cleaned_data['if_public']:
                create_note_public(request, form)
            else:
                create_note_private(request, form)
    form = NoteForm()
    return render(request, "note_add_page.html", {"form": form})


@login_required
def note_page(request, note_id):
    if len(EncryptedNote.objects.filter(id=note_id)):
        note = EncryptedNote.objects.get(id=note_id)
    else:
        note = Note.objects.get(id=note_id)
    if note.can_view(request.user):
        if isinstance(note, EncryptedNote):
            if request.method == 'POST':
                form = NotePasswordForm(request.POST)
                if form.is_valid():
                    passwd = form.cleaned_data['password']
                    if check_password_equivalence(passwd, note.password, note.salt):
                        aes = AESCipher(note.aes_key)
                        decrypted_text = aes.decrypt(note.text)
                        messages.info(request, "Tekst notatki:" + decrypted_text)
            else:
                form = NotePasswordForm()
            context = {"note": note, "form": form}
        else:
            context = {"note": note}
    else:
        context = {}
        messages.info(request, "Nie masz uprawnień do wyświetlenia notatki")
    return render(request, "note_page.html", context)


@login_required
def share_note_page(request, note_id):
    note = Note.objects.get(id=note_id)
    if note.can_view(request.user):
        if request.method == 'POST':
            form = ShareNoteForm(request.POST)
            share_note(form, note, request)
        else:
            form = ShareNoteForm()
        context = {"form": form}
    else:
        context = {}
        messages.info(request, "Nie masz uprawnień do udostępniania notatki.")
    return render(request, "note_share_page.html", context)


def create_note_public(request, form):
    note = Note(
        text=form.cleaned_data['text']
    )
    if isinstance(request.user, User):
        note.author = request.user
    else:
        messages.info(request, "User not valid")
    note.save()


def create_note_private(request, form):
    note = Note(
        text=form.cleaned_data['text']
    )
    if isinstance(request.user, User):
        note.author = request.user
    else:
        messages.info(request, "User not valid")
    note.save()


def create_note_encrypted(request, form):
    key = generate_salt()
    aes_algorithm = AESCipher(key)
    note = EncryptedNote(
        text=aes_algorithm.encrypt(form.cleaned_data['text'])
    )
    note.aes_key = key
    note.salt = generate_salt()
    if len(form.cleaned_data['password']) == 0:
        messages.info(request, "Żeby zrobić zaszyfrowaną notatkę dodaj hasło")
    else:
        note.password = encrypt_password(form.cleaned_data['password'], note.salt)
        if isinstance(request.user, User):
            note.author = request.user
            note.save()
        else:
            messages.info(request, "Nieprawidłowy użytkownik")


def generate_salt():
    return os.urandom(SALT_SIZE)


def encrypt_password(password, salt):
    encrypted_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 320000)
    return encrypted_password


def check_password_equivalence(password, password_encrypted, salt):
    hash_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 320000)
    if hash_password == password_encrypted:
        return True
    else:
        return False


def share_note(form, note, request):
    if form.is_valid():
        user_to_share = User.objects.get(username=form.cleaned_data['user_to_share'])
        if user_to_share:
            note.share_note(user_to_share)
            messages.info(request, "Notatka udostępniona.")
