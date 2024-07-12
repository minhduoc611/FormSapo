from django.urls import path
from . import views
from .views import product_detail, add_order, customer_detail, OrderDetailView, upload_order_file




urlpatterns = [
    path('', views.index, name='index'),
    path('customers/', views.customer_list, name='customer_list'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_segment/', views.add_segment,name='add_segment'),
    path('segment_list/',views.segment_list,name='segment_list'),
    path('products/', views.product_list, name='product_list'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('products/add/', views.add_product, name='add_product'),
    path('product/<str:product_id>/', product_detail, name='product_detail'),
    path('add_orderline/', views.add_orderline, name='add_orderline'),
    path('add_order/', add_order, name='add_order'),
    path('order_list/',views.order_list,name='order_list'),
    path('customer/<str:customer_id>/', customer_detail, name='customer_detail'),
    path('order/<str:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('get-product-info/', views.get_product_info, name='get_product_info'),
    path('upload_order_file/', upload_order_file, name='upload_order_file'),




]