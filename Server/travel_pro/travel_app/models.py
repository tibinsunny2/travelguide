from django.db import models
from django.contrib.auth.models import User



# Create your models here.


  

from django.db import models

class TravelPackage(models.Model):
    DURATION_CHOICES = [
        (1, '1 day'),
        (2, '2 days'),
        (3, '3 days'),
        # Add more duration choices as needed
    ]

    HOTEL_CHOICES = [
        ('5star', '5 Star'),
        ('4star', '4 Star'),
        ('3star', '3 Star'),
        # Add more hotel choices as needed
    ]
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(choices=DURATION_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    photos = models.ImageField(upload_to='image/', null=True, blank=True)
    select_hotel = models.CharField(max_length=255, choices=HOTEL_CHOICES)
    packages_inclusion = models.TextField()
    note = models.TextField()

    def __str__(self):
        return self.title

class userreg(models.Model):
    username=models.CharField(max_length=50)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=50)
    address=models.TextField()
    zipcode=models.IntegerField()
    passport=models.FileField(upload_to='image/',null=True, blank=True)
    id_proof=models.FileField(upload_to='image/',null=True, blank=True)
    phone_no=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=50)

class travelblog(models.Model):
    username=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    image1=models.FileField(upload_to='image/',null=True, blank=True)
    image2=models.FileField(upload_to='image/',null=True, blank=True)
    image3=models.FileField(upload_to='image/',null=True, blank=True)
    message=models.TextField()
    date=models.DateTimeField(auto_now_add=True)