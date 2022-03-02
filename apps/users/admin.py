from django.contrib import admin
from .models import User, Contact
import datetime 
import csv 
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from .forms import UserForm


def csv_export(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = 'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() \
        if not field.many_to_many and not field.one_to_many and not field.one_to_one]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
csv_export.short_description = 'Export to CSV'

def user_pdf(obj):
    url = reverse('admin_user_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
user_pdf.short_description = 'User detail PDF'

def user_detail(obj):
    url = reverse('admin_user_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = (
        'username', 'email', 'phone', 'full_name', 'gender', 
        user_detail, user_pdf
    )
    list_filter = (
        'gender', 'date_joined', 'is_active', 'is_staff'
    )
    actions = [csv_export]


admin.site.register(User, UserAdmin)
admin.site.register(Contact)
