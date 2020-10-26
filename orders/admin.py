from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import OrderForm, Orders, Cart, ShortDescriptions, DemoVersionForm
from .serializers import to_dict
from django.core.mail import EmailMessage
from research.models import Research
from django.conf import settings

# Register your models here.


class OrdersAdmin(admin.ModelAdmin):
    fields = ['items_ordered', 'date_added', 'completed', 'get_total_from_cart']
    readonly_fields = ['date_added', 'get_total_from_cart']


admin.site.register(OrderForm)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Cart)
admin.site.register(DemoVersionForm)
admin.site.register(ShortDescriptions)
