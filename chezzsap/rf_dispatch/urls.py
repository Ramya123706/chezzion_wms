from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('five/', views.fifth, name='fifth'),
    path('six/', views.sixth, name='sixth'),
    path('start/', views.first, name='first'),
    path('secondary/', views.second, name='second'),
    path('hu1/', views.hu1, name='hu1'),
    path('hu12/', views.hu12, name='hu12'),
    path('hu123/', views.hu123, name='hu123'),
    path('new1/', views.new1, name='new1'),
    path('new2/', views.new2, name='new2'),
    path('new3/', views.new3, name='new3'),
    path('new4/', views.new4, name='new4'),
    path('one/', views.one, name='one'),
    path('two/', views.two, name='two'),
    path('three/', views.three, name='three'),
    path('four/', views.four, name='four'),
    path('five1/', views.five1, name='five1'),
    path('six1/', views.six1, name='six1'),
    path('seven1/', views.seven1, name='seven1'),
    path('eight1/', views.eight1, name='eight1'),
    path('nine1/', views.nine1, name='nine1'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

