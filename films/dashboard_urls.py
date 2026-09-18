from django.urls import path
from . import dashboard_views
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_views.dashboard_home, name='home'),
    path('movies/', dashboard_views.dashboard_movie_list, name='movie_list'),
    path('movies/add/', views.film_create, name='movie_add'),
    path('movies/<slug:slug>/edit/', dashboard_views.dashboard_movie_edit, name='movie_edit'),
    path('movies/<slug:slug>/delete/', dashboard_views.dashboard_movie_delete, name='movie_delete'),
    path('schedule/', views.schedule_update, name='schedule_update'),
    path('users/', dashboard_views.dashboard_user_list, name='user_list'),
    path('users/create/', dashboard_views.dashboard_user_create, name='user_create'),
    path('users/<int:user_id>/delete/', dashboard_views.dashboard_user_delete, name='user_delete'),
]
