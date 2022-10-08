from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


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
    name = models.CharField(max_length=120)
    type = models.CharField(
        max_length=6, choices=WorkerType.choices, default=WorkerType.WORKER
    )
    salary = models.IntegerField(default=0)
    clan = models.ForeignKey(Clan, on_delete=models.SET_NULL, null=True)
    command = models.ForeignKey(
        "users.Command", related_name="workers", on_delete=models.CASCADE
    )
    salary = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    respect = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    wallet_private_key = models.CharField(max_length=96, unique=True)
    wallet_public_key = models.CharField(max_length=96, unique=True)
    telegram = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username

    @property
    def is_manager(self):
        return self.type in [self.WorkerType.HR, self.WorkerType.ADMIN]

    @property
    def is_admin(self):
        return self.type == self.WorkerType.ADMIN

    @property
    def department(self):
        return self.command.stream.department.name

    class Meta:
        ordering = ["-id"]


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Stream(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department, related_name="streams", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Command(models.Model):
    name = models.CharField(max_length=100)
    stream = models.ForeignKey(
        Stream, related_name="commands", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
