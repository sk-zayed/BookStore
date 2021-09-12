from django.contrib import admin

# Register your models here.
from .models import Customer, Book, Contact, Order, OrderUpdate, SoldBook

admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(SoldBook)