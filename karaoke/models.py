from django.db import models

# Create your models here.

class SongModel(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class PointModel(models.Model):
    point = models.IntegerField()
    duedate = models.DateField()
    title_id = models.ForeignKey(SongModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.point