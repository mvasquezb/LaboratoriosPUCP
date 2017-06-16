from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout_then_login

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #
    # Login
    #
    url(r'^login$',
        login,
        {'template_name': 'internal/login.html'},
        name='login'),

    url(r'^logout$',
        logout_then_login,
        name='logout'),
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    #
    # ServiceRequest
    #
    url('^servicerequest/attachFile/(?P<id>\d+)$',
        views.servicerequest.upload,
        name='serviceRequest.upload'),
    url('^servicerequest/files/(?P<id>\d+)$',
        views.servicerequest.attachmentList,
        name='serviceRequest.attachmentList'),
    url('^servicerequest/attachedFileShow/(?P<id>\d+)$',
        views.servicerequest.showAttachedFile,
        name='serviceRequest.showAttachedFile'),
    url('^servicerequest/deleteAttachedFile/(?P<id>\d+)$',
        views.servicerequest.deleteAttachedFile,
        name='serviceRequest.deleteAttachedFile'),
    url('^servicerequest/downloadAttachedFile/(?P<id>\d+)$',
        views.servicerequest.downloadAttachedFile,
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
    #
    # Role
    #
    url('^role/$',
        views.role.index,
        name='role.index'),
    url('^role/show/(?P<pk>\d+)$',
        views.role.show,
        name='role.show'),
    url('^role/create$',
        views.role.create,
        name='role.create'),
    url('^role/edit/(?P<pk>\d+)$',
        views.role.edit,
        name='role.edit'),
    url('^role/delete/(?P<pk>\d+)$',
        views.role.delete,
        name='role.delete'),
    #
    # RequestStorage
    #
    url('^inventoryOrder/?$',
        views.inventoryOrder.index,
        name='inventoryOrder.index'),
    url('^inventoryOrder/create/?$',
        views.inventoryOrder.create,
        name='inventoryOrder.create'),
    url('^inventoryOrder/edit/(?P<pk>\d+)$',
        views.inventoryOrder.edit,
        name='inventoryOrder.edit'),
    url('^inventoryOrder/show/(?P<pk>\d+)$',
        views.inventoryOrder.show,
        name='inventoryOrder.show'),
    url('^inventoryOrder/check/?$',
        views.inventoryOrder.check,
        name='inventoryOrder.check'),
    url('^inventoryOrder/approve/(?P<pk>\d+)$',
        views.inventoryOrder.approve,
        name='inventoryOrder.approve'),
    url('^inventoryOrder/reject/(?P<pk>\d+)$',
        views.inventoryOrder.reject,
        name='inventoryOrder.reject'),
    url('^inventoryOrder/delete/(?P<pk>\d+)$',
        views.inventoryOrder.delete,
        name='inventoryOrder.delete'),
    #
    # ServiceRequest
    #
    url('^servicerequest/create/(?P<pk>\d+)$',
        views.servicerequest.create,
        name='servicerequest.create'),
    url('^servicerequest/(?P<pk>\d+)/delete/?$',
        views.servicerequest.delete,
        name='servicerequest.delete'),
    url('^servicerequest/select_client/?$',
        views.servicerequest.select_client,
        name='servicerequest.select_client'),
    url('^servicerequest/(?P<pk>\d+)/edit/?$',
        views.servicerequest.edit,
        name='servicerequest.edit'),
    url('^servicerequest/add_sample/(?P<pk>\d+)$',
        views.servicerequest.add_sample,
        name='servicerequest.add_sample'),
    url('^servicerequest/edit_sample/(?P<pk_request>\d+)/(?P<pk_sample>\d+)$',
        views.servicerequest.edit_sample,
        name='servicerequest.edit_sample'),
    url('^servicerequest/delete_sample/(?P<pk_request>\d+)/(?P<pk_sample>\d+)$',
        views.servicerequest.delete_sample,
        name='servicerequest.delete_sample'),
    url('^servicerequest/create_client$',
        views.servicerequest.create_client,
        name='servicerequest.create_client'),
    url('^servicerequest$',
        views.servicerequest.index,
        name='servicerequest.index'),
    url('^servicerequest/(?P<request_id>\d+)/?$',
        views.servicerequest.show,
        name='servicerequest.show'),
    url('^servicerequest/(?P<request_id>\d+)/quotation/?$',
        views.servicerequest.quotation,
        name='servicerequest.quotation'),
    url('^servicerequest/(?P<request_id>\d+)/assign_employee/(?P<sample_id>\d+)/?$',
        views.servicerequest.assign_employee,
        name='servicerequest.assign_employee'),
    url('^servicerequest/view_workload_per_request/?$',
        views.servicerequest.workload_view_per_request,
        name='servicerequest.workload_view_per_request'),
    url('^servicerequest/approve/(?P<pk>\d+)$',
        views.servicerequest.approve,
        name='servicerequest.approve'),

    #
    # ServiceContract
    #
    url('^servicecontract/?$',
        views.servicecontract.index,
        name='servicecontract.index'),
    url('^servicecontract/(?P<pk>\d+)/edit/?$',
        views.servicecontract.edit,
        name='servicecontract.edit'),
    url('^servicecontract/(?P<service_id>\d+)/?$',
        views.servicecontract.show,
        name='servicecontract.show'),
    url('^servicecontract/(?P<pk>\d+)/delete/?$',
        views.servicecontract.delete,
        name='servicecontract.delete'),
    #
    # Laboratory
    #
    url('^laboratory/$',
        views.laboratory.index,
        name='laboratory.index'),
    url('^laboratory/create$',
        views.laboratory.create,
        name='laboratory.create'),
    url('^laboratory/edit/(?P<pk>\d+)$',
        views.laboratory.edit,
        name='laboratory.edit'),
    url('^laboratory/delete/(?P<pk>\d+)$',
        views.laboratory.delete,
        name='laboratory.delete'),
    url('^laboratory/show/(?P<pk>\d+)$',
        views.laboratory.show,
        name='laboratory.show'),
    #
    # sampleType
    #
    url('^sampleType/?$',
        views.sampleType.index,
        name='sampleType.index'),
    url('^sampleType/create/?$',
        views.sampleType.create,
        name='sampleType.create'),
    url('^sampleType/edit/(?P<id>\d+)/$',
        views.sampleType.edit,
        name='sampleType.edit'),
    url('^sampleType/delete/(?P<id>\d+)/?$',
        views.sampleType.delete,
        name='sampleType.delete'),
    #
    # Essay
    #
    url('^essay/create$',
        views.essay.create,
        name='essay.create'),
    url('^essay/(?P<pk>\d+)$',
        views.essay.show,
        name='essay.show'),
    url('^essay/(?P<pk>\d+)/edit/?$',
        views.essay.edit,
        name='essay.edit'),
    url('^essay/?$',
        views.essay.index,
        name='essay.index'),
    url('^essay/(?P<pk>\d+)/delete/?$',
        views.essay.delete,
        name='essay.delete'),
    #
    # EssayMethods
    #
    url('^essaymethod/create/?$',
        views.essaymethod.create,
        name='essaymethod.create'),
    url('^essaymethod/(?P<pk>\d+)$',
        views.essaymethod.show,
        name='essaymethod.show'),
    url('^essaymethod/(?P<pk>\d+)/edit/?$',
        views.essaymethod.edit,
        name='essaymethod.edit'),
    url('^essaymethod/?$',
        views.essaymethod.index,
        name='essaymethod.index'),
    url('^essaymethod/(?P<pk>\d+)/delete/?$',
        views.essaymethod.delete,
        name='essaymethod.delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
