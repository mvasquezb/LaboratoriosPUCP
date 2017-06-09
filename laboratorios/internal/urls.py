from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    #
    #ServiceRequest
    #
    url('^serviceRequest/attachFile/(?P<id>\d+)$',
        views.serviceRequest.upload,
        name='serviceRequest.upload'),
    url('^serviceRequest/files/(?P<id>\d+)$',
        views.serviceRequest.attachmentList,
        name='serviceRequest.attachmentList'),
    url('^serviceRequest/attachedFileShow/(?P<id>\d+)$',
        views.serviceRequest.showAttachedFile,
        name='serviceRequest.showAttachedFile'),
    url('^serviceRequest/deleteAttachedFile/(?P<id>\d+)$',
        views.serviceRequest.deleteAttachedFile,
        name='serviceRequest.deleteAttachedFile'),
    url('^serviceRequest/downloadAttachedFile/(?P<id>\d+)$',
        views.serviceRequest.downloadAttachedFile,
        name='serviceRequest.downloadAttachedFile'),
    #
    # Employee
    #
    url('^employee/$',
        views.employee.index,
        name='employee.index'),
    url('^employee/create$',
        views.employee.create,
        name='employee.create'),
    url('^employee/edit/(?P<pk>\d+)$',
        views.employee.edit,
        name='employee.edit'),
    url('^employee/show/(?P<pk>\d+)$',
        views.employee.show,
        name='employee.show'),
    url('^employee/delete/(?P<pk>\d+)$',
        views.employee.delete,
        name='employee.delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
