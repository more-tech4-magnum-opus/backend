from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to="uploads/")
    image_cropped = models.ImageField(upload_to="cropped/", blank=True)
    nft = models.CharField(max_length=500, blank=True)

    price = models.IntegerField(validators=[MinValueValidator(0)])
    creator = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
