from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_users, name='login'),
    path('logout/', views.logout_users, name='logout'),
    path('register/', views.register_users, name='register'),
    path('report_missing_person/', views.report_missing_person, name='report_missing_person'),
    path('view_missing_persons', views.view_missing_persons, name='view_missing_persons'),
    path('missing_person/<int:id>/', views.missing_person_detail, name='missing_person_detail'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('edit/<int:report_id>/', views.edit_report, name='edit_report'),
    path('delete/<int:report_id>/', views.delete_report, name='delete_report'),
    path('login-required/', views.login_required_message, name='login_required_page'),
    path('search/', views.search, name='search'),
] 
