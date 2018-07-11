from django.conf.urls import url
from django.contrib import admin, messages

# Register your models here.
import django_rq
from django.utils.translation import ugettext as _
from MetaManagement.models import Device, Signature
from MetaManagement.views import handle_signing_task

admin.site.site_header = _("MetaManagement")
admin.site.site_title = _("MetaManagement")


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'ecid', 'product_type', 'hw_model')
    search_fields = ['name', 'ecid']
    readonly_fields = ['created_at']


class SignatureAdmin(admin.ModelAdmin):
    list_display = ('device', 'blob_version', 'blob_build', 'is_fetched', 'created_at')
    search_fields = ['device__name', 'device__ecid']
    readonly_fields = ['created_at', 'is_fetched']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None, so this is an edit
            return ['device', 'blob_version', 'blob_build', 'blob_file', 'ap_nonce', 'is_ota', 'is_fetched', 'created_at']
        else:  # This is an addition
            return ['created_at', 'is_fetched']

    def save_model(self, request, obj, form, change):
        """
        :type obj: Signature
        """
        super(SignatureAdmin, self).save_model(request, obj, form, change)
        # if obj.blob_file.name:
        #     pass
        # else:
        request_dict = {
            'ecid': obj.device.ecid,
            'product_type': obj.device.product_type,
            'hw_model': obj.device.hw_model,
            'ios_version': obj.blob_version,
            'ios_build': obj.blob_build,
            'ap_nonce': obj.ap_nonce,
            'replace': True,
        }
        if obj.is_ota:
            request_dict.update({'ota': obj.is_ota})
        queue = django_rq.get_queue('high')
        queue.enqueue(handle_signing_task, request_dict, True)
        messages.info(request, _("%s signing task has been added to the \"high\" queue.") % str(obj))


admin.site.register(Device, DeviceAdmin)
admin.site.register(Signature, SignatureAdmin)

