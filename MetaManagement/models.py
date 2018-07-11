from __future__ import unicode_literals

from django.core.validators import RegexValidator
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
        null=False,
        validators=[
            RegexValidator(
                r'^[A-Fa-f0-9]+$',
                _("Enter a valid 'ECID' consisting of hex letters and numbers."),
                'invalid'
            )
        ]
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
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9]+$',
                _("Enter a valid 'HW Model' consisting of letters and numbers."),
                'invalid'
            )
        ]
    )

    product_type = models.CharField(
        verbose_name=_("Product Type"),
        max_length=16,
        blank=False,
        help_text=_("Example: iPhone10,3"),
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9|,]+$',
                _("Enter a valid 'Product Type' consisting of letters, numbers and commas."),
                'invalid'
            )
        ]
    )

    ios_version = models.CharField(
        verbose_name=_("iOS Version"),
        max_length=16,
        blank=False,
        help_text=_("Example: 11.4"),
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9|\.]+$',
                _("Enter a valid 'iOS Version' consisting of letters, numbers and dots."),
                'invalid'
            )
        ]
    )

    ios_build = models.CharField(
        verbose_name=_("iOS Build"),
        max_length=16,
        blank=True,
        default="",
        help_text=_("Example: 15F5061e"),
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9]+$',
                _("Enter a valid 'iOS Build' consisting of letters and numbers."),
                'invalid'
            )
        ]
    )

    generator = models.CharField(
        verbose_name=_("Generator"),
        max_length=32,
        blank=True,
        validators=[
            RegexValidator(
                r'^[A-Fa-f0-9]+$',
                _("Enter a valid 'Generator' consisting of hex letters and numbers."),
                'invalid'
            )
        ]
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
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9|\.]+$',
                _("Enter a valid 'Blob Version' consisting of letters, numbers and dots."),
                'invalid'
            )
        ]
    )

    blob_build = models.CharField(
        verbose_name=_("Blob Build"),
        max_length=16,
        blank=True,
        default="",
        help_text=_("Example: 15F5061e"),
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9]+$',
                _("Enter a valid 'Blob Build' consisting of letters and numbers."),
                'invalid'
            )
        ]
    )

    ap_nonce = models.CharField(
        verbose_name=_("Blob Nonce"),
        max_length=64,
        blank=True,
        default="",
        validators=[
            RegexValidator(
                r'^[A-Fa-f0-9]+$',
                _("Enter a valid 'Blob Nonce' consisting of hex letters and numbers."),
                'invalid'
            )
        ]
    )

    is_ota = models.BooleanField(
        verbose_name=_("OTA Ticket"),
        default=False
    )

    blob_file = models.FileField(
        verbose_name=_("Blob File"),
        max_length=255,
        upload_to="shsh2",
        help_text=_("Choose a Blob File (*.shsh2) to upload"),
        blank=True,
        null=True,
    )

    is_fetched = models.BooleanField(
        verbose_name=_("Blob Fetched"),
        default=False
    )

    def __unicode__(self):
        if len(self.blob_build) > 0:
            return self.device.ecid + ' (' + self.blob_version + '-' + self.blob_build + ')'
        else:
            return self.device.ecid + ' (' + self.blob_version + ')'

