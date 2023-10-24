from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('detail/<int:p_id>',views.detail,name='detail'),
    path('cart/',views.cart,name='cart'),
    path('update_item/', views.updateItem,name='update_item'),
    path('search_item/', views.search_item,name='search_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.pay,name='payment'),

    path('login/',views.login_user,name='login'),
    path('register/',views.register_user,name='register'),
    path('logout/',views.logout_user,name='logout'),
]