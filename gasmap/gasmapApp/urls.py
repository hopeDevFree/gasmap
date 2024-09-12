from django.urls import path
from . import views

app_name = "gasmapApp"

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path('create/', views.item_create, name='item_create'),
    path('<int:pk>/update/', views.item_update, name='item_update'),
    path('<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('search_address/', views.search_address, name='search_address'),
    path('search_station/', views.search_station, name='search_station'),
    path('add_station/', views.add_station, name = 'add_station')
]
