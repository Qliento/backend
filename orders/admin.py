from django.contrib import admin
from .models import OrderForm, Orders, Cart, ItemsInCart
# Register your models here.


# class OrdersAdmin(admin.ModelAdmin):
#     fields = ['ordered_researches', 'date_added', 'completed', 'customer', 'total']
#     readonly_fields = ['date_added']


admin.site.register(OrderForm)
admin.site.register(Orders)
admin.site.register(Cart)
admin.site.register(ItemsInCart)
