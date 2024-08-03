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
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views


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

    path('verify_old_password/', views.verify_old_password, name='verify_old_password'),

    path('change_password/', views.change_password, name='change_password'),

    path('password_reset/',auth_views.PasswordResetView.as_view(
               template_name='password_reset.html',
               email_template_name='password_reset_email.html',
               success_url=reverse_lazy('password_reset_done')
           ),
           name='password_reset'),

      path('password_reset/done/',
           auth_views.PasswordResetDoneView.as_view(
               template_name='password_reset_done.html'
           ),
           name='password_reset_done'),

      path('reset/<uidb64>/<token>/',
           auth_views.PasswordResetConfirmView.as_view(
               template_name='password_reset_confirm.html',
               success_url=reverse_lazy('password_reset_complete')
           ),
           name='password_reset_confirm'),

      path('reset/done/',
           auth_views.PasswordResetCompleteView.as_view(
               template_name='password_reset_complete.html'
           ),
           name='password_reset_complete'),

    path('update_amount/', views.update_amount, name='update_amount'),
    path('get_current_amount/', views.get_current_amount, name='get_current_amount'),
    path('fetch-transaction-months/', views.fetch_transaction_months, name='fetch_transaction_months'),
    path('delete-transactions/', views.delete_transactions, name='delete_transactions'),
    path('account_list/', views.customer_account_list, name='account_list'),
    path('delete_customer/<int:account_no>/', views.delete_customer, name='delete_customer'),
    path('verify_account/', views.verify_account, name='verify_account'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('api/get_customer_accounts/', views.get_customer_accounts, name='get_customer_accounts'),
    path('transaction_statement/', views.user_transaction_statement, name='transaction_statement'),
    path('delete-transaction/<int:id>/', views.delete_transaction, name='delete_transaction'),
    path('send_mail/', views.send_mail_view, name='send_mail'),
    path('get_account_email/', views.get_account_email, name='get_account_email'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('atm_card_view/', views.atm_card_view, name='atm_card_view'),
    path('action_center/', views.action_center, name='action_center'),
    path('action/<int:id>/', views.action_detail, name='action_detail'),
    path('update_service/', views.update_service, name='update_service'),
    path('make_transaction/', views.make_otp_transaction, name='make_transaction'),
    path('api/atm_transaction/', views.ATMTransactionView, name='atm_transaction'),
    path('delete_transactionByOtp/<str:transaction_id>/', views.delete_transactionByOtp, name='delete_transactionByOtp'),
    path('end_session/<str:transaction_id>/', views.transactionotp_end_session, name='transactionotp_end_session'),



    #------------ End User Account URL --------------------------------------------------------
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)


