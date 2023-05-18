from django.urls import path
from .views import *


urlpatterns = [
    path("/auth/login", login, name="login"),
    path("/auth/register", register, name="register"),
    path("/auth/verify", verifyCode, name="verify"),
    path("/auth/reset-password", reset_password, name="reset-password"),
    path("/auth/reset-password-with-email", reset_password_with_email, name="reset-password-with-email"),
    path("/profile", profile, name="profile"),
]
