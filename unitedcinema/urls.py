
from django.contrib import admin
from django.urls import path,include,re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'films/',include('films.urls')),
    #path('/accounts',include('django.contrib.auth.urls')),
    re_path(r'^accounts/',include('accounts.urls')),
    path('about/',views.about),
    path('home/',views.homepage),
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
