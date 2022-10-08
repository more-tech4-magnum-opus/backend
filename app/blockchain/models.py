from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from users.models import User


class Transaction(models.Model):
    user_from = models.ForeignKey(
        User, related_name="transactions_from", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        User, related_name="transactions_to", on_delete=models.CASCADE
    )

    amount = models.IntegerField(validators=[MinValueValidator(1)])

    created = models.DateTimeField(auto_now_add=True)

    hash = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"transaction from {self.user_from} to {self.user_to}"


class AdminTransaction(models.Model):
    class TransactionType(models.TextChoices):
        FROM = "PAYMENT", "payment"
        TO = "SALARY", "salary"

    type = models.CharField(max_length=7, choices=TransactionType.choices)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    user = models.ForeignKey(
        User, related_name="admin_transactions", on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)

    hash = models.CharField(max_length=256, unique=True)

    @property
    def user_from(self):
        return "system" if self.type == self.TransactionType.TO else self.user.username

    @property
    def user_to(self):
        return (
            "system" if self.type == self.TransactionType.FROM else self.user.username
        )

    def __str__(self):
        return str(self.amount)
