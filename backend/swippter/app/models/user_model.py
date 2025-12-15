from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from rest_framework import status as S
from app.core.exceptions import UnprocessableError, CUSTOM_CODE
from app.models.base_model import BaseModel
from app.utils.utilities import F, generate_salt
from app.models.signals.user_signal import trigger_user_verification_email


class Role(models.IntegerChoices):
    SUPER_ADMIN = 1, "super_admin"
    ADMIN = 2, "admin"
    CONSUMER = 3, "consumer"
    SELLER = 4, "seller"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise UnprocessableError(
                code=S.HTTP_422_UNPROCESSABLE_ENTITY,
                msg=F.UNPROCESSABLE,
                errors=[
                    {
                        F.FIELD: F.EMAIL,
                        F.ERRORS: [
                            {
                                F.CODE: CUSTOM_CODE.EMAIL_MUST_BE_SET,
                                F.MSG: F.EMAIL_MUST_BE_SET,
                            }
                        ],
                    }
                ],
            )
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault(F.IS_SUPERUSER, False)
        extra_fields.setdefault(F.IS_STAFF, False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault(F.IS_SUPERUSER, True)
        extra_fields.setdefault(F.IS_STAFF, True)
        extra_fields.setdefault(F.IS_VERIFIED, True)
        extra_fields.setdefault(F.ROLE, Role.SUPER_ADMIN)
        extra_fields.setdefault(F.FIRST_NAME, F.ADMIN)
        extra_fields.setdefault(F.LAST_NAME, F.ADMIN)
        extra_fields.setdefault(F.SALT, generate_salt())
        return self._create_user(email, password, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    role = models.IntegerField(
        blank=False, null=False, default=Role.CONSUMER, choices=Role.choices
    )
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    salt = models.CharField(max_length=32, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    address = models.CharField(max_length=1000,default="")

    objects = UserManager()

    USERNAME_FIELD = F.EMAIL
    REQUIRED_FIELDS = []
    ordering = (F.EMAIL,)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


post_save.connect(trigger_user_verification_email, sender=User)
