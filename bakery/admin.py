from django.contrib import admin

from bakery.models import Order, Product

admin.site.register(Product)
admin.site.register(Order)
