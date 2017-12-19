#_*_ coding: utf-8 _*_
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

#没有改变或继承原有的USER，试试可不可以自定义
# Create your models here.
@python_2_unicode_compatible
class goods(models.Model):
    good_id=models.IntegerField(primary_key=True,default=0)
    name=models.CharField(max_length=30)
    comment=models.TextField()
    place=models.CharField(max_length=20)
    producer=models.CharField(max_length=40)
    supplier_id=models.IntegerField()
    price=models.IntegerField()
    count=models.IntegerField()
    remain=models.IntegerField()
    type=models.CharField(max_length=10)
    image_path=models.URLField(null=True)
    website=models.URLField(null=True)

    class Meta:
        db_table="goods"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class managers(models.Model):
    manager_id=models.IntegerField(primary_key=True,default=0)
    name=models.CharField(max_length=10)
    address=models.CharField(max_length=50)
    telephone=models.CharField(max_length=15)
    email=models.EmailField()
    reg_time=models.DateField()
    password=models.CharField(max_length=20)

    class Meta:
        db_table="managers"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class customers(models.Model):
    customer_id=models.IntegerField(primary_key=True,db_column='Fld')
    name=models.CharField(max_length=10)
    address=models.CharField(max_length=50)
    telephone=models.CharField(max_length=15)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    temp_order=models.IntegerField(null=True)

    class Meta:
        db_table="customers"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class orders(models.Model):
    order_id=models.IntegerField(primary_key=True,default=0)
    is_temp=models.IntegerField()
    good_str=models.CharField(max_length=50)
    good_num=models.CharField(max_length=50)
    customer_id=models.IntegerField()
    manager_id=models.IntegerField()
    status=models.CharField(max_length=50) #paid/sent/got
    submit_date=models.DateField()
    finish_date=models.DateField()

    class Meta:
        db_table="orders"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class suppliers(models.Model):
    supplier_id=models.IntegerField(primary_key=True,default=0)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)

    class Meta:
        db_table="suppliers"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class contacts(models.Model):
    contact_id=models.IntegerField(primary_key=True,default=0)
    name=models.CharField(max_length=10)
    address=models.CharField(max_length=50)
    telephone=models.CharField(max_length=15)
    email=models.EmailField()
    reg_time=models.DateField()
    supplier_id=models.IntegerField()

    class Meta:
        db_table="contacts"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class supply_orders(models.Model):
    supply_order_id=models.IntegerField(primary_key=True,default=0)
    supplier_id=models.IntegerField()
    good_str=models.CharField(max_length=50)
    goods_num=models.CharField(max_length=50)
    status=models.CharField(max_length=4)
    submit_date=models.DateField()
    finish_date=models.DateField()
    contact_id = models.IntegerField()
    manager_id = models.IntegerField()

    class Meta:
        db_table="supply_orders"

    def _str_(self):
        return self.name

@python_2_unicode_compatible
class complains(models.Model):
    complaint_id=models.IntegerField(primary_key=True,default=0)
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
        db_table="complains"

    def _str_(self):
        return self.name
























