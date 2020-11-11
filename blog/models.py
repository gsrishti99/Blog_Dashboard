from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=13)
    slug = models.CharField(max_length=130)
    views = models.IntegerField(default=0)
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + ' by ' + self.author
