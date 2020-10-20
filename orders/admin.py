from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import OrderForm, Orders, Cart, ItemsInCart, DemoVersionForm
from .serializers import to_dict
from django.core.mail import EmailMessage
from research.models import Research
from django.conf import settings

# Register your models here.


class OrdersAdmin(admin.ModelAdmin):
    fields = ['items_ordered', 'date_added', 'completed', 'get_total_from_cart']
    readonly_fields = ['date_added', 'get_total_from_cart']

#
# class DemoVersionFormAdmin(admin.ModelAdmin):
#     change_form_template = "admin/send_file.html"
#
#     def response_change(self, request, obj):
#         if "_approve" in request.POST:
#
#             get_this_order = to_dict(obj)
#             research_demo = get_this_order.get('desired_research')
#             email_of_recipient = get_this_order.get('email')
#
#             get_pdf_demo = Research.objects.filter(id=research_demo).values()
#             normalized_data = list(get_pdf_demo)[0]
#             name_of_file = normalized_data.get('demo')
#             title_of_file = normalized_data.get('name')
#             id_of_file = normalized_data.get('id')
#
#             mail = EmailMessage(' Демо-версия',
#                                 'Доброго времени суток, пользователь. '
#                                 'По вашему запросу, вам была отправлена демоверсия исследования в формате PDF. \n'
#                                 'Название: "{}" \n'
#                                 'Идентификатор: {} \n'
#                                 '\n'
#                                 'С уважением, команда Qliento'.format(title_of_file, id_of_file),
#                                 settings.EMAIL_HOST_USER,
#                                 [email_of_recipient])
#
#             mail.attach_file('static/files/{}'.format(name_of_file))
#             mail.send()
#
#             return HttpResponseRedirect(".")
#         return super().response_change(request, obj)


admin.site.register(OrderForm)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Cart)
admin.site.register(DemoVersionForm)
