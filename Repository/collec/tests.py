# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Repository.settings")
django.setup()


import unittest

from django.test import TestCase, Client

from Repository import rootview
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

# Create your tests here.
'''
 通常1、html里的东西不在这里测试
      （1）、html里面的html代码是写死的；
      （2）、嵌套在html中的django模板语言也不能测，即使有部分逻辑。
      但写测试用例的时候至少要调用一个类或者方法。模板语言没有出参也没有入参
      
    2、models模型可以测，属于数据库层
    3、views，视图层可以测试，有入参、有方法

'''

from django.test import TestCase, override_settings

@override_settings(LOGIN_URL='')
class LoginTestCase(TestCase):

    def test_login(self):
        response = self.client.get('/login/')
        self.assertRedirects(response, '/login/')