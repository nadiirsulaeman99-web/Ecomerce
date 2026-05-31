from django.contrib import admin
from .models import Order, OrderItem

import csv
import datetime
from django.http import HttpResponse

from django.utils.safestring import mark_safe
from django.urls import reverse


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}" target="_blank">PDF</a>')

order_pdf.short_discription = 'Invoice'


def export_to_csv(modeladmin, request, qureyset):
    # Htt response
    obts = modeladmin.model._meta
    content_disposition = f"attachment; filename={obts.verbose_name}.csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition

    #csv file
    writer = csv.writer(response)
    fields = [field for field in obts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow(field.verbose_name for field in fields)

    for obj in qureyset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d%m%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_discription = 'Export to CSV'

class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['frist_name', 'email', 'create_at', 'paid', order_pdf]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
