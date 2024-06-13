"""hospitalms URL Configuration

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
from django.urls import path, include
from common import views

''' 主路由表 '''
urlpatterns = [
    path('admin/', admin.site.urls),  # admin路由，这里是django自带的
    path('user/', include('common.urls')),  # 用户模块，包括登录、注册、找回密码等，common是app的名字
    path('', views.home, name='home'),  # 根路径路由
]

'''
    将主路由表划分为多个子表 依据第一项将子表划分到各个app中
'''
