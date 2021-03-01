from django.db import models
from authentication.models import User
from store.models import Product


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=2)
