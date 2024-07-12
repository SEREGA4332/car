from django.contrib import admin
from .models import Client, Car, Sale

admin.site.register(Client)
admin.site.register(Car)
admin.site.register(Sale)