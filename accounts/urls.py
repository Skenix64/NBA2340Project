from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('reset_request/', views.reset_request_view, name='reset_request'),
    path('reset/<str:token>/', views.reset_password_view, name='reset_password'),
]
