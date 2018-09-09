# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db import models
from  django.contrib.auth.models import User
from django.utils.html import *


class Asset(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='sender')
    orderID = models.ForeignKey('Order',on_delete=models.CASCADE,verbose_name='orderID')
    Category = models.CharField(max_length=512,null=True,help_text="Category")
    PartNo =  models.CharField(max_length=512,null=True,help_text="PartNo")
    SN = models.CharField(max_length=512, null=True, help_text="SN")
    ProductDescription = models.CharField(max_length=512, null=True, help_text="ProductDescription")
    Qty = models.IntegerField(null=True, help_text="Qty")
    receiveQty = models.IntegerField(null=True,help_text="receiveQty")
    submitButton = models.CharField(max_length=512, default='NO', help_text="submitButton")
    receiveButton = models.CharField(max_length=512, default='NO', help_text="receiveButton")

    def __str__(self):
        return self.PartNo

        # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
         return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='sent_user')
    receive_user = models.CharField(max_length=512, verbose_name='receive_user')
    orderId = models.CharField(max_length=512, help_text="orderId")
    Shipfrom = models.CharField(max_length=512, null=True, help_text="shipfrom")
    Shipto = models.CharField(max_length=512, null=True, help_text="shipto")
    PO = models.CharField(max_length=512, null=True, help_text="PO")
    Forwarder = models.CharField(max_length=512, null=True, help_text="Forwarder")
    Packages = models.IntegerField(null=True, help_text="Packages")
    NetWeight = models.CharField(max_length=512, help_text="NetWeight")
    GrossWeight = models.CharField(max_length=512, help_text="GrossWeight")
    Volume = models.CharField(max_length=512, help_text="Volume")
    Tracking = models.CharField(max_length=512, help_text="Tracking")
    ordersubmitButton = models.CharField(max_length=512, default='NO', help_text="ordersubmitButton")
    orderreceiveButton = models.CharField(max_length=512, default='NO', help_text="orderreceiveButton")
    vendorcomments = models.CharField(max_length=512,null=True,help_text="vendorcomments")
    receivecommets = models.CharField(max_length=512,null=True,help_text="receivecommets")
    sendOrder_time = models.DateTimeField(null=True,help_text="send_Order_time")
    receiveOrder_time = models.DateTimeField(null=True,help_text="receive_Order_time")
    send_vendor_comment = models.CharField(max_length=512,default='NO',help_text="send_vendor_comment")
    receive_vendor_comment = models.CharField(max_length=512,default='NO',help_text="receive_vendor_comment")
    create_Order_time = models.DateTimeField(null=True,help_text="create_Order_time")

    def __str__(self):
        return self.orderId

    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Contact = models.EmailField(null=True)
    Phone = models.CharField(max_length=255)

class ExtendUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Country = models.CharField(max_length=255, help_text="Country", null=True)
    City = models.CharField(max_length=255, help_text="City", null=True)
    Email = models.EmailField(max_length=255,help_text="Email",null=True)
    Phone = models.CharField(max_length=255,help_text="Phone",null=True)
    clear_password =models.CharField(max_length=255,null=True)
    User_Status = models.CharField(max_length=255,null=True,default='vendor')



class Notice(models.Model):
    content = models.CharField(max_length=255, help_text="content", null=True)