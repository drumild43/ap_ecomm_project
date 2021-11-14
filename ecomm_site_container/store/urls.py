from django.urls import path, include
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.home, name='anon_homepage'),
    path('<int:user_id>/', views.home, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('<int:user_id>/logout/', views.logout, name='logout'),
    path('products/', views.products, name='products'),
    path('<int:user_id>/account/', views.account, name='account'),
    path('<int:user_id>/address/', views.address, name='address'),
    path('<int:user_id>/personal-details/', views.pers_details, name='pers-details'),
    path('product-details/<int:id>', views.product_details, name='product-details'),
    path('accounts/', include('allauth.urls'))
]