from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage),
    path('verify_registration', views.verify_registration),
    path('verify_login', views.verify_login),
    path('success', views.login_successful),
    path('logout', views.logout),
]