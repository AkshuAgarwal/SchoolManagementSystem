from django.db import models
from django.core.validators import RegexValidator


class User(models.Model):
    user_id = models.PositiveBigIntegerField(unique=True, primary_key=True)
    user_name = models.CharField(max_length=32)
    user_type = models.CharField(max_length=32)
    creation_time = models.DateTimeField()
    contact_no = models.CharField(
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message='Contact No. must be entered in the format: "+999999999999" (with country code). Up to 15 digits allowed.',
            )
        ],
        max_length=17,
    )
    mail_id = models.EmailField()
    address = models.TextField(max_length=1024)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)


class Authorization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    password = models.TextField()
    auth_token = models.TextField()
    ip_address = models.GenericIPAddressField()
