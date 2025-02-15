"""motoAlSat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from motoVitrin import views


 




urlpatterns = [
    path('admin/',admin.site.urls,name='admin'),
    path('login/',views.custom_login,name='login'),
    path('home/',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('logout/', views.logout_user,name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path("sales-report/", views.sales_report, name="sales_report"),
    path("siparis_ekle/",views.siparis_ekle, name="siparis_ekle"),
    path('custom-login/',views.custom_login, name='customlogin'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('marketer-dashboard/', views.marketer_dashboard, name='marketer_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    
]

