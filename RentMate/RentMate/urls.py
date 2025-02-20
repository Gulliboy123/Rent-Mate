"""
URL configuration for RentMate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views #password reset



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name="logout"),
    path('aboutus/', views.AboutPage, name='aboutus'),
    path('contactus/', views.ContactPage, name='contactus'),
    path('property/', views.PropertyPage, name='property'),
    path('my-account/', views.my_account, name='my_account'),
    path('saved/', views.saved, name='saved'),
    path('bookings/', views.bookings, name='bookings'),
    path('forgotpassword/', views.ForgotPassword, name='forgotpassword'),
    path('newpassword/<str:user>/', views.NewPasswordPage, name='newpassword'),
    path('message/', views.Message, name='message'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)