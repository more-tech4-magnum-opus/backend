from django.core.files import File
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from utils.file import crop_image
from utils.generators import generate_charset
from .models import Product


@receiver(pre_save, sender=Product)
def create_product(sender, instance, **kwargs):
    slug = generate_charset(5)
    while Product.objects.filter(slug=slug).exists():
        slug = generate_charset(5)
    instance.slug = slug


@receiver(post_save, sender=Product)
def process_product(sender, instance, created, **kwargs):
    if instance.image and kwargs["update_fields"] != frozenset({"image_cropped"}):
        instance.image_cropped = File(
            crop_image(instance.image.path, cut_to=(250, 250)),
            name=instance.image.path.split(".")[0].split("/")[-1] + ".png",
        )
        instance.save(update_fields=["image_cropped"])
