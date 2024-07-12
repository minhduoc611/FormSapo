from django import forms
from .models import Customer,OrderLine,Product,Order,Segment,Category
from django.utils.timezone import localtime, get_current_timezone

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address', 'segment']
        widgets = {
            'segment': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['segment'].queryset = Segment.objects.all()



class SegmentForm(forms.ModelForm):
    class Meta:
        model = Segment
        fields = ['id', 'description']



class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ['order', 'product', 'quantity']
        widgets = {
            'order': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
OrderLineFormSet = forms.inlineformset_factory(Order, OrderLine, form=OrderLineForm, extra=1)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('id',)
        fields = ['order_date', 'customer']
        widgets = {
            'order_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control','step': '60'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),

        }
        input_formats = {
            'order_date': ['%Y-%m-%dT%H:%M'],
        }