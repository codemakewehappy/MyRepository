# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collec.forms import LoginForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, response
from django.contrib.auth import authenticate, login
import random

from collec.models import ExtendUser


def mylogin(request):
        er = []
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():

                data = form.cleaned_data
                username = data['username']
                password = data['password']
                # username = request.POST.get('username')
                # password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None and not (user.is_staff == 1):
                    login(request, user)
                    # Redirect to a success page.
                    return HttpResponseRedirect('/collec/index/')
                elif user is not None and  user.is_staff == 1:
                    login(request, user)
                    # Redirect to a success page.
                    return HttpResponseRedirect('/admin/collec/extenduser/')
                else:
                    # Return an 'invalid login' error message.
                    er.append('Please input the correct username and password !')

            else:
                er.append('Please input vaild username and password !')
        else:
            er = []

        return render(request, 'login.html',{'er':er})

def forget_password(request):
            er = []
            if request.method == 'POST':
                tuname = request.POST.get("username")
                tuemail = request.POST.get("email")

                from django.contrib.auth.models import User
                flag = User.objects.filter(username=tuname)
                if (flag.exists()):
                    email_flag = User.objects.filter(username=tuname,email=tuemail)
                    if (email_flag.exists()):
                        # new_password = tuname + '&' + str(random.randint(10000, 99999))
                        # usr = User.objects.get(username=tuname)
                        # usr.set_password(new_password)
                        # usr.save()
                        # ExtendUser.objects.get(user=usr).update(clear_password=new_password)
                        # email_name = []
                        # user_email = tuemail
                        # email_name.append(user_email)
                        # subject = 'Notify:Login Information.'
                        # text_context = 'Dear' + tuname + 'this is your Login account :' + tuname + ' and your new password'+tupassword
                        # html_msg = '<a href="10.110.23.85/login">10.110.23.85/login</a>'
                        # Post_mail(email_name, subject, text_context, html_msg)
                        return HttpResponseRedirect('/login/')
                    else:
                        er.append('Please input correct email !')

                else:
                    er.append('Please input correct username !')
            else:
                er = []

            return render(request, 'forgetpassword.html', {'er': er})

