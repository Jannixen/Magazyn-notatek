from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.db import models
from django.utils import timezone


class Note(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    date = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=10000, default='Tu wpisz treść swojej notatki')
    if_public = models.BooleanField(default=False)
    users_with_permission_to_view = models.ManyToManyField(User, related_name='permissions')

    def get_short(self):
        return self.text[0:20] + "..."

    def save(self):
        super().save()
        self.users_with_permission_to_view.add(self.author)
        super().save()

    def can_view(self, user):
        if self.users_with_permission_to_view.contains(user) or self.if_public:
            return True
        return False

    def share_note(self, user):
        self.users_with_permission_to_view.add(user)
        super().save()



class EncryptedNote(Note):
    salt = models.BinaryField()
    password = models.BinaryField()
    aes_key = models.BinaryField()
