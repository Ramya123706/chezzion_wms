from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import yard_checkin_view, truck_inspection_view, update_truck_status

urlpatterns = [
    # General
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('start/', views.first, name='first'),
    path('six/', views.sixth, name='sixth'),
    path("search/", views.search, name="search"),

    # Outbound steps
    path('outbound1/', views.outbound1, name='outbound1'),
    path('outbound2/', views.outbound2, name='outbound2'),
    path('outbound3/', views.outbound3, name='outbound3'),
    path('outbound4/', views.outbound4, name='outbound4'),
    path('outbound5/', views.outbound5, name='outbound5'),
    path('outbound6/', views.outbound6, name='outbound6'),
    path('outbound7/', views.outbound7, name='outbound7'),

    # HU-related
    path('hu1/', views.hu1, name='hu1'),
    path('hu12/', views.hu12, name='hu12'),
    path('hu123/', views.hu123, name='hu123'),

    # New steps
    path('new1/', views.new1, name='new1'),
    path('new2/', views.new2, name='new2'),
    path('new3/', views.new3, name='new3'),
    path('new4/', views.new4, name='new4'),

    # Check-in and inspection
    path('one/', yard_checkin_view, name='one'),
    path('three/', views.three, name='three'),
    path('four/', views.four, name='four'),
    path('yard_checkin/', yard_checkin_view, name='yard_checkin'),
    path('get-truck-details/', views.get_truck_details, name='get_truck_details'),
    path('inspection/<str:truck_no>/', truck_inspection_view, name='truck_inspection'),
    path('inspection-summary/', views.inspection_summary_view, name='inspection_summary'),
    path('truck_landing/', views.truck_landing, name='truck_landing'),
    # path("questions/", views.question_list, name="question_list"),
    # path("questions/add/", views.add_question, name="add_question"),
    # path("questions/delete/<int:pk>/", views.delete_question, name="delete_question"),
    # Truck Logs
    path('status-log/<str:truck_no>/', views.status_log_view, name='status_log'),
    path('truck-log/<str:truck_no>/', views.truck_log_view, name='truck_log_view'),
    path('truck-status/', views.truck_status_view, name='truck_status'),
    path('truck/<str:truck_no>/update-status/', update_truck_status, name='update_truck_status'),
    path('truck/<str:truck_no>/status-log/', views.status_log_view, name='status_log_view'),
    path('trucks/', views.truck_list, name='truck_list'),
    path('trucks/<str:truck_no>/', views.truck_detail, name='truck_detail'),

    # Product Management
    path('product/', views.product_view, name='add_product'),
    path('product/<str:product_id>/', views.product_detail_view, name='product_detail'),
    path('product/edit/<str:product_id>/', views.product_edit, name='product_edit'),
    path('product-list/', views.product_list, name='product_list'),
    path('product/delete/<str:product_id>/', views.product_delete, name='product_delete'),


    path('ajax/product-suggestions/', views.product_suggestions, name='product_suggestions'),
    path('get-product-description/<int:product_id>/', views.get_product_description, name='get_product_description'),

    # Stock Upload
    path('stock_upload/login', views.stock_upload_login, name='stock_upload_login'),
    path('stock_upload/menu', views.stock_menu, name='stock_menu'),
    path('stock_upload/batch_product', views.batch_product_view, name='batch_product'),
    path('stock/<int:pk>/', views.stock_detail_view, name='stock_detail'),
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    # path('products/search/', views.product_search, name='product_search'),
    # Warehouse
    path('warehouse/', views.warehouse_view, name='warehouse_view'),
    path('warehouse/<int:whs_no>/', views.warehouse_detail_view, name='warehouse_detail'),
    path('warehouse_search/<int:whs_no>/', views.warehouse_search_view, name='warehouse_search_details'),
    path('warehouse/edit/<int:whs_no>/', views.edit_warehouse, name='edit_warehouse'),

    # Inventory & Bin
    path('inventory/', views.inventory_view, name='inventory'),
    path('create_bin/', views.create_bin, name='create_bin'),

    # Customers
    path('add_customers/', views.add_customers, name='add_customers'),
    path('customers/', views.customers_list, name='customers_list'),
    path('customers/<str:customer_id>/', views.customers_detail, name='customers_detail'),
    path('customers/<str:customer_id>/edit/', views.customers_edit, name='customers_edit'),
    path('customers/delete/<int:customer_id>/', views.customers_delete, name='customers_delete'),

    # Vendor
    path('add_vendor/', views.add_vendor, name='add_vendor'),
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/<str:vendor_id>/', views.vendor_detail, name='vendor_detail'),
    path('vendors/<str:vendor_id>/edit/', views.vendor_edit, name='vendor_edit'),
    path('vendors/<str:vendor_id>/delete/', views.vendor_delete, name='vendor_delete'),

    # Purchase Orders
    path('purchase_order/add_purchase/', views.add_purchase, name='add_purchase'),
    path('purchase/<int:pk>/', views.purchase_detail, name='purchase_detail'),
    path('purchase/edit/<int:po_id>/', views.purchase_edit, name='purchase_edit'),
    path('purchase/<int:pk>/pdf/', views.download_po_pdf, name='purchase_pdf'),
    path("purchases/", views.purchase_list_view, name="purchase_list"),


    # RF & Tasks
    path('rf_ptl/', views.rf_ptl, name="rf_plt"),
    path('task/', views.task, name='task'),

    # Categories
    path('add-category/', views.add_category, name='add_category'),
    path('ajax/category-suggestions/', views.category_suggestions, name='category_suggestions'),
    path("get-subcategories/<int:category_id>/", views.get_subcategories, name="get_subcategories"),
    path("ajax/load-subcategories/", views.load_subcategories, name="ajax_load_subcategories"),
    # Suggestions
    path('ajax/truck-suggestions/', views.truck_suggestions, name='truck_suggestions'),
    path('ajax/whs-suggestions/', views.whs_suggestions, name='whs_suggestions'),


    # Picking
    path('add_picking/', views.add_picking, name='add_picking'),
    path('pending_task/', views.pending_task, name='pending_task'),
    path('picking/edit/<str:picking_id>/', views.edit_picking, name='edit_picking'),
    path('picking/confirm/<str:picking_id>/', views.confirm_picking, name='confirm_picking'),
    path('picking/delete/<str:picking_id>/', views.delete_picking, name='delete_picking'),
    path('putaway_task/', views.putaway_task, name='putaway_task'),
    path('pending_tasks/', views.putaway_pending, name='putaway_pending'),
    path('putaway/edit/<str:putaway_id>/', views.edit_putaway, name='edit_putaway'),
    path('putaway/confirm/<str:putaway_id>/', views.confirm_putaway, name='confirm_putaway'),
    path('putaway/delete/<str:putaway_id>/', views.delete_putaway, name='delete_putaway'),
    path('add_picking/', views.add_picking, name='add_picking'),
    path('pending_task/', views.pending_task, name='pending_task'),
    path('customer/', views.customer, name='customer'),

    path('ajax/whs-suggestions/', views.whs_suggestions, name='whs_suggestions'),
    path('ajax/category-suggestions/', views.category_suggestions, name='category_suggestions'),

    path('add_picking/', views.add_picking, name='add_picking'),
    path('pending_task/', views.pending_task, name='pending_task'),
    path('picking/edit/<str:picking_id>/', views.edit_picking, name='edit_picking'),
    path('customer/', views.customer, name='customer'),
    path('picking/confirm/<str:picking_id>/', views.confirm_picking, name='confirm_picking'),
    path('picking/delete/<str:picking_id>/', views.delete_picking, name='delete_picking'),
    path('inbound_delivery/', views.inbound_delivery, name='inbound_delivery'),
    path('get-po-products/<int:po_id>/', views.get_po_products, name='get_po_products'),
    path('inbound/delivery_detail/<str:inbound_delivery_number>/', views.delivery_detail, name='delivery_detail'),
    path('inbound_delivery/edit/<str:inbound_delivery_number>/', views.edit_inbound_delivery, name='edit_inbound_delivery'),
    path('po-suggestions/', views.po_suggestions, name='po_suggestions'),


    # Pallet Management
    path('create_pallet/', views.creating_pallet, name='creating_pallet'),
    path('pallet/<str:pallet_no>/', views.pallet_detail, name='pallet_detail'),
    path('pallet/edit/<str:pallet_no>/', views.edit_pallet, name='edit_pallet'),
    path('pallet/delete/<str:pallet_no>/', views.delete_pallet, name='delete_pallet'), 
    path('edit_pallet/<str:pallet_no>/', views.edit_pallet, name='edit_pallet'),
    path('add_child_pallet/', views.add_child_pallet, name='add_child_pallet'),

    # Customer landing
    path('customer/', views.customer, name='customer'),
    path('get-po-products/<int:po_id>/', views.get_po_products, name='get_po_products'),
    path('sales_order_creation/',views.sales_order_creation,name='sales_order_creation'),
    path('sales/', views.sales_order_list, name='sales_order_list'),
    path("get-warehouse-address/<int:whs_id>/", views.get_warehouse_address, name="get_warehouse_address"),
    path('product-autocomplete/', views.product_autocomplete, name='product-autocomplete'),

    path('sales/<str:so_no>/', views.sales_order_detail, name='sales_order_detail'),
    path('sales-order/edit/<str:so_no>/', views.sales_order_edit, name='sales_order_edit'),
    path('sales/<str:so_no>/delete/', views.sales_order_delete, name='sales_order_delete'),
    path("sales/<str:so_no>/pdf/", views.sales_order_pdf, name="sales_order_pdf"),

    # Outbound Delivery
    path('outbound/', views.outbound, name='outbound'),
    path('get-so-products/<int:so_id>/', views.get_so_products, name='get_so_products'),
    path("packing/create/", views.create_packing, name="create_packing"),
    path("packing/", views.packing_list, name="packing_list"),  
    path("packing/detail/<int:packing_id>/", views.packing_detail, name="packing_detail"),
    # path("packing/<int:packing_id>/add_item/", views.add_packed_item, name="add_packed_item"),
    path("packing/<int:packing_id>/edit/", views.edit_packing, name="edit_packing"),
    path("packing/<int:packing_id>/delete/", views.delete_packing, name="delete_packing"),
    path("packing/<int:packing_id>/add-item/", views.add_packed_item, name="add_packed_item"),
    path("tasks/", views.all_tasks, name="all_tasks"),
    path("putaway/<str:putaway_id>/", views.putaway_detail, name="putaway_detail"),
    path("picking/<str:picking_id>/", views.picking_detail, name="picking_detail"),         
    path("material/create/", views.material_create, name="material_create"),
    path("material/", views.material_list, name="material_list"),  
    path("material/<int:id>/edit/", views.material_edit, name="material_edit"), 
    path("material/<int:id>/delete/", views.material_delete, name="material_delete"),
    path("get-total-quantity/<str:product_id>/", views.get_total_quantity, name="get_total_quantity"),
    path("outbound/<str:delivery_no>/", views.outbound_detail, name="outbound_detail"),
# Outbound → PGI
    path("pgi/<str:delivery_no>/", views.post_goods_issue, name="post_goods_issue"),
    path("pgi/detail/<str:pgi_no>/", views.pgi_detail, name="pgi_detail"),

    # Inbound → GR
    path("gr/<str:inbound_no>/", views.goods_receipt, name="goods_receipt"),
    path("gr/detail/<str:gr_no>/", views.gr_detail, name="gr_detail"),
    #GR
    path('create-gr/', views.create_gr, name='create_gr'),
    path("gr_list/", views.gr_list, name="gr_list"),

    path("bulk-upload-bins/", views.bulk_upload_bins, name="bulk_upload_bins"),
    path('bulk-upload-products/', views.bulk_upload_products, name='bulk_upload_products'),
    path('batch-product/upload-csv/', views.batch_product_csv_upload, name='batch_product_csv_upload'),

 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
