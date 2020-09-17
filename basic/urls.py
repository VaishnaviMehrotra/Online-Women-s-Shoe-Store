"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:s
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from basic.views import register, index, about, stock, contact, login, casualShoes, boots, sportsShoesANDFloaters, \
    logout_view, heels, cart, get_cart_data, purchase, change_quan, removeCartItem

urlpatterns = (
    path('registration/', register),
    path('', index),
    path('index/', index),

    path('about/', about),
    path('stock/', stock),
    path('contact/', contact),
    path('login/', login),
    path('logout/', logout_view),
    path('cart/', cart, name='cart'),
    path('heels/', heels),
    path('casualShoes/', casualShoes),
    path('boots/', boots),
    path('sportsShoes&Floaters/', sportsShoesANDFloaters),
    path('purchase/', purchase),
    path('get_cart_data/', get_cart_data, name='get_cart_data'),
    path('change_quan/', change_quan, name='change_quan'),
    path('remove_cart_item/', removeCartItem, name='remove_cart_item'),


)
