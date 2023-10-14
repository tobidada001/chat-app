from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length= 300)


class RoomMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(  auto_now_add=True)

    class Meta:
        ordering = ('date', )