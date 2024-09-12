from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    time_to_cook = models.IntegerField()

    def __str__(self):
        return self.name
    

class Order(models.Model):
    person_name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through='OrderItem')
    date = models.DateField(auto_now_add=True)
    created_at = models.TimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
