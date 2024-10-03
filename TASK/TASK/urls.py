"""
URL configuration for TASK project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from TASKapp.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path('',index),

    #user
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/', register, name='register'),

    #task
    path('task/',task, name='task'),
    path('task/add/', add_task, name='add_task'),  # 新增任務的路由
    path('task/edit/<slug:id>/', edit_task, name='edit_task'),
    path('task/delete/<slug:id>/',delete_task),
    path('task/share/<slug:id>/',share_task),
    path('task/show_share/',show_share),
    path('task/show_log/<slug:id>',show_log),
    path('task/comment/<slug:id>',comment_task),
]
