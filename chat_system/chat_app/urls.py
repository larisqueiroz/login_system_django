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
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages')
]

urlpatterns += staticfiles_urlpatterns()