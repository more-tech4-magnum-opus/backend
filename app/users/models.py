from django.contrib.auth.models import AbstractUser
from django.db import models
from faker import Faker


class Clan(models.Model):
    name = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        name = Faker().name()
        self.name = name  + "'s clan"
        super(Clan, self).save(*args, **kwargs)


class User(AbstractUser):
    class WorkerType(models.TextChoices):
        WORKER = "WORKER", "worker"
        HR = "HR", "human resources"
        ADMIN = "ADMIN", "administrator"

    first_name = None
    last_name = None

    # image = models.ImageField(upload_to=user_file_upload_mixin, blank=True)
    # image_cropped = models.ImageField(upload_to="cropped/", blank=True)

    about = models.TextField(blank=True)
    type = models.CharField(
        max_length=6, choices=WorkerType.choices, default=WorkerType.WORKER
    )
    salary = models.IntegerField(default=0)
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super(AbstractUser, self).save(*args, **kwargs)

    @property
    def is_manager(self):
        return self.type in [self.WorkerType.HR, self.WorkerType.ADMIN]

    @property
    def is_admin(self):
        return self.type == self.WorkerType.ADMIN

    class Meta:
        ordering = ["-id"]