from django.urls import path
from login.views import LoginJWTView
from rest_framework_simplejwt import views

urlpatterns = [
    path("auth/", LoginJWTView.as_view(), name="auth"),
    path("auth/refresh/", views.TokenRefreshView.as_view(), name="auth_refresh"),
]
