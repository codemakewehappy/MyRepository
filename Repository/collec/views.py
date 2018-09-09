# -*- coding:utf-8 -*-
import os
import sys
import StringIO
import xlwt

reload(sys)
sys.setdefaultencoding('utf-8')
import xlrd
from django.contrib import auth
from django.http import HttpResponseRedirect, response
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
import json
from django.contrib.auth import authenticate, login, logout, user_logged_out
from django.contrib.auth.models import User
from collec.forms import ChangePasswordForm
from collec.models import Asset, Order, ExtendUser, Notice
from . import models
from django.core.mail import send_mail, EmailMultiAlternatives

from django.db.models import Q
from datetime import datetime
from Repository import settings
# from django.utils import timezone
# from django.utils import timezone as datetime

def receive(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'collec/receiveOrder.html')
    else:
        return HttpResponseRedirect('/login/')

def submit(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return render(request,'collec/submited.html')
    else:
        return HttpResponseRedirect('/login/')

def index(request):
    if request.user.is_authenticated:
       return render(request, 'collec/index.html')
    else:
       return HttpResponseRedirect('/login/')

def detail(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'collec/detail.html')
    else:
        return HttpResponseRedirect('/login/')

def createOrder(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.POST:
            if request.POST.has_key('submit'):
                ord = request.POST.get('Order')
                vendorcomments = request.POST.get('vendorcomments')
                apo = request.POST.get('PO')
                apg = request.POST.get('Packages')
                agw = request.POST.get('GrossWeight')
                av = request.POST.get('Volume')
                af = request.POST.get('Forwarder')
                at = request.POST.get('Tracking')
                fromcompany = request.POST.get('shipfromcompany')
                fromcity = request.POST.get('shipfromcity')
                fromcontact = request.POST.get('shipfromcontact')
                fromphone = request.POST.get('shipfromphone')
                tocompany = request.POST.get('shiptocompany')
                tocity = request.POST.get('shiptocity')
                tocontact = request.POST.get('shiptocontact')
                tophone = request.POST.get('shiptophone')
                apartno = request.POST.getlist('PartNo', '')
                asn = request.POST.getlist('SN', '')
                aqty = request.POST.getlist('Qty', '')
                apd = request.POST.getlist('ProductDescription', '')
                acategorys = request.POST.getlist('loc', '')
                receiveuser = request.POST.get('receive_user')
                asf = fromcompany + '/' + fromcity+'/'+ fromcontact + '/' + fromphone
                aso = tocompany + '/' + tocity + '/' + tocontact + '/' + tophone
                us = request.user
                sendTime = datetime.now()
                createTime = datetime.now()
                commentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                if (vendorcomments and not (vendorcomments.strip() =='')):
                        vendorcomments = commentTime+'  '+vendorcomments
                        orde = Order.objects.create(orderId=ord, receive_user=receiveuser,vendorcomments=vendorcomments, ordersubmitButton='YES',
                                                    orderreceiveButton='NO', user=us, Tracking=at, Shipfrom=asf,
                                                    Shipto=aso,
                                                    PO=apo, Packages=apg, GrossWeight=agw, Volume=av,
                                                    Forwarder=af, send_vendor_comment='YES',
                                                    receive_vendor_comment='NO', sendOrder_time=sendTime,create_Order_time=createTime)
                else:
                        orde = Order.objects.create(orderId=ord, receive_user=receiveuser,vendorcomments=vendorcomments, ordersubmitButton='YES',
                                                    orderreceiveButton='NO', user=us, Tracking=at, Shipfrom=asf,
                                                    Shipto=aso,
                                                    PO=apo, Packages=apg, GrossWeight=agw, Volume=av,
                                                    Forwarder=af, sendOrder_time=sendTime,create_Order_time=createTime)


                for i in range(len(apartno)):
                        models.Asset.objects.create(PartNo=apartno[i], SN=asn[i], Qty=aqty[i],Category=acategorys[i],
                                                    ProductDescription=apd[i],
                                                    user=us, orderID=orde, submitButton='YES')


                return HttpResponseRedirect('/collec/createOrder/')

            elif request.POST.has_key('save'):
                ord = request.POST.get('Order')
                vendorcomments = request.POST.get('vendorcomments')
                apo = request.POST.get('PO')
                apg = request.POST.get('Packages')
                agw = request.POST.get('GrossWeight')
                av = request.POST.get('Volume')
                af = request.POST.get('Forwarder')
                at = request.POST.get('Tracking')
                fromcompany = request.POST.get('shipfromcompany')
                fromcity = request.POST.get('shipfromcity')
                fromcontact = request.POST.get('shipfromcontact')
                fromphone = request.POST.get('shipfromphone')
                tocompany = request.POST.get('shiptocompany')
                tocity = request.POST.get('shiptocity')
                tocontact = request.POST.get('shiptocontact')
                tophone = request.POST.get('shiptophone')
                apartno = request.POST.getlist('PartNo', '')
                asn = request.POST.getlist('SN', '')
                aqty = request.POST.getlist('Qty', '')
                apd = request.POST.getlist('ProductDescription', '')
                acategorys =  request.POST.getlist('loc','')
                receiveuser = request.POST.get('receive_user')
                asf = fromcompany + '/' + fromcity + '/' + fromcontact + '/' + fromphone
                aso = tocompany   + '/' + tocity  + '/' + tocontact + '/' + tophone
                us = request.user
                createTime = datetime.now()
                commentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))




                if(vendorcomments and not (vendorcomments.strip()=='')):
                     vendorcomments = commentTime + '  ' + vendorcomments
                     orddd = Order.objects.create(ordersubmitButton='NO',receive_user=receiveuser,orderId=ord,vendorcomments=vendorcomments,
                                                             orderreceiveButton='NO', user=us, Tracking=at, create_Order_time=createTime,
                                                             Shipfrom=asf, Shipto=aso,
                                                             PO=apo, Packages=apg, GrossWeight=agw,
                                                             Volume=av,
                                                             Forwarder=af)

                else:
                    orddd = Order.objects.create(ordersubmitButton='NO', receive_user=receiveuser,orderId=ord,vendorcomments=vendorcomments,
                                                     orderreceiveButton='NO', user=us, Tracking=at,
                                                     create_Order_time=createTime,
                                                     Shipfrom=asf, Shipto=aso,
                                                     PO=apo, Packages=apg, GrossWeight=agw,
                                                     Volume=av,
                                                     Forwarder=af)


                for i in range(len(apartno)):
                        models.Asset.objects.create(PartNo=apartno[i],SN=asn[i],Qty=aqty[i],Category=acategorys[i],ProductDescription=apd[i],user=us,submitButton='NO',orderID=orddd)


                return HttpResponseRedirect('/collec/createOrder/')

        else:
           generateorder = request.user.username +datetime.now().strftime("%Y%m%d%H%M%S")

           receive_list =User.objects.filter(is_superuser=1,is_staff=0)

           return render(request, 'collec/addOrder.html', {"generateorder": generateorder,'receives':receive_list})
    else:
        return HttpResponseRedirect('/login/')

