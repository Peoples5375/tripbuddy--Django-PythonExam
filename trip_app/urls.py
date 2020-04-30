from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('create_trip', views.create_trip),
    path('remove_trip/<id>', views.remove_trip),
    path('edit_trip/<id>', views.edit_trip),
    path('submit_edit/<id>', views.submit_edit),
    path('trips/new', views.new_trip),
    path('trips/<id>', views.see_trip),
    path('logout', views.logout),
]   