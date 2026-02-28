from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('report/', views.report_item, name='report_item'),
    path('claim/<int:item_id>/', views.submit_claim, name='submit_claim'),
    path('item/edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('item/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('security-report/', views.security_report, name='security_report'),
    path('my-claims/', views.my_claims, name='my_claims'),
    path('manage-claims/', views.manage_claims, name='manage_claims'),
    path('approve-claim/<int:claim_id>/', views.approve_claim, name='approve_claim'),
    path('reject-claim/<int:claim_id>/', views.reject_claim, name='reject_claim'),
]