def addOrder(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.POST:
            if request.POST.has_key('submit'):
                ord = request.POST.get('Order')
                vendorcomments = request.POST.get('vendorcomments')
                apo = request.POST.get('PO')
                apg = request.POST.get('Packages')
                agw = request.POST.get('GrossWeight')
                av = request.POST.get('Volume')
                af = request.POST.get('Forwarder')
                at = request.POST.get('Tracking')
                asf = request.POST.get('Shipfrom')
                aso = request.POST.get('Shipto')
                apartno = request.POST.getlist('PartNo','')
                asn = request.POST.getlist('SN','')
                aqty = request.POST.getlist('Qty','')
                apd = request.POST.getlist('ProductDescription','')
                acategorys = request.POST.getlist('loc', '')
                us = request.user
                sendTime = datetime.now()

                orddd = Order.objects.get(orderId=ord)
                atts = Asset.objects.filter(orderID=orddd)

                reccoment = vendorcomments
                if (vendorcomments == None or not vendorcomments.strip()):
                    ex_length = 0
                else:
                    ex_length = len(reccoment)

                odd = Order.objects.get(orderId=ord)
                lastcomment_sql = odd.vendorcomments
                lastcomment = str(lastcomment_sql)
                if (lastcomment_sql == None):
                    index = 0

                else:
                    index = len(lastcomment_sql)


                commentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                if (ex_length <= index):
                    reccoments = lastcomment_sql

                else:
                    newcomment = reccoment[index:]

                    if (index == 0):

                        if (newcomment.strip()):
                            newcomment = str(newcomment.strip())
                            reccoments = commentTime + '   ' + newcomment

                        else:
                            reccoments = lastcomment_sql

                    else:
                        old_ex_comment = reccoment[:index]

                        if (old_ex_comment == lastcomment and newcomment.strip()):
                            newcomment = str(newcomment.strip())
                            reccoments = lastcomment + '\n' + commentTime + '  ' + newcomment

                        else:
                            reccoments = lastcomment_sql


                if(vendorcomments and not (vendorcomments.strip()=='')):
                        Order.objects.filter(orderId=ord).update(vendorcomments=reccoments, ordersubmitButton='YES',
                                                             orderreceiveButton='NO', user=us, Tracking=at,
                                                             Shipfrom=asf, Shipto=aso,
                                                             PO=apo, Packages=apg, GrossWeight=agw,
                                                             Volume=av,
                                                             Forwarder=af,send_vendor_comment='YES',receive_vendor_comment='NO',sendOrder_time=sendTime)
                else:
                        Order.objects.filter(orderId=ord).update(vendorcomments=reccoments, ordersubmitButton='YES',
                                                                 orderreceiveButton='NO', user=us, Tracking=at,
                                                                 Shipfrom=asf, Shipto=aso,
                                                                 PO=apo, Packages=apg, GrossWeight=agw,
                                                                 Volume=av,
                                                                 Forwarder=af,sendOrder_time=sendTime)

                for i in range(len(apartno)):
                        aid = atts[i].id
                        models.Asset.objects.filter(id=aid).update(PartNo=apartno[i], SN=asn[i], Qty=aqty[i],Category=acategorys[i],
                                                                   ProductDescription=apd[i],
                                                                   user=us, submitButton='YES')

                return HttpResponseRedirect('/collec/submit/')

            elif request.POST.has_key('save'):
                ord = request.POST.get('Order')
                vendorcomments = request.POST.get('vendorcomments')
                apo = request.POST.get('PO')
                apg = request.POST.get('Packages')
                agw = request.POST.get('GrossWeight')
                av = request.POST.get('Volume')
                af = request.POST.get('Forwarder')
                at = request.POST.get('Tracking')
                asf = request.POST.get('Shipfrom')
                aso = request.POST.get('Shipto')
                apartno = request.POST.getlist('PartNo', '')
                asn = request.POST.getlist('SN', '')
                aqty = request.POST.getlist('Qty', '')
                apd = request.POST.getlist('ProductDescription', '')
                acategorys = request.POST.getlist('loc', '')

                us = request.user

                orddd= Order.objects.get(orderId=ord)
                atts = Asset.objects.filter(orderID=orddd)

                reccoment_ex = vendorcomments
                reccoment = str(reccoment_ex)
                ex_length = len(reccoment)
                odd = Order.objects.get(orderId=ord)
                lastcomment_sql = odd.vendorcomments
                lastcomment = str(lastcomment_sql)
                index = len(lastcomment)

                commentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                if (ex_length <= index):
                    reccoments = lastcomment_sql
                else:
                    newcomment = reccoment[index:]
                    if (index == 0):
                        if (newcomment.strip()):
                            newcomment = newcomment.strip()
                            reccoments = commentTime + '  ' + newcomment
                        else:
                            reccoments = lastcomment
                    else:
                        old_ex_comment = reccoment[:index]
                        if (old_ex_comment == lastcomment and newcomment.strip()):
                            newcomment = newcomment.strip()
                            reccoments = lastcomment + '\n' + commentTime + '  ' + newcomment
                        else:
                            reccoments = lastcomment

                if (vendorcomments and not (vendorcomments.strip() == '')):
                    Order.objects.filter(orderId=ord).update(vendorcomments=reccoments, ordersubmitButton='NO',
                                                    orderreceiveButton='NO', user=us, Tracking=at, Shipfrom=asf, Shipto=aso,
                                                    PO=apo, Packages=apg,GrossWeight=agw, Volume=av,
                                                    Forwarder=af)
                else:
                    Order.objects.filter(orderId=ord).update(vendorcomments=reccoments, ordersubmitButton='NO',
                                                             orderreceiveButton='NO', user=us, Tracking=at,
                                                             Shipfrom=asf, Shipto=aso,
                                                             PO=apo, Packages=apg, GrossWeight=agw, Volume=av,
                                                             Forwarder=af)
                for i in range(len(apartno)):
                        aid = atts[i].id
                        models.Asset.objects.filter(id=aid).update(PartNo=apartno[i], SN=asn[i], Qty=aqty[i],Category=acategorys[i],
                                                    ProductDescription=apd[i],
                                                    user=us,submitButton='NO')


                ors = Order.objects.filter(orderId=ord)
                asts = Asset.objects.filter(orderID=ors[0])

                return render(request,'collec/saveaddOrder.html/',{"ord":ors[0],"assts":asts})

            return HttpResponseRedirect('/collec/submit/')
    else:
        return HttpResponseRedirect('/login/')

def receiveOrder(request,ord_id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.POST:
            receivecomments = request.POST.get('receivecomments')

            ord = Order.objects.get(orderId=ord_id)
            Order.objects.filter(orderId=ord_id).update(receivecommets=receivecomments)
            ass = ord.asset_set.all()
            for aset in ass:
                Asset.objects.filter(id=aset.id).update(receiveButton='YES',receiveQty=aset.receiveQty)

            Order.objects.filter(orderId=ord_id).update(orderreceiveButton='YES')
            return HttpResponseRedirect('/collec/receive/')
    else:
        return HttpResponseRedirect('/login/')

def sendAssetAmount(request):
        if request.is_ajax():
            asset_id = request.GET.get("asset_id")
            amount = request.GET.get("amount")
            Asset.objects.filter(id=asset_id).update(receiveQty=amount)
            Asset.objects.filter(id=asset_id).update(receiveButton='YES')
            ret = {"amount":amount}
            return HttpResponse(json.dumps(ret))

def my_logout(request):
    if request.user.is_authenticated:
          logout(request)
          return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')

def changepd(request):
    if request.user.is_authenticated:
        er = []
        username = request.user.username
        if request.user.is_staff == 1:
            if request.method == 'POST':
                form = ChangePasswordForm(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    old_password = data['old_password']
                    new_password1 = data['new_password1']
                    new_password2 = data['new_password2']

                    user = authenticate(request, username=username, password=old_password)
                    if user is not None:

                        # Redirect to a success page.
                        if new_password1 == new_password2:
                            user.set_password(new_password1)
                            user.save()
                            ExtendUser.objects.filter(user=user).update(clear_password=new_password1)
                            return HttpResponseRedirect('/login/')
                        else:
                            er.append('Please input same new password!')
                    else:
                        # Return an 'invalid login' error message.
                        er.append('Please input the correct old password !')
            else:
                er = []
                print 'execute program to changepassword'
            return render(request, 'admin_user_changepd.html', {'er': er})
        else:
            if request.method == 'POST':
                form = ChangePasswordForm(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    old_password = data['old_password']
                    new_password1 = data['new_password1']
                    new_password2 = data['new_password2']

                    user = authenticate(request, username=username, password=old_password)
                    if user is not None:

                        # Redirect to a success page.
                        if new_password1 == new_password2:
                            user.set_password(new_password1)
                            user.save()
                            ExtendUser.objects.filter(user=user).update(clear_password=new_password1)
                            return HttpResponseRedirect('/login/')
                        else:
                            er.append('Please input same new password!')
                    else:
                        # Return an 'invalid login' error message.
                        er.append('Please input the correct old password !')
            else:
                er = []
                print 'execute program to changepassword'
            return render(request, 'changepassword.html', {'er': er})
    else:
        return HttpResponseRedirect('/login/')

def vendormanage(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users=User.objects.all()
        return render(request,'collec/vendorMange.html',{"users":users})
    else:
        return HttpResponseRedirect('/login/')

def deleteUser(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
       User.objects.filter(id=id).delete()
       return HttpResponseRedirect('/collec/vendormanage/')
    else:
        return HttpResponseRedirect('/login/')

def addUser(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            tuname = request.GET.get("uname")
            tupassword = request.GET.get("upassword")
            tuemail = request.GET.get("uemail")
            tufirstname =request.GET.get("ufirstname")
            tulastname = request.GET.get("ulastname")
            tuphone = request.GET.get("uphone")
            usr=User.objects.create_user(username=tuname,email=tuemail,password=tupassword)
            User.objects.filter(username=tuname).update(first_name=tufirstname)
            User.objects.filter(username=tuname).update(last_name=tulastname)
            exusr = ExtendUser.objects.create(user=usr,Phone=tuphone,clear_password=tupassword)
            exusr.save()
            email_name = []
            user_email = tuemail
            email_name.append(user_email)
            subject = 'Notify:Login Information.'
            text_context = 'Dear' + tuname + 'this is your Login account :' + tuname + ' and password'+tupassword
            html_msg = '<a href="10.110.23.85/login">10.110.23.85/login</a>'
            #Post_mail(email_name, subject, text_context, html_msg)

            ret = {"infor": "adduser operation success!!!"}
            return HttpResponse(json.dumps(ret))
    else:
        return HttpResponseRedirect('/login/')

#获取已提交但未接收订�?
def orajax(request):
    if request.is_ajax():
        order_set = Order.objects.filter(ordersubmitButton='YES',orderreceiveButton='NO',receive_user=request.user.username).values('orderId','Forwarder', 'GrossWeight','PO', 'Packages', 'Shipfrom', 'Shipto','Tracking','Volume','vendorcomments','receivecommets','sendOrder_time')
        for ordd in order_set:
            if(ordd['receivecommets'] ==None or ordd['receivecommets']==''):
                 ordd['receivecommets'] =''
            ordd['sendOrder_time'] = datetime.strftime(ordd['sendOrder_time'], '%Y-%m-%d %H:%M:%S')

        data_list = list(order_set)
        data = {"data":data_list}
        return HttpResponse(json.dumps(data))

#获取指定订单下的详细目录
def asetajax(request):
    if request.is_ajax():
        ordId  = request.GET.get("orderId")
        ord = Order.objects.get(orderId=ordId)
        asets = Asset.objects.filter(orderID=ord).values('id','Category','PartNo','SN', 'ProductDescription', 'Qty','receiveButton','receiveQty')
        asetsl = list(asets)
        datas = {"data": asetsl}
        return HttpResponse(json.dumps(datas))

def ajaxrecveorder(request):
    if request.is_ajax():
        oid=request.GET.get("ordid")
        comts=request.GET.get("coments")
        receiveTime = datetime.now()

        reccoment = comts
        if (comts == None or not comts.strip()):
            ex_length = 0
        else:
            ex_length = len(reccoment)
        odd = Order.objects.get(orderId=oid)
        lastcomment_sql = odd.receivecommets
        lastcomment = str(lastcomment_sql)
        if (lastcomment_sql == None):
            index = 0
        else:
            index = len(lastcomment_sql)

        commentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if (ex_length <= index):
            reccoments = lastcomment_sql
        else:
            newcomment = reccoment[index:]
            print newcomment
            if (index == 0):
                if (newcomment.strip()):
                    newcomment = str(newcomment.strip())
                    reccoments = commentTime + '  ' + newcomment
                else:
                    reccoments = lastcomment
            else:
                old_ex_comment = reccoment[:index]
                if (old_ex_comment == lastcomment and newcomment.strip()):
                    newcomment = str(newcomment.strip())
                    reccoments = lastcomment + '\n' + commentTime + '  ' + newcomment
                else:
                    reccoments = lastcomment

        user_name = request.user.username
        usr= models.User.objects.get(username=user_name)
        email_name = []
        user_email = usr.email
        email_name.append(user_email)
        subject = 'Notify:Order Received.'
        text_context = 'Dear'+user_name+'  you sent shipment ID :'+oid+' have received! you can login '
        html_msg = '<a href="10.110.23.85/login" target="_blank">10.110.23.85/login</a>'
        Order.objects.filter(orderId=oid).update(receivecommets=reccoments,orderreceiveButton='YES',send_vendor_comment='YES',receive_vendor_comment='YES',receiveOrder_time=receiveTime)
       # Post_mail(email_name,subject,text_context,html_msg)

        ret = {"data": 'Succesful'}
        return HttpResponse(json.dumps(ret))

#获取已经接收的所有order
def ajaxreceived(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            order_set = Order.objects.filter(orderreceiveButton='YES',ordersubmitButton='YES',receive_user=request.user.username).values('orderId', 'Forwarder', 'GrossWeight',
                                                                             'NetWeight', 'PO', 'Packages', 'Shipfrom',
                                                                             'Shipto', 'Tracking', 'Volume',
                                                                             'vendorcomments','receivecommets','sendOrder_time','receiveOrder_time')


            for ordd in order_set:
                 from datetime import datetime
                 ordd['sendOrder_time'] =  datetime.strftime(ordd['sendOrder_time'],'%Y-%m-%d %H:%M:%S')
                 ordd['receiveOrder_time'] = datetime.strftime(ordd['receiveOrder_time'],'%Y-%m-%d %H:%M:%S')


            data_list = list(order_set)
            data = {"data": data_list}
            return HttpResponse(json.dumps(data))
    else:
        return HttpResponseRedirect('/login/')

#获取已经接收的单条order下的详细物品
def receivedassetajax(request):
    if request.is_ajax():
        ordId  = request.GET.get("orderId")
        ord = Order.objects.get(orderId=ordId)
        asets = Asset.objects.filter(orderID=ord,receiveButton='YES').values('Category','PartNo','SN', 'ProductDescription', 'Qty','receiveQty')
        asetsl = list(asets)
        datas = {"data": asetsl}
        return HttpResponse(json.dumps(datas))

def updateOrder(request,ord):
    if request.user.is_authenticated:
         ors = Order.objects.filter(orderId=ord)
         asts = Asset.objects.filter(orderID=ors[0])
         return render(request, 'collec/saveaddOrder.html', {"ord": ors[0], "assts": asts})
    else:
        return HttpResponseRedirect('/login/')

#已经创建好的order，在Shipment order页面中提�?
def ajax_vendor_send(request):
    if request.is_ajax:
        ord_id = request.GET.get("ordid")
        reccoment_ex = request.GET.get("coments")
        sendTime = datetime.now()
        reccoment =reccoment_ex
        if(reccoment_ex == None or not  reccoment_ex.strip()):
            ex_length = 0
        else:
            ex_length = len(reccoment)
        odd = Order.objects.get(orderId=ord_id)
        lastcomment_sql  =odd.vendorcomments
        lastcomment= str(lastcomment_sql)
        if(lastcomment_sql == None):
            index = 0
        else:
            index = len(lastcomment_sql)
        commentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if(ex_length <= index ):
            reccoments = lastcomment_sql

        else:
            newcomment = reccoment[index:]
            if(index==0):
                if(newcomment.strip()):
                    newcomment = str(newcomment.strip())
                    reccoments = commentTime+'   '+newcomment
                else:
                    reccoments = lastcomment_sql
            else:
                old_ex_comment = reccoment[:index]
                if(old_ex_comment == lastcomment and  newcomment.strip()):
                    newcomment = str(newcomment.strip())
                    reccoments = lastcomment+'\n'+commentTime+'  '+newcomment
                else:
                    reccoments = lastcomment_sql

        if(reccoment_ex):
            Order.objects.filter(orderId=ord_id).update(vendorcomments=reccoments,send_vendor_comment='YES',receive_vendor_comment='NO',ordersubmitButton='YES',sendOrder_time = sendTime)
        else:
            Order.objects.filter(orderId=ord_id).update(vendorcomments=reccoments, send_vendor_comment='NO',
                                                        receive_vendor_comment='NO',ordersubmitButton='YES',sendOrder_time = sendTime)
        ret = {"info": "successful"}
        return HttpResponse(json.dumps(ret))

#获取vendor 保存到系统中的所有order，包括received、sent、create
def ajaxsubmited(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            order_set = Order.objects.filter(user=request.user).values('orderId','orderreceiveButton','ordersubmitButton',
                                                                                                       'Forwarder',
                                                                                                       'GrossWeight',
                                                                                                       'PO', 'Packages',
                                                                                                       'Shipfrom',
                                                                                                       'Shipto',
                                                                                                       'Tracking',
                                                                                                       'Volume',
                                                                                                       'vendorcomments',
                                                                                                       'receivecommets','sendOrder_time','receiveOrder_time')

            for ordd in order_set:
                if(ordd['vendorcomments']==None or ordd['vendorcomments']==''):
                    ordd['vendorcomments'] = ''
                if(ordd['receivecommets']==None or ordd['receivecommets']==''):
                    ordd['receivecommets'] = ''
                if (ordd['orderreceiveButton'] == 'YES' and ordd['ordersubmitButton'] == 'YES'):
                    ordd['sendOrder_time'] = datetime.strftime(ordd['sendOrder_time'], '%Y-%m-%d %H:%M:%S')
                    ordd['receiveOrder_time'] = datetime.strftime(ordd['receiveOrder_time'], '%Y-%m-%d %H:%M:%S')
                    ordd['orderreceiveButton'] ='approved'
                elif(ordd['orderreceiveButton'] == 'NO' and ordd['ordersubmitButton'] == 'YES'):
                    ordd['sendOrder_time'] = datetime.strftime(ordd['sendOrder_time'], '%Y-%m-%d %H:%M:%S')
                    ordd['receiveOrder_time'] = '---'
                    ordd['orderreceiveButton'] = 'shipped'
                else:
                    ordd['sendOrder_time'] = '---'
                    ordd['receiveOrder_time'] = '---'
                    ordd['orderreceiveButton'] = 'draft'
            data_list = list(order_set)
            data = {"data": data_list}
            return HttpResponse(json.dumps(data))
    else:
        return HttpResponseRedirect('/login/')

#获取vendor 保存到系统中的order的单条物品详细信�?
def submitedassetajax(request):
    if request.is_ajax():
        ordId = request.GET.get("orderId")
        ord = Order.objects.get(orderId=ordId)
        asets = Asset.objects.filter(orderID=ord).values('Category','PartNo', 'SN', 'ProductDescription',
                                                                              'Qty', 'receiveQty')

        for aset in asets:
            if( aset['receiveQty']==None or aset['receiveQty'] =='' ):
                aset['receiveQty'] ='--'


        asetsl = list(asets)
        datas = {"data": asetsl}
        return HttpResponse(json.dumps(datas))

#received side 取消接收单条order下的物品数量
def cancleReceiveAmount(request):
    if request.is_ajax():
        asset_id = request.GET.get("asset_id")
        Asset.objects.filter(id=asset_id).update(receiveQty=None)
        Asset.objects.filter(id=asset_id).update(receiveButton='NO')
        ret = {"info":'successful'}
        return HttpResponse(json.dumps(ret))

#receive side add Comment
def ajax_saveReceive(request):
    if request.is_ajax:
        ord_id = request.GET.get("ordid")
        reccoment_ex = request.GET.get("coments")
        reccoment =reccoment_ex
        if(reccoment_ex == None or not reccoment_ex.strip()):
            ex_length = 0
        else:
            ex_length = len(reccoment)
        odd = Order.objects.get(orderId=ord_id)
        lastcomment_sql  =odd.receivecommets
        lastcomment= str(lastcomment_sql)
        if(lastcomment_sql == None):
            index = 0
        else:
            index = len(lastcomment_sql)

        commentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if(ex_length <= index):
            reccoments = lastcomment_sql
        else:
            newcomment = reccoment[index:]
            print newcomment
            if(index==0):
                if(newcomment.strip()):
                    newcomment = str(newcomment.strip())
                    reccoments = commentTime+'  '+newcomment
                else:
                    reccoments = lastcomment
            else:
                old_ex_comment = reccoment[:index]
                if(old_ex_comment == lastcomment and  newcomment.strip()):
                    newcomment = str(newcomment.strip())
                    reccoments = lastcomment+'\n'+commentTime+'  '+newcomment
                else:
                    reccoments = lastcomment

        Order.objects.filter(orderId=ord_id).update(receivecommets=reccoments,send_vendor_comment='NO',receive_vendor_comment='YES')

        user_name = request.user.username
        usr = models.User.objects.get(username=user_name)
        email_name = []
        user_email = usr.email
        email_name.append(user_email)
        subject = 'Notify:Order Coment changed.'
        text_context = 'Dear' + user_name + ',you sent shipment ID :' + ord_id + ' Comment have changed! you can login'
        html_msg = '<a href="10.110.23.85/login"></a>'
        #Post_mail(email_name, subject, text_context,html_msg)

        ret = {"info":"successful"}
        return HttpResponse(json.dumps(ret))

#vendor side add Comment
def ajax_vendorcomment_save(request):
    if request.is_ajax:
        ord_id = request.GET.get("ordid")
        vendorcoment = request.GET.get("coments")
        reccoment_ex =vendorcoment
        reccoment = str(reccoment_ex)
        ex_length = len(reccoment)
        odd = Order.objects.get(orderId=ord_id)
        lastcomment_sql = odd.vendorcomments
        lastcomment = str(lastcomment_sql)
        index = len(lastcomment)

        commentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if (ex_length <= index):
            reccoments = lastcomment_sql
        else:
            newcomment = reccoment[index:]
            if (index == 0):
                if (newcomment.strip()):
                    newcomment = newcomment.strip()
                    reccoments = commentTime + '  ' + newcomment
                else:
                    reccoments = lastcomment
            else:
                old_ex_comment = reccoment[:index]
                if (old_ex_comment == lastcomment and newcomment.strip()):
                    newcomment = newcomment.strip()
                    reccoments = lastcomment + '\n' + commentTime + '  ' + newcomment
                else:
                    reccoments = lastcomment
        Order.objects.filter(orderId=ord_id).update(vendorcomments=reccoments,send_vendor_comment='YES',receive_vendor_comment='NO')
        ret = {"info": "successful"}
        return HttpResponse(json.dumps(ret))


def searchorder(request):

    if request.user.is_superuser:
        condition1 = request.POST.get('Order')
        condition2 = request.POST.get('PO')
        condition3 = request.POST.get('Forwarder')
        condition4 = request.POST.get('Tracking')
        condition5 = request.POST.get('Shipfrom')
        condition6 = request.POST.get('Shipto')
        condition7 = request.POST.get('PartNo')
        condition8 = request.POST.get('ProductDescription')
        condition9 = request.POST.get('SN')
        condition10 = request.POST.get('fromTime')
        condition11 = request.POST.get('toTime')
        condition12 = request.POST.get('loc')

    else:
        condition1 = request.POST.get('Order')
        condition2 = request.POST.get('PO')
        condition3 = request.POST.get('Forwarder')
        condition4 = request.POST.get('Tracking')
        condition5 = request.POST.get('Shipfrom')
        condition6 = request.POST.get('Shipto')
        condition7 = None
        condition8 = None
        condition9 = None
        condition10 = request.POST.get('fromTime')
        condition11 = request.POST.get('toTime')
        condition12 = request.POST.get('loc')

    return render(request,'collec/searchResult.html', {'orderIds': condition1, 'POs': condition2, 'Forwarders': condition3, 'Trackings': condition4, 'Shipfroms': condition5, 'Shiptos': condition6, 'PartNos': condition7, 'ProductDescriptions': condition8, 'SNs': condition9, 'fromTimes': condition10, 'toTimes': condition11, 'selectvalue': condition12})

#根据输入的条件字段，返回搜索的order数据
def ajax_searchOrder(request):
    condition1 = request.GET.get('orderId')
    condition2 = request.GET.get('PO')
    condition3 = request.GET.get('Forwarder')
    condition4 = request.GET.get('Tracking')
    condition5 = request.GET.get('Shipfrom')
    condition6 = request.GET.get('Shipto')
    condition7 = request.GET.get('PartNo')
    condition8 = request.GET.get('ProductDescription')
    condition9 = request.GET.get('SN')
    condition10 = request.GET.get('fromTime')
    condition11 = request.GET.get('toTime')
    condition12 = request.GET.get('selectval')



    if(request.user.is_superuser):
        if (not condition1 and not condition2 and not condition3 and not condition4 and not condition5 and not condition6 and not condition7 and not condition8 and not condition9 and not condition10 and not condition11 and not condition12):
            order_set = Order.objects.filter(ordersubmitButton='YES',receive_user=request.user.username).values('orderId', 'Forwarder', 'GrossWeight',
                                                       'PO', 'Packages',
                                                      'Shipfrom',
                                                      'Shipto', 'Tracking', 'Volume',
                                                      'vendorcomments', 'receivecommets', 'orderreceiveButton',
                                                      'sendOrder_time', 'receiveOrder_time')

            for ordd in order_set:
                if (ordd['orderreceiveButton'] == 'YES'):
                    ordd['sendOrder_time'] = datetime.strftime(ordd['sendOrder_time'], '%Y-%m-%d %H:%M:%S')
                    ordd['receiveOrder_time'] = datetime.strftime(ordd['receiveOrder_time'], '%Y-%m-%d %H:%M:%S')
                else:
                    ordd['sendOrder_time'] = datetime.strftime(ordd['sendOrder_time'], '%Y-%m-%d %H:%M:%S')
                    ordd['receiveOrder_time'] = '---'

            data_list = list(order_set)
            data = {"data": data_list}
            return HttpResponse(json.dumps(data))

        else:
            if(condition12 == 'approved'):
                if (condition10 and condition11):

                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES', orderreceiveButton='YES',
                                                     receiveOrder_time__range=(condition10, condition11)).distinct()
                elif (condition10):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES', orderreceiveButton='YES',
                                                     receiveOrder_time__gt=condition10).distinct()
                elif (condition11):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES', orderreceiveButton='YES',
                                                     receiveOrder_time__lt=condition11).distinct()
                else:
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES', orderreceiveButton='YES'
                                                     ).distinct()
            elif(condition12 == 'shipped'):
                if (condition10 and condition11):

                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',orderreceiveButton='NO',
                                                     sendOrder_time__range=(condition10, condition11)).distinct()
                elif (condition10):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',orderreceiveButton='NO',
                                                     sendOrder_time__gt=condition10).distinct()
                elif (condition11):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',orderreceiveButton='NO',
                                                     sendOrder_time__lt=condition11).distinct()
                else:
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',orderreceiveButton='NO',
                                                     ).distinct()
            else:
                if (condition10 and condition11):

                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',
                                                     sendOrder_time__range=(condition10, condition11)).distinct()
                elif (condition10):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',
                                                     sendOrder_time__gt=condition10).distinct()
                elif (condition11):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',
                                                     sendOrder_time__lt=condition11).distinct()
                else:
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,receive_user=request.user.username,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',
                                                     ).distinct()


    else:
        if ( not condition1 and not condition2 and not condition3 and not condition4 and not condition5 and not condition6 and not condition10 and not condition11 and not condition12):

            order_set = Order.objects.filter(user=request.user).values('orderId', 'Forwarder', 'GrossWeight',
                                                                       'PO', 'Packages',
                                                                       'Shipfrom','ordersubmitButton',
                                                                       'Shipto', 'Tracking', 'Volume',
                                                                       'vendorcomments',
                                                                       'orderreceiveButton',
                                                                       'receivecommets', 'sendOrder_time',
                                                                       'receiveOrder_time').distinct()

            for ordd in order_set:
                if (ordd['orderreceiveButton'] == 'YES' and ordd['ordersubmitButton'] =='YES'):
                    ordd['sendOrder_time'] = datetime.strftime(ordd['sendOrder_time'], '%Y-%m-%d %H:%M:%S')
                    ordd['receiveOrder_time'] = datetime.strftime(ordd['receiveOrder_time'], '%Y-%m-%d %H:%M:%S')
                elif(ordd['orderreceiveButton'] == 'NO' and ordd['ordersubmitButton'] =='YES'):
                    ordd['sendOrder_time'] = datetime.strftime(ordd['sendOrder_time'], '%Y-%m-%d %H:%M:%S')
                    ordd['receiveOrder_time'] = '---'
                else:
                    ordd['sendOrder_time'] = '---'
                    ordd['receiveOrder_time'] = '---'

            data_list = list(order_set)
            data = {"data": data_list}
            return HttpResponse(json.dumps(data))

        else:
            if (condition12 == 'approved'):
                if (condition10 and condition11):

                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES', orderreceiveButton='YES',
                                                     user=request.user,
                                                     sendOrder_time__range=(condition10, condition11)).distinct()
                elif (condition10):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES', orderreceiveButton='YES',
                                                     user=request.user, sendOrder_time__gt=condition10).distinct()
                elif (condition11):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES', orderreceiveButton='YES',
                                                     user=request.user, sendOrder_time__lt=condition11).distinct()
                else:
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES', orderreceiveButton='YES',
                                                     user=request.user).distinct()
            elif (condition12 == 'shipped'):
                if (condition10 and condition11):

                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',orderreceiveButton='NO',
                                                     user=request.user,
                                                     sendOrder_time__range=(condition10, condition11)).distinct()
                elif (condition10):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',orderreceiveButton='NO',
                                                     user=request.user, sendOrder_time__gt=condition10).distinct()
                elif (condition11):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',orderreceiveButton='NO',
                                                     user=request.user, sendOrder_time__lt=condition11).distinct()
                else:
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='YES',orderreceiveButton='NO',
                                                     user=request.user).distinct()
            elif (condition12 == 'draft'):
                if (condition10 and condition11):

                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='NO',orderreceiveButton='NO',
                                                     user=request.user,
                                                     sendOrder_time__range=(condition10, condition11)).distinct()
                elif (condition10):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='NO',orderreceiveButton='NO',
                                                     user=request.user, sendOrder_time__gt=condition10).distinct()
                elif (condition11):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='NO',orderreceiveButton='NO',
                                                     user=request.user, sendOrder_time__lt=condition11).distinct()
                else:
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     ordersubmitButton='NO',orderreceiveButton='NO',
                                                     user=request.user).distinct()
            else:
                if (condition10 and condition11):

                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     user=request.user,
                                                     create_Order_time__range=(condition10, condition11)).distinct()
                elif (condition10):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     user=request.user, create_Order_time__gt=condition10).distinct()
                elif (condition11):
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     user=request.user, create_Order_time__lt=condition11).distinct()
                else:
                    OrdResult = Order.objects.filter(orderId__contains=condition1, PO__contains=condition2,
                                                     Forwarder__contains=condition3, Tracking__contains=condition4,
                                                     Shipfrom__contains=condition5, Shipto__contains=condition6,
                                                     user=request.user).distinct()

    if (OrdResult):
        if request.user.is_superuser:
             OrdResults = OrdResult.filter(asset__PartNo__contains=condition7,
                                      asset__ProductDescription__contains=condition8, asset__SN__contains=condition9)
        else:
            OrdResults = OrdResult.filter()

        if (OrdResults):
            order_set = OrdResults.values('orderId', 'Forwarder', 'GrossWeight',
                                           'PO', 'Packages',
                                          'Shipfrom',
                                          'Shipto', 'Tracking', 'Volume',
                                          'vendorcomments',
                                          'orderreceiveButton','ordersubmitButton',
                                          'receivecommets', 'sendOrder_time', 'receiveOrder_time')

            for ordd in order_set:
                if (ordd['orderreceiveButton'] == 'YES' and ordd['ordersubmitButton'] == 'YES'):
                    ordd['sendOrder_time'] = datetime.strftime(ordd['sendOrder_time'], '%Y-%m-%d %H:%M:%S')
                    ordd['receiveOrder_time'] = datetime.strftime(ordd['receiveOrder_time'], '%Y-%m-%d %H:%M:%S')
                elif (ordd['orderreceiveButton'] == 'NO' and ordd['ordersubmitButton'] == 'YES'):
                    ordd['sendOrder_time'] = datetime.strftime(ordd['sendOrder_time'], '%Y-%m-%d %H:%M:%S')
                    ordd['receiveOrder_time'] = '---'
                else:
                    ordd['sendOrder_time'] = '---'
                    ordd['receiveOrder_time'] = '---'
        else:
            order_set = {}
    else:
        order_set = {}

    data_list = list(order_set)
    data = {"data": data_list}
    return HttpResponse(json.dumps(data))

