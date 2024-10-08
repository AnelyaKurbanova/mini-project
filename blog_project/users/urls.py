from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('profile/<int:pk>/', views.profile, name='profile'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),
   
    path('profile/<int:pk>/follow/', views.follow_user, name='follow_user'),

    path('profile/<int:pk>/unfollow/', views.unfollow_user, name='unfollow_user'),
]
