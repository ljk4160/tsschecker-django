from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.


class Device(models.Model):
    class Meta(object):
        verbose_name = _("Meta")
        verbose_name_plural = _("Metas")

    ecid = models.CharField(
        primary_key=True,
        verbose_name=_("ECID"),
        max_length=16,
        blank=False,
        unique=True,
        null=False
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False
    )

    hw_model = models.CharField(
        verbose_name=_("HW Model"),
        max_length=16,
        blank=False,
        help_text=_("Example: n90ap"),
    )

    product_type = models.CharField(
        verbose_name=_("Product Type"),
        max_length=16,
        blank=False,
        help_text=_("Example: iPhone10,3"),
    )

    ios_version = models.CharField(
        verbose_name=_("iOS Version"),
        max_length=16,
        blank=False,
        help_text=_("Example: 11.4"),
    )

    ios_build = models.CharField(
        verbose_name=_("iOS Build"),
        max_length=16,
        blank=True,
        default="",
        help_text=_("Example: 15F5061e"),
    )

    generator = models.CharField(
        verbose_name=_("Generator"),
        max_length=32,
        blank=True
    )

    def __unicode__(self):
        return self.name + ' (' + self.ecid + ')'


class Signature(models.Model):
    class Meta(object):
        verbose_name = _("Signature")
        verbose_name_plural = _("Signatures")

    id = models.AutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )

    device = models.ForeignKey(
        Device,
        verbose_name=_("Device")
    )

    blob_version = models.CharField(
        verbose_name=_("Blob Version"),
        max_length=16,
        blank=False,
        help_text=_("Example: 11.4"),
    )

    blob_build = models.CharField(
        verbose_name=_("Blob Build"),
        max_length=16,
        blank=True,
        default="",
        help_text=_("Example: 15F5061e"),
    )

    ap_nonce = models.CharField(
        verbose_name=_("Blob Nonce"),
        max_length=64,
        blank=True,
        default=""
    )

    blob_file = models.FileField(
        verbose_name=_("Blob File"),
        max_length=255,
        upload_to="shsh2",
        help_text=_("Choose a Blob File (*.shsh2) to upload"),
        blank=True,
        null=True,
    )

    def __unicode__(self):
        if len(self.blob_build) > 0:
            return self.device.ecid + ' (' + self.blob_version + '-' + self.blob_build + ')'
        else:
            return self.device.ecid + ' (' + self.blob_version + ')'

