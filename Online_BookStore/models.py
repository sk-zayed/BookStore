from django.db import models
from django.db.models.deletion import CASCADE
import datetime

# Create your models here.

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.IntegerField(default=0)

    def __str__(self):
        return str(self.customer_id)+" - "+self.firstname+" "+self.lastname

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, default="")
    price = models.IntegerField(default=0)
    book_desc = models.CharField(max_length=500)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="images", default="")

    def __str__(self):
        return str(self.book_id)+" - "+self.book_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.msg_id)+" - "+self.firstname+" "+self.lastname

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=CASCADE)
    ordered_book = models.CharField(max_length=50)
    book_category = models.CharField(max_length=50)
    book_cost = models.IntegerField(default=0)

    def __str__(self):
        return str(self.order_id)+" - "+self.ordered_book

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=CASCADE)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(datetime.datetime.now())

    def __str__(self):
        return str(self.order_id)+" - "+self.update_desc

class SoldBook(models.Model):
    sold_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=CASCADE)
    book_name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, default="")
    price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.sold_id)+" - "+self.book_name