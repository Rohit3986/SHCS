from django.contrib import admin
from django.urls import path,include
from myapp import views
#http://127.0.0.1:8000/
#http://127.0.0.1:8000/dashboard/
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login),
    path('dashboard/',views.dashboard),
    path('profile/',views.profile),
    path('logout/',views.logout),
    path('register/',views.register),
    path('select_doctors/',views.doctor)
]
