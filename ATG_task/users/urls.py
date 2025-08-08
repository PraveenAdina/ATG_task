from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),

    path('blog/create/', views.create_blog, name='create_blog'),
    path('blog/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('blog/edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('blog/view/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/view/<int:blog_id>/', views.blog_detail, name='blog_detail'),

]
