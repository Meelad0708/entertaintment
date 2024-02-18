from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    release = models.DateField('Release Date')
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.title

    def release_date(self):
        return self.release

    def __int__(self):
        return self.rating


