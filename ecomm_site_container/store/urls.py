from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.home, name='anon_homepage'),
    path('<int:user_id>/', views.home, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/<int:user_id>/', views.logout, name='logout')
]