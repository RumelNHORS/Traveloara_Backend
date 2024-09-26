from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save


# Choices for gender and identity types
GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)

# User Indentification Choice 
IDENTITY_TYPE = (
    ("National Identification Number", "National Identification Number"),
    ("Driver's License", "Driver's License"),
    ("International Passport", "International Passport"),
)


# Custom User model inheriting from AbstractUser
class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default="Other")

    # User type fields
    is_guest = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Set email as the default username
        if not self.username:
            self.username = self.email
        # Ensure only one type of user is set
        if self.is_guest:
            self.is_host = False
            self.is_admin = False
            self.is_superuser = False
        elif self.is_host:
            self.is_guest = False
            self.is_admin = False
            self.is_superuser = False
        elif self.is_admin:
            self.is_guest = False
            self.is_host = False
            self.is_superuser = False
        elif self.is_superuser:
            self.is_guest = False
            self.is_host = False
            self.is_admin = False
        
        super().save(*args, **kwargs)
    

