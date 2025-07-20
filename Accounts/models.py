import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

def generate_unique_code():
    model = User
    while True:
        code = str(uuid.uuid4()).replace("-", "").upper()[:6]
        try:
            if not model.objects.filter(pk=code).exists():
                break
        except Exception as e:
            return code
    return code

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, mobile_number=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password='admin', mobile_number=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, password, mobile_number, **extra_fields)

class BaseUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=255, primary_key=True, default=generate_unique_code)
    full_name = models.CharField(_("full name"), max_length=255, blank=True)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.strip().split(" ")[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        with mail.get_connection() as connection:
            mail.EmailMessage(subject, message, from_email, [self.email], connection=connection, **kwargs).send()

class User(BaseUser):
    """
    Final User model
    """
    mobile_number = models.CharField(max_length=20, blank=True, null=True)


class Venue(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Day(models.Model):
    day = models.IntegerField(_(""))

class Speaker(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    time = models.TimeField(default=timezone.now)
    date = models.DateField(default=timezone.datetime(2025, 7, 25).date())
    pin = models.BooleanField(default=False)
    description = models.TextField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    redirect = models.CharField( max_length=100, default="")
    def __str__(self):
        return self.name

class ProjectExhibitionRegistration(models.Model):
    leader_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    team_name = models.CharField(max_length=100)
    number_of_members = models.IntegerField()
    district = models.CharField(max_length=100,)
    university = models.CharField(max_length=100,)
    abstract_link = models.URLField(max_length=300, default="")
    abstract_pdf = models.FileField(
			upload_to='abstracts/',
			validators=[
				FileExtensionValidator(allowed_extensions=['pdf'])
			]
		   )


    def __str__(self):
        return f"{self.team_name} - {self.leader_name}"

class IdeathonRegistration(models.Model):
    team_name = models.CharField(max_length=100)
    team_lead_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    institution = models.CharField(max_length=50)
    number_of_members = models.IntegerField()

    def __str__(self):
        return f"{self.team_name} - {self.team_lead_name}"


class HackathonRegistration(models.Model):
    team_lead_name = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    number_of_members = models.IntegerField()
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    github_profile = models.URLField()
    linkedin_profile = models.URLField() 
    portfolio = models.URLField(blank=True, null=True) 
    resume_link = models.URLField()

    def __str__(self):
        return f"{self.team_lead_name} - {self.institution}"

class MediaRegistration(models.Model):
    name = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    intrested_area = models.CharField(max_length=50)
    portfolio = models.URLField(max_length=250)

    def __str__(self):
        return f"{self.name} - {self.intrested_area}"

class ReadmissionRegistration(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=3)
    contact_no = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    muncipality = models.CharField(max_length=100)
    vard = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.age}"