from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
def validateCin(value):
    if len(value) !=8:
        raise ValidationError("Cin must has 8 characters")

class Person(AbstractUser):
    cin = models.CharField(primary_key=True , max_length=8  , validators=[validateCin], blank=False)
    email = models.EmailField("Email" , max_length=50 , blank=False)
    username = models.CharField(max_length=10, unique = True , blank=False)
    image = models.ImageField(null=True , upload_to="images/")
    location = models.CharField(max_length=50,default='Unknown')
    # face_image = models.ImageField(upload_to='face_images/', null=True, blank=True)
    keyword = models.CharField(max_length=8 , default=' ')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name= "Person"
