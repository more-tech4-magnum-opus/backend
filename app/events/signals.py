from django.core.files import File
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver

from utils.file import crop_image
from utils.generators import generate_charset
from .models import EventAttendance, Event


@receiver(post_save, sender=EventAttendance)
def create_attendance(sender, instance, created, **kwargs):
    if created:
        token = generate_charset(25)
        while EventAttendance.objects.filter(token=token).exists():
            token = generate_charset(25)
        instance.token = token

        instance.event.planning += 1
        instance.event.save(update_fields=["planning", "token"])


@receiver(post_save, sender=Event)
def process_event(sender, instance, created, **kwargs):
    if created:
        slug = generate_charset(5)
        while Event.objects.filter(slug=slug).exists():
            slug = generate_charset(5)
        instance.slug = slug
        instance.save(update_fields=["slug"])

    if instance.image and kwargs["update_fields"] is None:
        instance.image_cropped = File(
            crop_image(instance.image.path, cut_to=(250, 250)),
            name=instance.image.path.split(".")[0].split("/")[-1] + ".png",
        )
        instance.save(update_fields=["image_cropped"])


@receiver(post_delete, sender=EventAttendance)
def delete_attendance(sender, instance, **kwargs):
    instance.event.planning -= 1
    instance.event.save(update_fields=["planning"])
