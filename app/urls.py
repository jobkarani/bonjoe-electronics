from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('update_profile/<int:id>', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    path('accounts/profile/', views.profile, name='profile'),
    path('shop/', views.shop, name='shop'),
    path('shop/category/<slug:category_slug>/', views.shop, name='products_by_category'),
    path('shop/category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('aboutus/', views.About, name='About'),
    path('shop/search/', views.search, name='search'),
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('userPayment/', views.userPayment, name='userPayment'),
]
