"""New URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
     path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("user/",views.UserView.as_view()),
    path("product/action/<int:Pid>",views.ProductView.as_view()),
    path("product/action/",views.ProductView.as_view()),
    path("cart/",views.CartView.as_view()),
    path("product/",views.ProductAllView.as_view(),name="all"),
    path("order/",views.OrderView.as_view())
    # path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    # path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
