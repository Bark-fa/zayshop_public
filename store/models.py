from datetime import datetime
from django.db import models

GENDER_CHOICES = (
    ('men', 'men'),
    ('women', 'women'),
    ('unisex', 'unisex')
)


class Product(models.Model):
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=450)
    colors = models.CharField(max_length=450)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    genders = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_webp = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    S = models.BooleanField(default=True)
    M = models.BooleanField(default=True)
    L = models.BooleanField(default=True)
    XL = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name
