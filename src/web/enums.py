from django.db import models

#TODO: может оптимизировать раз оно и не используется вовсе
class Role(models.TextChoices):
    admin = "admin", "Администратор"
    staff = "staff", "Сотрудник"
    user = "user", "Пользователь"
