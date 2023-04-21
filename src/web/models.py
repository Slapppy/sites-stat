from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager


from .enums import Role


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, commit=True, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, role=Role.admin, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=128, null=True)
    surname = models.CharField(max_length=128, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(choices=Role.choices, max_length=15, default=Role.user)#TODO: как будто оо нигде и не используется, может но и не надо тогда

    @property
    def is_superuser(self):
        return self.role == Role.admin

    @property
    def is_staff(self):
        return self.role in (Role.admin, Role.staff)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "web_user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Counter(BaseModel):
    name = models.CharField(max_length=128, unique=True)
    link = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="counters")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Счетчик"
        verbose_name_plural = "Счетчики"
