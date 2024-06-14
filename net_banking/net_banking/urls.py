"""
URL configuration for net_banking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from .import views



urlpatterns = [
    path('admin/', admin.site.urls),

    path('master/',views.master,name="master"),

    path('',views.index,name="index"),

    path('contact_us',views.contact_us,name="contact_us"),

    path('login',views.login,name="login"),

    path('signup/', views.new_account_holder, name='signup'),

    path('blog/', views.blog, name="blog"),

    path('user_account/',views.user_account,name="user_account"),

    path('logout/', views.logout, name='logout'),

    path('activate/',views.activate,name='activate'),

    path('update_profile/',views.update_profile,name='update_profile'),

    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),

    path('api/profit-data/', views.get_profit_data, name='get_profit_data'),

path('chart/', views.chart_view, name='chart_view'),
]

