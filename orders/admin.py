from django.contrib import admin
from .models import OrderForm, Orders, Cart, ShortDescriptions, \
    DemoVersionForm, Statistics, Check, StatisticsDemo, StatisticsBought, StatisticsWatches
from modeltranslation.admin import TranslationStackedInline, TabbedDjangoJqueryTranslationAdmin
from social_django.admin import UserSocialAuth, Nonce, Association
from oauth2_provider.admin import Application, RefreshToken, AccessToken, Grant


class ShortDescriptionAdmin(TabbedDjangoJqueryTranslationAdmin):
    list_display = ['title']


class CheckAdmin(admin.ModelAdmin):
    fields = ['ordered_researches', 'total_price', 'date', 'client_bought', 'order_id', 'pg_payment_id']
    readonly_fields = ['ordered_researches', 'total_price', 'date', 'client_bought', 'order_id', 'pg_payment_id']
    list_display = ['client_bought', 'date']


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['research_to_collect', 'get_name_partner']
    fields = ['research_to_collect', 'get_name_partner', 'get_demo_downloaded', 'get_total_watches', 'get_total_purchases']
    readonly_fields = ['get_name_partner', 'get_demo_downloaded', 'get_total_watches', 'get_total_purchases']

    def get_name_partner(self, obj):
        return obj.get_name_partner
    get_name_partner.short_description = 'Партнёр'

    def get_demo_downloaded(self, obj):
        return obj.get_demo_downloaded
    get_demo_downloaded.short_description = 'Количество скачанных демо-версий'

    def get_total_watches(self, obj):
        return obj.get_total_watches
    get_total_watches.short_description = 'Количество просмотров'

    def get_total_purchases(self, obj):
        return obj.get_total_purchases
    get_total_watches.short_description = 'Количество покупок'


class DemoVersionFormAdmin(admin.ModelAdmin):
    list_display = ['email']


class OrderFormAdmin(admin.ModelAdmin):
    list_display = ['email']


class CartInline(admin.TabularInline):
    list_display = ['id']
    model = Cart
    fields = ['ordered_item', 'calculate_total_price', 'added', 'date_added']
    readonly_fields = ['calculate_total_price', 'date_added']
    extra = 0


class OrdersAdmin(admin.ModelAdmin):
    inlines = [CartInline]
    list_display = ['buyer']
    fields = ['total_sum', 'buyer', 'pg_sig']
    readonly_fields = ['total_sum', 'pg_sig']

    def get_object(self, request, object_id, from_field=None):
        qs = Orders.objects.get(id=object_id)
        check_price = Cart.objects.filter(user_cart=int(object_id), added=False)
        total_price = 0
        try:
            for i in check_price:
                if i is None:
                    pass
                else:
                    total_price += i.calculate_total_price
            if qs.total_sum != total_price:
                qs.total_sum = total_price
            else:
                pass
            return qs
        except:
            raise ValueError({"detail": "Something went wrong"})


admin.site.register(OrderForm, OrderFormAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Cart)

admin.site.register(DemoVersionForm, DemoVersionFormAdmin)
admin.site.register(ShortDescriptions, ShortDescriptionAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(Check, CheckAdmin)

admin.site.register(StatisticsDemo)
admin.site.register(StatisticsWatches)
admin.site.register(StatisticsBought)

admin.site.unregister(UserSocialAuth)
admin.site.unregister(Nonce)
admin.site.unregister(Association)
admin.site.unregister(Application)
admin.site.unregister(RefreshToken)
admin.site.unregister(AccessToken)
admin.site.unregister(Grant)