#返回搜索order下的物品信息
def ajax_searchasset(request):
    condition1 = request.GET.get('orderId')
    condition2 = request.GET.get('PartNo')
    condition3 = request.GET.get('ProductDescription')
    condition4 = request.GET.get('SN')
    ord = Order.objects.get(orderId=condition1)
    if request.user.is_superuser:
        asets = Asset.objects.filter(orderID=ord,PartNo__contains=condition2,ProductDescription__contains=condition3,SN__contains=condition4).values('Category','PartNo', 'SN', 'ProductDescription', 'Qty',
                                                     'receiveQty')
    else:
        asets = Asset.objects.filter(orderID=ord,user=request.user).values('Category','PartNo', 'SN', 'ProductDescription', 'Qty',
                                                     'receiveQty')

    asetsl = list(asets)
    datas = {"data": asetsl}
    return HttpResponse(json.dumps(datas))


def upload_order(request):
    return render(request,'collec/upload_order.html')

def import_excelFile(request):
    if 'cancel' in request.POST:
        return HttpResponseRedirect('/collec/upload_order/')

    wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
    ws = wb.sheets()[0]
    nrow = ws.nrows
    headers = ['PO', 'Shipfrom', 'Shipto', 'Forwarder', 'TrackingNO', 'PackagesQty', 'GrossWeight', 'Volume', 'PartNo', 'ProductDescription',
               'SN','SentQty']

    lists = []
    for row in range(1, nrow):
        r = {}
        for col in range(1, len(headers) + 1):
            key = headers[col - 1]
            r[key] = ws.cell(row, col - 1).value

        lists.append(r)

    psname = []
    count = 0
    for cell in lists:
        # for header in headers:
        po = str(cell['PO'])
        shipfrom = str(cell['Shipfrom'])
        shipto = str(cell['Shipto'])
        forward = str(cell['Forwarder'])
        trackingNO = str(cell['TrackingNO'])
        packagesQty = int(cell['PackagesQty'])
        grossWeight = int(cell['GrossWeight'])
        volume = str(cell['Volume'])
        partNo = int(cell['PartNo'])
        productDescription = str(cell['ProductDescription'])
        sn = str(cell['SN'])
        sentQty = int(cell['SentQty'])
        psname.append(po)


        sentTime = datetime.now()

        if(count == 0):
            generateorder = request.user.username + datetime.now().strftime("%Y%m%d%H%M%S")+str(count)
            oss = Order(orderId=generateorder, user=request.user, PO=po, Shipfrom=shipfrom, Shipto=shipto,
                        Forwarder=forward, Tracking=trackingNO, Packages=packagesQty, GrossWeight=grossWeight,
                        Volume=volume, sendOrder_time=sentTime, create_Order_time=sentTime)
            oss.save()
            ass = Asset(user=request.user, orderID=oss, PartNo=partNo, ProductDescription=productDescription, SN=sn,
                        Qty=sentQty)
            ass.save()

        else:
            generateorder = request.user.username + datetime.now().strftime("%Y%m%d%H%M%S")+str(count)
            xsname = psname[:count]
            if(po != '' and po not in xsname):
                oss = Order(orderId=generateorder, user=request.user, PO=po, Shipfrom=shipfrom, Shipto=shipto,
                            Forwarder=forward, Tracking=trackingNO, Packages=packagesQty, GrossWeight=grossWeight,
                            Volume=volume, sendOrder_time=sentTime, create_Order_time=sentTime)
                oss.save()
                ass = Asset(user=request.user, orderID=oss, PartNo=partNo, ProductDescription=productDescription, SN=sn,
                            Qty=sentQty)
                ass.save()

            else:
                lenth= Order.objects.filter(PO=po,user=request.user).count()
                oddd=Order.objects.filter(PO=po, user=request.user)[lenth-1]
                odd = Order.objects.get(orderId=oddd.orderId)

                ass = Asset(user=request.user, orderID=odd, PartNo=partNo, ProductDescription=productDescription, SN=sn,
                            Qty=sentQty)
                ass.save()
        count=count + 1


    return HttpResponseRedirect('/collec/upload_order/')

