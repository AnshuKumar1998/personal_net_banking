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
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),

    path('master/',views.master,name="master"),


    #------------ Pages URL ------------------------------------------------------------

    path('',views.index,name="index"),

    path('contact_us', views.contact_us, name="contact_us"),

    path('login', views.login, name="login"),

    path('signup/', views.new_account_holder, name='signup'),

    path('blog/', views.blog, name="blog"),

    path('payment/', views.payment_page, name='payment_page'),

    path('process_payment/', views.process_payment, name='process_payment'),

    path('get-transactions/', views.get_transactions, name='get_transactions'),

    path('loan_preview_form/', views.loan_preview_form, name='loan_preview_form'),

    path('delete_loan/<int:loan_id>/', views.delete_loan, name='delete_loan'),



    #------------ End Pages URL ------------------------------------------------------------

    #------------ User Account URL ------------------------------------------------------------

    path('user_account/', views.user_account, name="user_account"),

    path('logout/', views.logout, name='logout'),

    path('activate/', views.activate, name='activate'),

    path('update_profile/', views.update_profile, name='update_profile'),

    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),

    path('api/profit-data/', views.get_profit_data, name='get_profit_data'),

    path('chart/', views.chart_view, name='chart_view'),

    path('loan_form/', views.loan_form, name="loan_form"),

    path('fix_deposit_list/', views.fix_deposit_list, name="fix_deposit_list"),

    path('fix-deposite-details/<str:fix_deposite_id>/', views.fix_deposite_details, name='fix_deposite_details'),

    path('service/',views.service,name="service"),

    path('fix_deposite_process_payment/', views.fix_deposite_process_payment, name='fix_deposite_process_payment'),

    path('post_list/', views.post_list, name='post_list'),

    path('like/<int:post_id>/', views.like_post, name='like_post'),

    path('user_setting/', views.user_setting, name='user_setting'),

    path('activity/', views.user_activity, name='activity'),  # New URL pattern

    path('hide_message/', views.hide_message, name='hide_message'),

    path('delete_account/', views.delete_account, name='delete_account'),

    path('fix-deposite-payment/', views.fix_deposite_payment_details, name='fix-deposite-payment'),

    path('fixDeposite-paymentProcess/', views.fix_deposite_payment_process, name='fixDeposite-paymentProcess'),

    path('complaint/', views.complaint_form, name='complaint_form'),

    path('delete_complaint/<int:id>/', views.delete_complaint, name='delete_complaint'),

    path('transfer_money/', views.transfer_money, name='transfer_money'),

    path('fetch-user-data/', views.fetch_user_data, name='fetch-user-data'),

    #------------ End User Account URL --------------------------------------------------------
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

