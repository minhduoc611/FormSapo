from .models import Order,Customer,Segment, Product,Category, OrderLine,UploadedFile
from .form import CustomerForm, SegmentForm, OrderLineForm, OrderForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
from django.contrib import messages
from django.views import View
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import csv
import pandas as pd
from django.db.models import Sum, Count
import openpyxl

# Create your views here.
def index(request):
    total_orders = Order.objects.count()
    total_customers = Customer.objects.count()
    total_revenue = OrderLine.objects.aggregate(Sum('line_amount'))['line_amount__sum'] or 0

    context = {
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_revenue': total_revenue,
    }
    return render(request, 'index.html', context)

def add_customer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = CustomerForm(data)
        if form.is_valid():
            customer = form.save()
            return JsonResponse({'success': True, 'customer': {'id': customer.id, 'name': customer.name}})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def customer_list(request):
    customers = Customer.objects.all()
    segments = Segment.objects.all()
    return render(request, 'Sapo/customer_list.html', {'customers': customers, 'segments': segments})


@csrf_exempt
def add_segment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            segment = Segment.objects.create(id=data['id'], description=data['description'])
            return JsonResponse({'success': True, 'segment': {'id': segment.id, 'description': segment.description}})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def segment_list(request):
    segments = Segment.objects.all()
    return render(request, 'Sapo/segment_list.html', {'segments': segments})



@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = Category.objects.get(id=data['category_id'])
            product = Product.objects.create(
                id=data['id'],
                name=data['name'],
                sale_price=data['sale_price'],
                category=category
            )
            return JsonResponse({'success': True, 'product': {
                'id': product.id,
                'name': product.name,
                'sale_price': product.sale_price,
                'category_name': product.category.name
            }})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'Sapo/product_list.html', {'products': products, 'categories': categories})


@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = Category.objects.create(
                id=data['id'],
                name=data['name']
            )
            return JsonResponse({'success': True, 'category': {'id': category.id, 'name': category.name}})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'Sapo/category_list.html', {'categories': categories})



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_lines = OrderLine.objects.filter(product=product).select_related('order__customer')

    context = {
        'product': product,
        'order_lines': order_lines
    }
    return render(request, 'Sapo/product_detail.html', context)


def add_orderline(request):
    if request.method == "POST":
        form = OrderLineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000')  
    else:
        form = OrderLineForm()
    return render(request, 'Sapo/add_orderline.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Customer, Product, Segment
from django.http import JsonResponse, HttpResponse
from decimal import Decimal
from django.db import transaction

def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            product_ids = request.POST.getlist('product[]')
            quantities = request.POST.getlist('quantity[]')

            for i in range(len(product_ids)):
                product = get_object_or_404(Product, id=product_ids[i])
                quantity = int(quantities[i])
                unit_price = product.sale_price
                line_amount = quantity * unit_price

                OrderLine.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    line_amount=line_amount
                )

            messages.success(request, 'Đơn hàng đã được lưu thành công!')
            return redirect('order_list')  # Chuyển hướng đến trang chủ hoặc trang khác
        else:
            messages.error(request, 'Có lỗi xảy ra. Vui lòng kiểm tra lại đơn hàng của bạn.')

    else:
        customers = Customer.objects.all()
        segments = Segment.objects.all()
        products = Product.objects.all()
        order_lines = OrderLine.objects.all()
        products = Product.objects.all()
        categories = Category.objects.all()

    return render(request, 'Sapo/add_order.html', {'customers': customers, 'products': products, 'segments': segments, 'order_line':order_lines,'products': products, 'categories': categories})

def order_list(request):
    orders = Order.objects.all().order_by('-id')  # Sắp xếp theo ID giảm dần
    return render(request, 'Sapo/order_list.html', {'orders': orders})


class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_lines = OrderLine.objects.filter(order=order)
        context = {
            'order': order,
            'order_lines': order_lines
        }
        return render(request, 'Sapo/order_detail.html', context)
    
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_lines = OrderLine.objects.filter(product=product).select_related('order__customer')

    context = {
        'product': product,
        'order_lines': order_lines
    }
    return render(request, 'Sapo/product_detail.html', context)

def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer=customer).select_related('customer')
    total_spent = sum(order.total_amount for order in orders)

    context = {
        'customer': customer,
        'orders': orders,
        'total_spent': total_spent,
        'segment': customer.segment
    }
    return render(request, 'Sapo/customer_detail.html', context)
    

from django.http import JsonResponse
from Sapo_app.models import Product

def get_product_info(request):
    product_id = request.GET.get('product_id')
    try:
        product = Product.objects.get(id=product_id)
        data = {
            'id': product.id,
            'name': product.name,
            'sale_price': product.sale_price,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist'}, status=404)

def upload_order_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        uploaded_file_record, created = UploadedFile.objects.get_or_create(
            file=uploaded_file, defaults={'processed': False})

        if not uploaded_file_record.processed:
            process_file(file_path)
            uploaded_file_record.processed = True
            uploaded_file_record.save()
        return redirect('order_list')
    return render(request, 'Sapo/upload_db.html')

def process_file(file_path):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    for row in ws.iter_rows(min_row=2, values_only=True):  # Assuming the first row is the header
        order_date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')  # Update the format to match your data
        order_id = row[1]
        customer_id = row[2]
        customer_name = row[3]
        segment_id = row[4]
        segment_description = row[5]
        category_id = row[6]
        category_name = row[7]
        product_id = row[8]
        product_name = row[9]
        orderline_quantity = int(row[10])
        product_sale_price = float(row[11])
        orderline_line_amount = float(row[12])

        segment, _ = Segment.objects.get_or_create(
            id=segment_id,
            defaults={'description': segment_description}
        )

        customer, _ = Customer.objects.get_or_create(
            id=customer_id,
            defaults={'name': customer_name, 'segment': segment}
        )

        category, _ = Category.objects.get_or_create(
            id=category_id,
            defaults={'name': category_name}
        )

        product, _ = Product.objects.get_or_create(
            id=product_id,
            defaults={'name': product_name, 'sale_price': product_sale_price, 'category': category}
        )

        order, _ = Order.objects.get_or_create(
            id=order_id,
            defaults={'order_date': order_date, 'customer': customer}
        )

        OrderLine.objects.create(
            order=order,
            product=product,
            quantity=orderline_quantity,
            unit_price=product_sale_price,
            line_amount=orderline_line_amount
        )