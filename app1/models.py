#_*_ coding: utf-8 _*_
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

#没有改变或继承原有的USER，试试可不可以自定义
# Create your models here.
@python_2_unicode_compatible
class Goods(models.Model):
    good_id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=30)
    comment=models.TextField()
    place=models.CharField(max_length=20)
    producer=models.CharField(max_length=40)
    supplier_id=models.IntegerField()
    price=models.IntegerField()
    count=models.IntegerField()
    remain=models.IntegerField()
    type=models.CharField(max_length=10)
    image_path=models.CharField(blank=True, max_length=100)
    website=models.CharField(blank=True, max_length=100)

    class Meta:
        db_table = "Goods"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class Managers(models.Model):
    manager_id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=10)
    address=models.CharField(max_length=50)
    telephone=models.CharField(max_length=15)
    email=models.EmailField()
    reg_time=models.DateField()
    password=models.CharField(max_length=20)

    class Meta:
        db_table="Managers"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class Customers(models.Model):
#    customer_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    address=models.CharField(max_length=50)
    telephone=models.CharField(max_length=15)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    temp_order=models.IntegerField(blank=True,null=True)
    @property
    def customer_id(self):
        return self.id

    class Meta:
        db_table="Customers"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class Orders(models.Model):
    order_id=models.IntegerField(primary_key=True)
    is_temp=models.IntegerField()
    good_str=models.CharField(max_length=50)
    good_num=models.CharField(max_length=50)
    customer_id=models.IntegerField()
    manager_id=models.IntegerField()
    status=models.CharField(max_length=50) #paid/sent/got
    submit_date=models.DateField()
    finish_date=models.DateField()

    class Meta:
        db_table="Orders"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class Suppliers(models.Model):
    supplier_id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)

    class Meta:
        db_table="Suppliers"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class Contacts(models.Model):
    contact_id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=10)
    address=models.CharField(max_length=50)
    telephone=models.CharField(max_length=15)
    email=models.EmailField()
    reg_time=models.DateField()
    supplier_id=models.IntegerField()

    class Meta:
        db_table="Contacts"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class Supply_orders(models.Model):
    supply_order_id=models.IntegerField(primary_key=True)
    supplier_id=models.IntegerField()
    good_str=models.CharField(max_length=50)
    goods_num=models.CharField(max_length=50)
    status=models.CharField(max_length=4)
    submit_date=models.DateField()
    finish_date=models.DateField()
    contact_id = models.IntegerField()
    manager_id = models.IntegerField()

    class Meta:
        db_table="Supply_orders"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class Complaints(models.Model):
    complaint_id=models.IntegerField(primary_key=True)
    customer_id=models.IntegerField()
    text=models.TextField()
    submit_date=models.DateField()
    proceed_date=models.DateField()
    status=models.CharField(max_length=4) #wait/done
    manager_id=models.IntegerField()
    reply=models.TextField()
   # score=models.IntegerField()
    follow_cmplt_id=models.IntegerField()
    source_cmplt_id=models.IntegerField()

    class Meta:
        db_table="Complaints"

    def _str_(self):
        return self.name
























