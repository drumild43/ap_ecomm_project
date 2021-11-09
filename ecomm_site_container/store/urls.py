from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.home, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin')
]