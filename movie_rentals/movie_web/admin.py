from django.contrib import admin

# Register your models here.
from .models import Movie, Profile

admin.site.register(Profile)
admin.site.register(Movie)
