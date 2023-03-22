"""memberscatalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from atexit import register
#from enum import member
from os import path
import statistics
from turtle import home
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from membersapp import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from membersapp.views import  add_card, delete_member, index, members, update_member
from membersapp.views import (
    login_view,
    register_view,
    index,
    show_members,
    add_member,
    logout_view,
    check_members
)
from memberscatalog import settings



    
urlpatterns = [
    path('', index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('members/', check_members, name='check_members'),
    path('members/add/', add_member, name='add_member'),
    #path('game/', game, name='game'),
    path('members/', members, name='members'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^home/$', index, name='home'),
    #url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register_view, name='register'),
    path('members/show/', show_members, name='show_members'),
    # url(r'^members/add/$', add_member, name='add_member'),
    path('members/update/<int:pk>/', update_member, name='update_member'),
    path('members/<int:pk>/delete/', delete_member, name='delete_member'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^admin/', admin.site.urls),
    path('add_card/<int:member_id>/', add_card, name='add_card'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)