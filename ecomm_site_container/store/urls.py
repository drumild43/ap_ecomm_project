from django.urls import path
from . import views

app_name = 'store'

# home + auth
urlpatterns = [
    path('', views.home, name='anon_homepage'),
    path('<int:user_id>/', views.home, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('<int:user_id>/logout/', views.logout, name='logout')   
]

# profile
urlpatterns += [
    path('<int:user_id>/account/', views.account, name='account'),
    path('<int:user_id>/can-order/<int:order_id>/', views.cancel_order, name='cancel-order'),
    path('<int:user_id>/address/', views.address, name='address'),
    path('<int:user_id>/personal-details/', views.pers_details, name='pers-details')
]

# product-related
urlpatterns += [
    path('products/', views.products, name='anon_products'),
    path('<int:user_id>/products/', views.products, name='products'),
    path('products/<int:product_id>/', views.product_details, name='anon_product-details'),
    path('<int:user_id>/products/<int:product_id>/', views.product_details, name='product-details'),
    path('products/<int:product_id>/signup/', views.signup, name='product-signup-redirect'),
    path('products/<int:product_id>/signin/', views.signin, name='product-signin-redirect'),
    path('<int:user_id>/submit-review/<int:product_id>/', views.review, name='review')
]

# cart, wishlist, checkout
urlpatterns += [
    path('<int:user_id>/cart/', views.cart, name='cart'),
    path('<int:user_id>/cart/<int:product_id>/', views.cart, name='add-to-cart'),
    path('<int:user_id>/cartitems/<int:cartitem_id>/', views.cart, name='update-cartitem'),
    path('<int:user_id>/wishlist/', views.wishlist, name='wishlist'),
    path('<int:user_id>/wishlist/<int:product_id>/', views.wishlist, name='update-wishlist'),
    path('<int:user_id>/checkout/', views.checkout, name='checkout'),
    path('<int:user_id>/pay-suc/', views.pay_suc, name='pay-suc')
]