from django.contrib import admin
from .models import OrderForm, Orders, Cart, ShortDescriptions, \
    DemoVersionForm, Statistics, Instructions, Check, StatisticsDemo
from modeltranslation.admin import TranslationStackedInline, TabbedDjangoJqueryTranslationAdmin


class OrdersAdmin(admin.ModelAdmin):
    fields = ['items_ordered', 'date_added', 'completed', 'get_total_from_cart']
    readonly_fields = ['date_added', 'get_total_from_cart']


class ShortDescriptionsAdmin(admin.ModelAdmin):
    list_display = ['data_needed']


class ShortDescriptionInline(TranslationStackedInline):
    model = ShortDescriptions


class InstructionsAdmin(TabbedDjangoJqueryTranslationAdmin):
    inlines = [ShortDescriptionInline, ]
    list_display = ['name']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer']


class CheckAdmin(admin.ModelAdmin):
    fields = ['ordered_researches', 'total_price', 'date', 'client_bought']
    readonly_fields = ['ordered_researches', 'total_price', 'date', 'client_bought']
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


admin.site.register(OrderForm, OrderFormAdmin)
# admin.site.register(Orders, OrdersAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(DemoVersionForm, DemoVersionFormAdmin)
admin.site.register(ShortDescriptions, ShortDescriptionsAdmin)
admin.site.register(Instructions, InstructionsAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(Check, CheckAdmin)
