# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib import admin
from .models import ExtendUser
from django.forms import ModelForm
from django.forms import TextInput, Textarea
from django.db import models
from django.core.mail import send_mail
from  django.contrib.auth.models import User
from django.shortcuts import redirect,get_object_or_404
class ExtendUserAdmin(admin.ModelAdmin):
    def object_link(self, obj):
        count = obj.user_id
        bid = 'bid' + '-' + str(count)
        turl = '/collec/deleteuser/' + str(count) + '/'
        return u'<a href="javascript:void(0);" id={id} onclick="deleteConfirm(this.id)">delete</a>'.format(id=bid)


    object_link.short_description = 'Operation'
    object_link.allow_tags = True

    def changelist_view(self, request, extra_context=None):

        self.list_display = ('user','User_Status','Country','City','Email','Phone','clear_password','object_link')


        return super(ExtendUserAdmin, self).changelist_view(request, extra_context=None)

    change_list_template = "my_change_list.html"
    change_form_template = "my_change_form.html"
    list_display = ('user','User_Status','Country','City','Email','Phone','clear_password','object_link')
    search_fields = ('Country', 'City','User_Status',)
    list_display_links = ('user',)
    list_per_page = 15


admin.site.site_header = "Smart Delivery Management"
admin.site.site_title = "Smart Delivery Management"
admin.site.index_template = "login.html"

admin.site.register(ExtendUser,ExtendUserAdmin)