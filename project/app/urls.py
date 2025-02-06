from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('adminregisterr/', views.adminregisterr, name='adminregisterr'),
    path('userregisterr/',views.userregisterr, name='userregisterr'),
    path('userhome/', views.userhome, name='userhome'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('addexpense/', views.addexpense, name='addexpense'),
    path('viewexpense/', views.viewexpense, name='viewexpense'),
    path('addgroup/', views.addgroup, name='addgroup'),
    path('viewgroup/', views.viewgroup, name='viewgroup'),
    path('addgroupmember/', views.addgroupmember, name='addgroupmember'),
    path('viewgroupmember/', views.viewgroupmember, name='viewgroupmember'),
    
    path('viewexpenses/', views.viewexpenses, name='viewexpenses'),
    path('viewusers/', views.viewusers, name='viewusers'),
    


]