from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Import Django's built-in logout view

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add this line for logout
    path('customer/new/', views.customer_create, name='customer_create'),
    path('customer/<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('search/', views.search_customers, name='search_customers'),
]
