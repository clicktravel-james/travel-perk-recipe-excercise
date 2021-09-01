from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

"""The manager class is the go between the database and the models. Every
model needs at least one manager class. Django adds one per model by default
but if you need special behaviour you can override it like in this file"""


class UserManager(BaseUserManager):

    """These methods are accessed through the .objects property on the model"""

    def create_user(self, email, password=None, **extra_fields):
        """Validates, creates and saves a new user """
        if not email:
            raise ValueError('User must have an email address')

        """self.model is short hand for creating a new user model,
        as it accesses the model propertery teh class is for"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Create a super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    """Needed to make sure our custom manager is used for this custom model"""
    objects = UserManager()

    """USERNAME_FIELD is manditory so swaps the value out for email"""
    USERNAME_FIELD = 'email'
