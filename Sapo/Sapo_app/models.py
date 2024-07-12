from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Customer model

class Segment(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id} - {self.description}"
    

class Customer(models.Model):
    id = models.CharField(max_length=10, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate the ID with prefix CUZ and unique suffix
            last_customer = Customer.objects.all().order_by('id').last()
            if last_customer:
                last_id = int(last_customer.id[4:])
                self.id = f'CUZ{last_id + 1:05d}'
            else:
                self.id = 'CUZ00001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.id}"   


#Category model
class Category(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Product model
class Product(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.name}"

# Order model
class Order(models.Model):
    id = models.CharField(max_length=10, primary_key=True, editable=False, unique=True)
    order_date = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate the ID with prefix ORD and unique suffix
            last_order = Order.objects.all().order_by('id').last()
            if last_order:
                last_id = int(last_order.id[6:])
                self.id = f'ORD{last_id + 1:07d}'
            else:
                self.id = 'ORD0000001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.order_date}"
    
# Order Line model
class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,editable=False)
    line_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Update unit_price based on product's sale_price
        self.unit_price = self.product.sale_price
        # Calculate line_amount before saving
        self.line_amount = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.id} - {self.product.name}"

@receiver(post_save, sender=OrderLine)
@receiver(post_delete, sender=OrderLine)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    order.total_amount = OrderLine.objects.filter(order=order).aggregate(total=models.Sum('line_amount'))['total'] or 0
    order.save()



class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name
    