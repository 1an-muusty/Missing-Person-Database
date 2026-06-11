from django.contrib import admin
from .models import Missingperson, CustomUser

admin.site.register(Missingperson)
admin.site.register(CustomUser)