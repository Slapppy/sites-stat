from django.contrib import admin

from .models import Counter, User

admin.site.register(Counter)
admin.site.register(User)
