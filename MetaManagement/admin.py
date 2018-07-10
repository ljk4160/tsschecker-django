from django.contrib import admin

# Register your models here.
from MetaManagement.models import Device, Signature
from django.utils.translation import ugettext as _

admin.site.site_header = _("MetaManagement")
admin.site.site_title = _("MetaManagement")


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'ecid', 'product_type', 'hw_model')
    search_fields = ['name', 'ecid']
    readonly_fields = ['created_at']


class SignatureAdmin(admin.ModelAdmin):
    list_display = ('device', 'blob_version', 'blob_build', 'created_at')
    search_fields = ['device__name', 'device__ecid']
    readonly_fields = ['created_at']


admin.site.register(Device, DeviceAdmin)
admin.site.register(Signature, SignatureAdmin)

