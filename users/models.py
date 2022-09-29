from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    verified = models.BooleanField(default=False)
    verified_date = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(null=True, max_length=255)
    first_name = None
    last_name = None

    def get_short_name(self):
        return self.name
        

    def __str__(self):
        return self.email


    def get_admin_url(self):
        return reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=(self.id,),
        )
