from django.contrib import admin
from django.urls import path, include

from gasmapApp import views

urlpatterns = [
    path('', views.home, name='home'),

    path('gasmapapp/', include("gasmapApp.urls")),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]
