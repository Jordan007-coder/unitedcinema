from django.urls import path,re_path,include
from . import views

app_name = 'accounts'


urlpatterns = [
	re_path(r'^signup/$',views.signup_view,name="signup"),
	#path('/accounts',include('django.contrib.auth.urls')),
	path('logout/',views.logout_view,name="logout"),
	path('login/',views.login_view,name="login"),
]