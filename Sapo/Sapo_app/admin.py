from django.contrib import admin
from .models import Customer, Product, Order, OrderLine, Category, Segment,UploadedFile
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','name','segment']
    search_fields=['id','name','segment']
admin.site.register(Customer)


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
admin.site.register(Product)

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
admin.site.register(Order)

class OrderLineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderLine._meta.fields]
admin.site.register(OrderLine)

class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]
admin.site.register(Category)

class SegmentAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Segment._meta.fields ]
admin.site.register(Segment)