def download_excle(request):
        # do something
        filename = 'static/admin/Excel/Product_view_Template.xls'
        from django.http import StreamingHttpResponse
        response = StreamingHttpResponse(readFile(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=Product_view_Template.xls'
        return response

def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def orderStatus(request):
    if request.is_ajax:
        odd = request.GET.get('oddid')
        ord = Order.objects.filter(orderId=odd,send_vendor_comment='YES',receive_vendor_comment='NO')
        if(ord):
            status = 'YES'
        else:
            status = 'NO'

        datas = {"data":status}
        return HttpResponse(json.dumps(datas))

def Post_mail(emaillist,subject,text_context,html_msg):

         if emaillist != None:
      
             msg=EmailMultiAlternatives(subject,text_context,settings.DEFAULT_FROM_EMAIL, emaillist)
             msg.attach_alternative(html_msg, "text/html")
             msg.content_subtype = "html"
             msg.send()


def showInfo(request):

    return render(request,'collec/personInfo.html')

def change_personalInfo(request):
        ucountry = request.POST.get('country')
        ucity = request.POST.get('city')
        usemail = request.POST.get('email')
        uphone = request.POST.get('phone')
        User.objects.filter(username=request.user.username).update(email=usemail)
        ExtendUser.objects.filter(user=request.user).update(Country=ucountry,City=ucity,Phone=uphone)
        return HttpResponseRedirect('/collec/showInfo/')

def export(request):
    now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    file_name = 'Purchase_Order_Information' + '_'+request.user.username+'_'+now + '.xls'
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet(u'Purchase Order Information')
    if request.user.is_superuser:

        if request.user.is_staff ==0:
            headers = ['Sent User', 'Receive User','Purchase Order', 'Status','Packages Qty', 'Gross Weight ', 'Volume', 'Forwarder ', 'Tracking NO.', 'Ship From', 'Ship To',
                       'Part Number', 'Product Description', 'Serial NO./Delivery Methods', 'Sent Quantity', 'Receive Quantity']
            for i in range(0, len(headers)):
                sheet.write(0, i, headers[i])
            row = 1
            for ord in Order.objects.filter(ordersubmitButton ='YES',receive_user=request.user.username):
                for asset in Asset.objects.filter(orderID=ord):
                    sheet.write(row, 0, ord.user.username)
                    sheet.write(row, 1, ord.receive_user)
                    sheet.write(row, 2, ord.PO)
                    if(ord.ordersubmitButton =='YES' and ord.orderreceiveButton =='YES'):
                        sheet.write(row, 3, 'Approved')
                    else:
                        sheet.write(row, 3, 'Shipped')
                    sheet.write(row, 4, ord.Packages)
                    sheet.write(row, 5, ord.GrossWeight)
                    sheet.write(row, 6, ord.Volume)
                    sheet.write(row, 7, ord.Forwarder)
                    sheet.write(row, 8, ord.Tracking)
                    sheet.write(row, 9, ord.Shipfrom)
                    sheet.write(row, 10, ord.Shipto)
                    sheet.write(row, 11, asset.PartNo)
                    sheet.write(row, 12, asset.ProductDescription)
                    sheet.write(row, 13, asset.SN)
                    sheet.write(row, 14, asset.Qty)
                    sheet.write(row, 15, asset.receiveQty)
                    row = row + 1
        else:
            headers = ['Sent User', 'Receive User', 'Purchase Order', 'Status', 'Packages Qty', 'Gross Weight ',
                       'Volume', 'Forwarder ', 'Tracking NO.', 'Ship From', 'Ship To',
                       'Part Number', 'Product Description', 'Serial NO./Delivery Methods', 'Sent Quantity',
                       'Receive Quantity']
            for i in range(0, len(headers)):
                sheet.write(0, i, headers[i])
            row = 1
            for ord in Order.objects.filter(ordersubmitButton='YES'):
                for asset in Asset.objects.filter(orderID=ord):
                    sheet.write(row, 0, ord.user.username)
                    sheet.write(row, 1, ord.receive_user)
                    sheet.write(row, 2, ord.PO)
                    if (ord.ordersubmitButton == 'YES' and ord.orderreceiveButton == 'YES'):
                        sheet.write(row, 3, 'Approved')
                    else:
                        sheet.write(row, 3, 'Shipped')
                    sheet.write(row, 4, ord.Packages)
                    sheet.write(row, 5, ord.GrossWeight)
                    sheet.write(row, 6, ord.Volume)
                    sheet.write(row, 7, ord.Forwarder)
                    sheet.write(row, 8, ord.Tracking)
                    sheet.write(row, 9, ord.Shipfrom)
                    sheet.write(row, 10, ord.Shipto)
                    sheet.write(row, 11, asset.PartNo)
                    sheet.write(row, 12, asset.ProductDescription)
                    sheet.write(row, 13, asset.SN)
                    sheet.write(row, 14, asset.Qty)
                    sheet.write(row, 15, asset.receiveQty)
                    row = row + 1


    else:
        headers = ['Sent User','Receive User', 'Purchase Order', 'Status','Packages Qty', 'Gross Weight ', 'Volume', 'Forwarder ', 'Tracking NO.', 'Ship From', 'Ship To',
                   'Part Number', 'Product Description', 'Serial NO./Delivery Methods', 'Sent Quantity', 'Receive Quantity']
        for i in range(0, len(headers)):
            sheet.write(0, i, headers[i])
        row = 1
        for ord in Order.objects.filter(user=request.user):
            for asset in Asset.objects.filter(orderID=ord):
                sheet.write(row, 0, ord.user.username)
                sheet.write(row, 1, ord.receive_user)
                sheet.write(row, 2, ord.PO)
                if (ord.ordersubmitButton == 'YES' and ord.orderreceiveButton == 'YES'):
                    sheet.write(row, 3, 'Approved')
                elif (ord.ordersubmitButton == 'YES' and ord.orderreceiveButton == 'NO'):
                    sheet.write(row, 3, 'Shipped')
                else:
                    sheet.write(row, 3, 'Created')
                sheet.write(row, 4, ord.Packages)
                sheet.write(row,5, ord.GrossWeight)
                sheet.write(row, 6, ord.Volume)
                sheet.write(row, 7, ord.Forwarder)
                sheet.write(row, 8, ord.Tracking)
                sheet.write(row, 9, ord.Shipfrom)
                sheet.write(row, 10, ord.Shipto)
                sheet.write(row, 11, asset.PartNo)
                sheet.write(row, 12, asset.ProductDescription)
                sheet.write(row, 13, asset.SN)
                sheet.write(row, 14, asset.Qty)
                sheet.write(row, 15, asset.receiveQty)
                row = row + 1

    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response

def sendpassword_eamil(request):
    if request.is_ajax():
        names = request.GET.get('usernames')
        emaillist = request.GET.get('emails')
        names = json.loads(names)
        emaillist =  json.loads(emaillist)
        for i in range(len(names)):
            import random
            new_password = names[i]+'&'+str(random.randint(10000,99999))
            usr = User.objects.get(username=names[i])
            usr.set_password(new_password)
            usr.save()
            flag=ExtendUser.objects.filter(user=usr)
            if(flag.exists()):
                ExtendUser.objects.get(user=usr).update(clear_password=new_password)
            else:
                extenduser = ExtendUser.objects.create(user=usr,clear_password=new_password)
                extenduser.save()

            # subject = 'Notify:Login Information.'
            # text_context = 'Dear ' + names[i] + ' this is your Login account :' + names[i] + ' and password' + new_password
            # html_msg = '<a href="10.110.23.85/login">10.110.23.85/login</a>'
           # Post_mail(emaillist[i],subject, text_context, html_msg)

        datas = {'dats':names}
        return HttpResponse(json.dumps(datas))

def mailbox(request):
    return render(request,'collec/mailbox.html')

def ajax_getOption(request):
    if request.is_ajax:
        ret = {"country":"china","city":"hangzhou","email":"11111111@qq.com","phone":"12345678901"}
        return HttpResponse(json.dumps(ret))

def add_user(request):
    return  render(request,'Smart_Delivery_AddUser.html')

def form_adduser(request):
    ustatus = request.POST.get('user_status')
    uname = request.POST.get('Username')
    upassword = request.POST.get('Password')
    ucountry = request.POST.get('Country')
    ucity = request.POST.get('City')
    uemail = request.POST.get('Email')
    uphone = request.POST.get('Phone')

    if (ustatus == 'vendor'):
        usr = User.objects.create_user(username=uname, email=uemail, password=upassword)
        ExtendUser.objects.create(user=usr,Country=ucountry,City=ucity,Phone=uphone,Email=uemail,clear_password=upassword,User_Status='vendor')
    else:
        usr = User.objects.create_user(username=uname,email=uemail,password=upassword,is_superuser=1)
        ExtendUser.objects.create(user=usr, Country=ucountry, City=ucity, Phone=uphone, Email=uemail,clear_password=upassword, User_Status='receiver')

    # email_name = []
    # user_email = uemail
    # email_name.append(user_email)
    # subject = 'Notify:Login Information.'
    # text_context = 'Dear' + uname + 'this is your Login account :' + uname + ' and password' + upassword
    # html_msg = '<a href="10.110.23.85/login">10.110.23.85/login</a>'
    # Post_mail(email_name, subject, text_context, html_msg)

    return  HttpResponseRedirect('/collec/add_user/')


def import_user(request):
    return render(request,'import_user_excelFile.html')

def add_notice(request):
    notices=Notice.objects.all()

    return  render(request,'addnotice.html')

def download_user_excle(request):
        # do something
        filename = 'static/admin/Excel/User_view_Template.xls'
        from django.http import StreamingHttpResponse
        response = StreamingHttpResponse(readFile(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=User_view_Template.xls'
        return response

def import_user_excle(request):
    if 'cancel' in request.POST:
        return HttpResponseRedirect('/collec/import_user/')

    wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
    ws = wb.sheets()[0]
    nrow = ws.nrows
    headers = ['Username', 'Password', 'Email', 'Country', 'City', 'Phone', 'User_Status']

    lists = []
    for row in range(1, nrow):
        r = {}
        for col in range(1, len(headers) + 1):
            key = headers[col - 1]
            r[key] = ws.cell(row, col - 1).value

        lists.append(r)

    usname = []
    users = User.objects.all()
    for usr in users:
        usname.append(usr.username)

    pcount = 0

    for cell in lists:
        # for header in headers:
        uname = str(cell['Username'])
        upassword = str(cell['Password'])
        uemail = str(cell['Email'])
        ucountry = str(cell['Country'])
        ucity = str(cell['City'])
        uphone = str(cell['Phone'])
        ustatus = str(cell['User_Status'])
        if (uname != '' and uname not in usname):
            if (ustatus == 'vendor'):
                usr = User.objects.create_user(username=uname, email=uemail, password=upassword)
                ExtendUser.objects.create(user=usr, Country=ucountry, City=ucity, Phone=uphone, Email=uemail,
                                          clear_password=upassword, User_Status='vendor')
            else:
                usr = User.objects.create_user(username=uname, email=uemail, password=upassword, is_superuser=1)
                ExtendUser.objects.create(user=usr, Country=ucountry, City=ucity, Phone=uphone, Email=uemail,
                                          clear_password=upassword, User_Status='receiver')
            pcount +=1
    if pcount:
        information = 'total' + str(pcount) + 'items product information import sucessful!'
    else:
        information = '0 item product information import! '

    return HttpResponseRedirect('/collec/import_user/', {'information': information})


def admin_password_change(request):
    return render(request,'admin_user_changepd.html')

def deleteuser(request,uid):
    if request.user.is_authenticated and request.user.is_superuser:
       User.objects.filter(id=uid).delete()
       return HttpResponseRedirect('/admin/collec/extenduser/')
    else:
        return HttpResponseRedirect('/login/')

def form_addnotice(request):
    notice = request.POST.get('notice')
    Notice.objects.create(content=notice)
    return HttpResponseRedirect('/collec/add_notice/')



