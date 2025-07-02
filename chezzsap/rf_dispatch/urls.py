from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path
from .views import yard_checkin_view, truck_inspection_view
from .views import update_truck_status

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('outbound1/', views.outbound1, name='outbound1'),
    path('outbound2/', views.outbound2, name='outbound2'),
    path('outbound3/', views.outbound3, name='outbound3'),
    path('outbound4/', views.outbound4, name='outbound4'),
    path('outbound5/', views.outbound5, name='outbound5'),
    path('outbound6/', views.outbound6, name='outbound6'),
    path('outbound7/', views.outbound7, name='outbound7'),
    path('six/', views.sixth, name='sixth'),
    path('start/', views.first, name='first'),
   
    path('hu1/', views.hu1, name='hu1'),
    path('hu12/', views.hu12, name='hu12'),
    path('hu123/', views.hu123, name='hu123'),
    path('new1/', views.new1, name='new1'),
    path('new2/', views.new2, name='new2'),
    path('new3/', views.new3, name='new3'),
    path('new4/', views.new4, name='new4'),
    path('one/', views.yard_checkin_view, name='one'),
     
    path('three/', views.three, name='three'),
    path('four/', views.four, name='four'),
    path('five1/', views.five1, name='five1'),
    path('six1/', views.six1, name='six1'),
    path('seven1/', views.seven1, name='seven1'),
    path('eight1/', views.eight1, name='eight1'),
    path('nine1/', views.nine1, name='nine1'),
    path('yard_checkin/', yard_checkin_view, name='yard_checkin'),
    path('inspection/<str:truck_no>/', truck_inspection_view, name='truck_inspection'),
    path('inspection-summary/', views.inspection_summary_view, name='inspection_summary'),
    path('truck_landing/', views.truck_landing, name='truck_landing'),
    path('status-log/<str:truck_no>/', views.status_log_view, name='status_log'),
    path('truck-log/', views.truck_log_view, name='truck_log_view'),
    path('truck-log/<str:truck_no>/', views.truck_log_view, name='track_log_view'),
    path('trucks/', views.truck_list, name='truck_list'),
    path('trucks/<str:truck_no>/', views.truck_detail, name='truck_detail'),
    path('truck-status/', views.truck_status_view, name='truck_status'),
    path('truck/<str:truck_no>/update-status/', update_truck_status, name='update_truck_status'),
    path('truck/<str:truck_no>/status-log/', views.status_log_view, name='status_log_view'),
    path('stock_upload/login', views.stock_upload_login, name='stock_upload_login'),
    path('stock_upload/menu', views.stock_menu, name='stock_menu'),
    path('stock_upload/batch_product', views.batch_product_view, name='batch_product'),
    path('stock/<str:pallet>/', views.stock_detail_view, name='stock_detail'),
    path('warehouse/', views.warehouse_view, name='warehouse_view'),
    path('warehouse/<int:whs_no>/', views.warehouse_detail_view, name='warehouse_detail'),
    path('warehouse/search/<int:whs_no>/', views.warehouse_search_view, name='warehouse_search_view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



