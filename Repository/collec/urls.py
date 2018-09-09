# -*- coding:utf-8 -*-

from django.conf.urls import url
from collec import views
app_name = 'collec'
urlpatterns = [
    url(r'^addOrder/', views.addOrder, name='addOrder'),
    url(r'^receive/', views.receive, name='receive'),
    url(r'^receiveOrder/(.+)/$', views.receiveOrder, name='receiveOrder'),
    url(r'^sendAssetAmount/$', views.sendAssetAmount, name='sendAssetAmount'),
    url(r'^cancleReceiveAmount/$', views.cancleReceiveAmount, name='cancleReceiveAmount'),
    url(r'^submit/', views.submit, name='submit'),
    url(r'^detail/$', views.detail, name="detail"),
    url(r'^mylogout/$',views.my_logout, name="mylogout"),
    url(r'^changepd/$',views.changepd, name="changepd"),
    url(r'^index/$', views.index, name="index"),
    url(r'^vendormanage/$', views.vendormanage, name="vendormanage"),
    url(r'^deleteUser/(?P<id>[0-9]{1,6})/$', views.deleteUser, name='deleteUser'),
    url(r'^addUser/$', views.addUser, name="addUser"),
    url(r'^deleteuser/(.+)/$', views.deleteuser, name="deleteuser"),
    url(r'^orderajax/$', views.orajax,name='ordajax'),
    url(r'^assetajax/$', views.asetajax,name='assetajax'),
    url(r'^ajaxreceiveorder/$', views.ajaxrecveorder,name='ajaxreceiveorder'),
    url(r'^ajaxreceived/', views.ajaxreceived, name='ajaxreceived'),
    url(r'^receivedassetajax/', views.receivedassetajax, name='receivedassetajax'),
    url(r'^ajaxsubmited/$', views.ajaxsubmited, name='ajaxsubmited'),
    url(r'^submitedassetajax/$', views.submitedassetajax, name='submitedassetajax'),
    url(r'^ajax_saveReceive/$', views.ajax_saveReceive, name='ajax_saveReceive'),
    url(r'^ajax_vendor_comment_save/$', views.ajax_vendorcomment_save, name='ajax_vendor_comment_save'),
    url(r'^searchorder/$', views.searchorder, name='searchorder'),
    url(r'^ajax_searchOrder/$', views.ajax_searchOrder, name='ajax_searchOrder'),
    url(r'^ajax_searchasset/$', views.ajax_searchasset, name='ajax_searchasset'),
    url(r'^ajax_vendor_send/$', views.ajax_vendor_send, name='ajax_vendor_send'),
    url(r'^createOrder/$', views.createOrder, name='createOrder'),
    url(r'^updateOrder/(.+)/$', views.updateOrder, name='updateOrder'),
    url(r'^upload_order/$', views.upload_order, name='upload_order'),
    url(r'^import_excelFile/$', views.import_excelFile, name='import_excelFile'),
    url(r'^download_excle/$', views.download_excle, name='download_excle'),
    url(r'^showInfo/$',views.showInfo,name='showInfo'),
    url(r'^change_personal_Info/$',views.change_personalInfo,name='change_personalInfo'),
    url(r'^export/$', views.export, name='export'),
    url(r'^sendpassword_eamil/$', views.sendpassword_eamil, name='sendpassword_eamil'),
    url(r'^orderStatus/$',views.orderStatus,name="orderStatus"),
    url(r'^ajax_getOption/$', views.ajax_getOption, name="ajax_getOption"),
    url(r'^add_user/$', views.add_user, name="add_user"),
    url(r'^form_adduser/$', views.form_adduser, name="form_adduser"),
    url(r'^import_user/$', views.import_user, name="import_user"),
    url(r'^import_user_excle/$', views.import_user_excle, name="import_user_excle"),
    url(r'^add_notice/$', views.add_notice, name="add_notice"),
    url(r'^form_addnotice/$', views.form_addnotice, name="form_addnotice"),
    url(r'^download_user_excle/$', views.download_user_excle, name="download_user_excle"),
    url(r'^admin_password_change/$', views.admin_password_change, name="admin_password_change"),
    url(r'^mailbox/$', views.mailbox, name='mailbox'),



]