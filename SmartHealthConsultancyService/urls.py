from django.contrib import admin
from django.urls import path,include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login),
    path('dashboard/',views.dashboard),
    path('profile/',views.profile),
    path('logout/',views.logout),
    path('register/',views.register),
]