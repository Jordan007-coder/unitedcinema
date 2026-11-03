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
    path('packages/', dashboard_views.dashboard_package_list, name='package_list'),
    path('packages/categories/', dashboard_views.dashboard_package_category_list, name='package_category_list'),
    path('packages/categories/add/', dashboard_views.dashboard_package_category_create, name='package_category_add'),
    path('packages/categories/<int:category_id>/edit/', dashboard_views.dashboard_package_category_edit, name='package_category_edit'),
    path('packages/categories/<int:category_id>/delete/', dashboard_views.dashboard_package_category_delete, name='package_category_delete'),
    path('packages/categories/reorder/', dashboard_views.dashboard_package_category_reorder, name='package_category_reorder'),
    path('packages/weekend/', dashboard_views.dashboard_weekend_update, name='weekend_update'),
    path('packages/reorder/', dashboard_views.dashboard_package_reorder, name='package_reorder'),
    path('packages/add/', dashboard_views.dashboard_package_create, name='package_add'),
    path('packages/<int:package_id>/edit/', dashboard_views.dashboard_package_edit, name='package_edit'),
    path('packages/<int:package_id>/delete/', dashboard_views.dashboard_package_delete, name='package_delete'),
    path('users/', dashboard_views.dashboard_user_list, name='user_list'),
    path('users/create/', dashboard_views.dashboard_user_create, name='user_create'),
    path('users/<int:user_id>/delete/', dashboard_views.dashboard_user_delete, name='user_delete'),
]
