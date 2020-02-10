from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


LOCATION_CHOICES = [
    ('киев', 'Киев'),
    ('харьков', 'Харьков'),
    ('одесса', 'Одесса'),
    ('днепр', 'Днепр'),
    ('львов', 'Львов'),
    ('донецк', 'Донецк'),
    ('запорожье', 'Запорожье'),
    ('полтава', 'Полтава'),
    ('винница', 'Винница'),
]


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=40, blank=False,
                              error_messages={'unique': 'Пользователь с данной почной уже существует!'})
    role = models.CharField(max_length=12, error_messages={'required': 'Роль должна быть выдана'})
    about = models.CharField(max_length=1000, blank=True, null=True)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    company_name = models.CharField(max_length=50, blank=True)
    company_address = models.CharField(max_length=15, blank=True, choices=LOCATION_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.role == 'employee':
            full_name = '%s %s' % (self.first_name, self.last_name)
        elif self.role == 'employer':
            full_name = '%s' % self.company_name
        else:
            full_name = '%s' % self.email

        return full_name.strip()




