from django.contrib import admin

from .models import *  # TODO нельзя импортировать звездочку, синтаксически непонятно, что вы тут используете

admin.site.register(Counter)
admin.site.register(User)

# Register your models here. # TODO зарегистрировали :)
