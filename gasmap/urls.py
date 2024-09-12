from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('gasmapapp/', include("gasmapApp.urls")),
    path('admin/', admin.site.urls)
]
