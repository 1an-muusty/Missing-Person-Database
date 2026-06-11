from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator

# Create your models here.
class Missingperson(models.Model):

    GENDER_CHOICES = [
        ('F','Female'),
        ('M','Male'),
        ('O','Other')
    ]

    STATUS_CHOICES = [
        ('missing','Missing'),
        ('found','Found'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Female' )
    lastSeenDate = models.DateField()
    lastSeenLocation = models.CharField(max_length=120)
    description = models.TextField()
    uploadPhoto= models.ImageField(upload_to='uploads/missingpeople/') 
    contactInformation = models.CharField(
        max_length=12, validators=[
            RegexValidator(
                regex=r'^\d{10,12}$',
                message="Phone number must be 10-12 digits.",
                code='invalid_phone_number'
            )
        ],
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='missing')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"
    class Meta:
        db_table = 'missingperson'
        verbose_name = "Missing Person"
        verbose_name_plural = "Missing Persons"

class CustomUser(AbstractUser):
    fname = models.CharField(max_length=50, verbose_name="First Name")
    lname = models.CharField(max_length=50, verbose_name="Last Name")

    class Meta:
        db_table = 'customUser'
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

