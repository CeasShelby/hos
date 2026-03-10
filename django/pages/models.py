from django.db import models

# Create your models here.
class Destination(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    disc = models.TextField()
    price = models.FloatField()
    img = models.ImageField(upload_to='images/')
    offer= models.BooleanField(default=False)

class Register(models.Model):
   password = models.CharField(max_length=128)