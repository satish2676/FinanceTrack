from django.urls import path
from . import views

urlpatterns = [
    path('admin_register/', views.admin_register, name='admin_register'), 
    path('', views.admin_login, name='login'),
    path('index/', views.index, name='index'),
    path('mark_paid/<int:member_id>/<str:disbursement_date>/', views.mark_paid, name='mark_paid'),
    path('register/', views.register, name="register"),
    path('view_members/', views.view_members, name='view_members'),
    path('daily_collection/', views.daily_collection, name='daily_collection'),
    path('paid_status/', views.paid_status, name='paid_status'),
    path('export_daily_collection/', views.export_daily_collection, name='export_daily_collection'),
    path('member_details/<str:loan_id>/', views.member_details, name='member_details'),
    path('member_details/', views.member_details, name='member_details'),
    path('all_members/', views.all_members, name='all_members'),
    path('export_all_members_excel/', views.export_all_members_excel, name='export_all_members_excel'),

    ]

    