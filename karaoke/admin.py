from django.contrib import admin
from .models import SongModel, PointModel

# Register your models here.

admin.site.register(SongModel)
admin.site.register(PointModel)