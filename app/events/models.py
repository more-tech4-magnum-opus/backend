from django.db import models

from users.models import User


class Event(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=8)
    about = models.TextField(blank=True)

    creator = models.ForeignKey(
        User, related_name="events_created", on_delete=models.CASCADE
    )
    starts = models.DateTimeField(blank=False)

    image = models.ImageField(upload_to="uploads/", blank=True)
    image_cropped = models.ImageField(upload_to="cropped/", blank=True)

    planning = models.IntegerField(default=0)
    attended = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-starts"]


class EventAttendance(models.Model):
    event = models.ForeignKey(Event, related_name="people", on_delete=models.CASCADE)
    worker = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)
    token = models.CharField(blank=False, unique=True, max_length=128)
    attended = models.BooleanField(default=False)

    @property
    def event_slug(self):
        return self.event.slug

    @property
    def worker_username(self):
        return self.worker.username

    def username(self):
        return self.worker_username

    def __str__(self):
        return f"{self.worker.name} attendance on {self.event.name}"

    class Meta:
        ordering = ["event__starts"]
        unique_together = ["event", "worker"]
