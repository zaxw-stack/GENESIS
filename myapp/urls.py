from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('details/', views.details, name='details'),
    path('blog/', views.blog, name='blog'),
    path('home/', views.home, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('services/', views.services, name='services'),
    path('starter/', views.starter, name='starter'),
    path('show/', views.show, name='show'),
    path('', views.home, name='home'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('payment/', views.payment, name='payment'),
    path('callback/', views.callback, name='callback'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin/', admin.site.urls),
]