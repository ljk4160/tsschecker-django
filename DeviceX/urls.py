"""DeviceX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from MetaManagement.views import register_device, sign_device

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/sign/$', sign_device, name='sign_device'),
    url(r'^api/register/$', register_device, name='register_device')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns.append(url(r'^admin/sites/django-rq/', include('django_rq.urls')))

handler400 = 'MetaManagement.error.bad_request'
handler404 = 'MetaManagement.error.page_not_found'
handler500 = 'MetaManagement.error.server_error'

