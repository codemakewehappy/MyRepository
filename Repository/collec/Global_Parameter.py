# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from collec.models import Asset, Order, Notice
from . import models

def glpcount(request):

        if not request.user.is_authenticated():
           submitedcount = None
           recevingcount = None
           nocie_cotent = None

        else:

           recevingcount = Order.objects.filter(ordersubmitButton='YES', orderreceiveButton='NO').count()

           submitedcount = Order.objects.filter(send_vendor_comment='NO', receive_vendor_comment='YES',user=request.user).count()

           notice_sets  = Notice.objects.all()
           notice_sets_count = notice_sets.count()
           nocie_cotents = Notice.objects.filter(id=notice_sets_count)
           if (nocie_cotents.exists()):
               notice=Notice.objects.get(id=notice_sets_count)
               nocie_cotent = notice.content
           else:
               nocie_cotent = None


        return {"recevingcount":recevingcount,"submitedcount":submitedcount,"noticecontent":nocie_cotent}

def glStaues(request):
    if request.user.is_authenticated():
        sendComment = Order.objects.filter(send_vendor_comment='YES',receive_vendor_comment='NO')
        receiveComment = Order.objects.filter(send_vendor_comment='NO', receive_vendor_comment='YES')
    else:
        sendComment = []
        receiveComment =[]

    content = {"sendComments": sendComment, "receiveComments": receiveComment}
    return  content