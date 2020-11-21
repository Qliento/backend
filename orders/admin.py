from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import OrderForm, Orders, Cart, ShortDescriptions, DemoVersionForm, Statistics, Instructions, Check
from .serializers import to_dict
from django.core.mail import EmailMessage
from research.models import Research
from django.conf import settings

# Register your models here.


class OrdersAdmin(admin.ModelAdmin):
    fields = ['items_ordered', 'date_added', 'completed', 'get_total_from_cart']
    readonly_fields = ['date_added', 'get_total_from_cart']


class ShortDescriptionsAdmin(admin.ModelAdmin):
    list_display = ['data_needed']


class ShortDescriptionInline(admin.TabularInline):
    model = ShortDescriptions


class InstructionsAdmin(admin.ModelAdmin):
    inlines = [ShortDescriptionInline, ]
    list_display = ['name']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'ordered_item']


class CheckAdmin(admin.ModelAdmin):
    fields = ['ordered_researches', 'total_price', 'date', 'client_bought']
    readonly_fields = ['ordered_researches', 'total_price', 'date', 'client_bought']
    list_display = ['client_bought', 'date']


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['partner_admin']
    readonly_fields = ['partner_admin', 'demo_downloaded', 'watches', 'bought']


admin.site.register(OrderForm)
# admin.site.register(Orders, OrdersAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(DemoVersionForm)
admin.site.register(ShortDescriptions, ShortDescriptionsAdmin)
admin.site.register(Instructions, InstructionsAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(Check, CheckAdmin)
