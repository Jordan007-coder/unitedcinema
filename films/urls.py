
from django.urls import path,re_path

from . import views

app_name = 'films'
urlpatterns = [
    path('home/',views.filmlist,name="list"),
    path('create/',views.film_create,name='create'),
    re_path(r'^(?P<slug>[\w-]+)/$',views.film_details,name="details"),
]
