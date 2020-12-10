from django.contrib import admin
from .models import OrderForm, Orders, Cart, ShortDescriptions, \
    DemoVersionForm, Statistics, Check, StatisticsDemo
from modeltranslation.admin import TranslationStackedInline, TabbedDjangoJqueryTranslationAdmin


# class OrdersAdmin(admin.ModelAdmin):
#     fields = ['items_ordered', 'date_added', 'completed', 'get_total_from_cart']
#     readonly_fields = ['date_added', 'get_total_from_cart']


class ShortDescriptionAdmin(TabbedDjangoJqueryTranslationAdmin):
    list_display = ['title']


class CheckAdmin(admin.ModelAdmin):
    fields = ['ordered_researches', 'total_price', 'date', 'client_bought', 'order_id']
    readonly_fields = ['ordered_researches', 'total_price', 'date', 'client_bought', 'order_id']
    list_display = ['client_bought', 'date']


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['research_to_collect', 'get_name_partner']
    fields = ['research_to_collect', 'bought', 'get_name_partner', 'get_demo_downloaded', 'get_total_watches']
    readonly_fields = ['get_name_partner', 'demo_downloaded', 'watches', 'get_demo_downloaded', 'get_total_watches']

    def get_name_partner(self, obj):
        return obj.get_name_partner
    get_name_partner.short_description = 'Партнёр'

    def get_demo_downloaded(self, obj):
        return obj.get_demo_downloaded
    get_demo_downloaded.short_description = 'Количество скачанных демо-версий'

    def get_total_watches(self, obj):
        return obj.get_total_watches
    get_total_watches.short_description = 'Количество просмотров'


class DemoVersionFormAdmin(admin.ModelAdmin):
    list_display = ['email']


class OrderFormAdmin(admin.ModelAdmin):
    list_display = ['email']


# class CartAdmin(admin.ModelAdmin):
#     list_display = ['id']
#
#     fields = ['ordered_item', 'calculate_total_price', 'added', 'date_added']
#     readonly_fields = ['calculate_total_price', 'date_added', 'added']
#
#     def calculate_total_price(self, obj):
#         return obj.calculate_total_price
#     calculate_total_price.short_description = 'Сумма'


class CartInline(admin.StackedInline):
    list_display = ['id']
    model = Cart
    fields = ['ordered_item', 'calculate_total_price', 'added', 'date_added']
    readonly_fields = ['calculate_total_price', 'date_added', 'added']
    extra = 1


class OrdersAdmin(admin.ModelAdmin):
    inlines = [CartInline]
    list_display = ['buyer']
    fields = ['total_sum', 'buyer']
    readonly_fields = ['total_sum']

    def get_queryset(self, request):
        qs = super(OrdersAdmin, self).get_queryset(request)
        the_id = list(qs.values('id'))[0]
        check_price = Cart.objects.filter(user_cart=the_id.get('id'))
        total_price = 0
        try:
            for i in check_price:
                total_price += i.calculate_total_price
            if qs.values('total_sum') != total_price:
                qs.update(total_sum=total_price)
            else:
                pass
            return qs
        except:
            raise ValueError


admin.site.register(OrderForm, OrderFormAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Cart, )
admin.site.register(DemoVersionForm, DemoVersionFormAdmin)
admin.site.register(ShortDescriptions, ShortDescriptionAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(Check, CheckAdmin)
