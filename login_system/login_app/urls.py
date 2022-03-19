from unicodedata import name
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name = 'index'),
    path('signup', views.signup, name = 'signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('unsign', views.delete, name= 'unsign'),
    path('accounts/profile/', views.index, name= 'index_google'),
]

urlpatterns += staticfiles_urlpatterns()