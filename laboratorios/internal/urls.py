from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout_then_login
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #
    # Login
    #
    url(r'^login/?$',
        login,
        {'template_name': 'internal/login.html'},
        name='login'),

    url(r'^logout/?$',
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
    url('^servicerequest/reportGenerator/(?P<id>\d+)$',
        views.servicerequest.reportGenerator,
        name='servicerequest.reportGenerator'),
    url('^servicerequest/reportDetail/$',
        views.servicerequest.reportDetail,
        name='servicerequest.reportDetail'),
    url('^servicerequest/reportDetailPDF/$',
        views.servicerequest.reportDetailPDF,
        name='servicerequest.reportDetail.PDF'),
    url('^servicerequest/finalReport/(?P<id>\d+)$',
        views.servicerequest.finalReport,
        name='servicerequest.finalReport'),
    #
    # Employee
    #
    url('^employee/$',
        views.employee.index,
        name='employee.index'),
    url('^employee/create$',
        views.employee.create,
        name='employee.create'),
    url('^employee/(?P<pk>\d+)/edit/?$',
        views.employee.edit,
        name='employee.edit'),
    url('^employee/(?P<pk>\d+)$',
        views.employee.show,
        name='employee.show'),
    url('^employee/(?P<pk>\d+)/delete/?$',
        views.employee.delete,
        name='employee.delete'),
    #
    # Role
    #
    url('^role/?$',
        views.role.index,
        name='role.index'),
    url('^role/(?P<pk>\d+)/?$',
        views.role.show,
        name='role.show'),
    url('^role/create/?$',
        views.role.create,
        name='role.create'),
    url('^role/(?P<pk>\d+)/edit/?$',
        views.role.edit,
        name='role.edit'),
    url('^role/(?P<pk>\d+)/delete/?$',
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
    url('^inventoryOrder/create/(?P<pk>\d+)$',
        views.inventoryOrder.createPK,
        name='inventoryOrder.createPK'),
    url('^inventoryOrder/(?P<pk1>\d+)/edit/(?P<pk>\d+)$',
        views.inventoryOrder.edit,
        name='inventoryOrder.edit'),
    url('^inventoryOrder/(?P<pk>\d+)$',
        views.inventoryOrder.show,
        name='inventoryOrder.show'),
    url('^inventoryOrder/check/?$',
        views.inventoryOrder.check,
        name='inventoryOrder.check'),
    url('^inventoryOrder/(?P<pk>\d+)/approve/?$',
        views.inventoryOrder.approve,
        name='inventoryOrder.approve'),
    url('^inventoryOrder/(?P<pk>\d+)/reject/?$',
        views.inventoryOrder.reject,
        name='inventoryOrder.reject'),
    url('^inventoryOrder/(?P<pk>\d+)/delete/?$',
        views.inventoryOrder.delete,
        name='inventoryOrder.delete'),
    #
    # ServiceRequest
    #
    url('^servicerequest/create/(?P<pk>\d+)/?$',
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
    url('^servicerequest/(?P<pk>\d+)/add_sample/?$',
        views.servicerequest.add_sample,
        name='servicerequest.add_sample'),
    url('^servicerequest/(?P<pk_request>\d+)/edit_sample/(?P<pk_sample>\d+)/?$',
        views.servicerequest.edit_sample,
        name='servicerequest.edit_sample'),
    url('^servicerequest/(?P<pk_request>\d+)/delete_sample/(?P<pk_sample>\d+)/?$',
        views.servicerequest.delete_sample,
        name='servicerequest.delete_sample'),
    url('^servicerequest/create_client/?$',
        views.servicerequest.create_client,
        name='servicerequest.create_client'),
    url('^servicerequest/?$',
        views.servicerequest.index,
        name='servicerequest.index'),
    url('^servicerequest/(?P<pk>\d+)/?$',
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
    url('^servicerequest/(?P<pk>\d+)/approve/?$',
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
    url('^servicecontract/approve/(?P<pk>\d+)$',
        views.servicecontract.approve,
        name='servicecontract.approve'),
    url('^servicecontract/refuse/(?P<pk>\d+)$',
        views.servicecontract.refuse,
        name='servicecontract.refuse'),
    #
    # Laboratory
    #
    url('^laboratory/$',
        views.laboratory.index,
        name='laboratory.index'),
    url('^laboratory/create$',
        views.laboratory.create,
        name='laboratory.create'),
    url('^laboratory/(?P<pk>\d+)/edit/?$',
        views.laboratory.edit,
        name='laboratory.edit'),
    url('^laboratory/(?P<pk>\d+)/delete/?$',
        views.laboratory.delete,
        name='laboratory.delete'),
    url('^laboratory/(?P<pk>\d+)$',
        views.laboratory.show,
        name='laboratory.show'),
    url('^laboratory/(?P<pk>\d+)/services/$',
        views.laboratory.services_index,
        name='laboratory.services_index'),
    url('^laboratory/(?P<pk>\d+)/track_services/$',
        views.laboratory.track_services,
        name='laboratory.track_services'),

    #
    # sampleType
    #
    url('^sampleType/?$',
        views.sampleType.index,
        name='sampleType.index'),
    url('^sampleType/create/?$',
        views.sampleType.create,
        name='sampleType.create'),
    url('^sampleType/(?P<id>\d+)/edit/?$',
        views.sampleType.edit,
        name='sampleType.edit'),
    url('^sampleType/(?P<id>\d+)/delete/?$',
        views.sampleType.delete,
        name='sampleType.delete'),

    #
    #Supply
    #
    url('^supply/create$',
        views.supply.create,
        name='supply.create'),
    url('^supply/(?P<pk>\d+)$',
        views.supply.show,
        name='supply.show'),
    url('^supply/(?P<pk>\d+)/edit/?$',
        views.supply.edit,
        name='supply.edit'),
    url('^supply/?$',
        views.supply.index,
        name='supply.index'),
    url('^supply/(?P<pk>\d+)/delete/?$',
        views.supply.delete,
        name='supply.delete'),

    #
    #Equipment
    #
    url('^equipment/create$',
        views.equipment.create,
        name='equipment.create'),
    url('^equipment/(?P<pk>\d+)$',
        views.equipment.show,
        name='equipment.show'),
    url('^equipment/(?P<pk>\d+)/edit/?$',
        views.equipment.edit,
        name='equipment.edit'),
    url('^equipment/?$',
        views.equipment.index,
        name='equipment.index'),
    url('^equipment/(?P<pk>\d+)/delete/?$',
        views.equipment.delete,
        name='equipment.delete'),

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
    #

    # inventoryItem
    #
    url('^inventoryItem/?$',
        views.inventoryItem.index,
        name='inventoryItem.index'),
    url('^inventoryItem/(?P<pk>\d+)$',
        views.inventoryItem.show,
        name='inventoryItem.show'),
    url('^inventoryItem/(?P<pk>\d+)/delete/?$',
        views.inventoryItem.delete,
        name='inventoryItem.delete'),
    url('^inventoryItem/(?P<pk>\d+)/edit/?$',
        views.inventoryItem.edit,
        name='inventoryItem.edit'),

    # Parameter Fill
    #
    url('^fill_parameters/(?P<pk>\d+)$',
        views.parameterfill.fill_parameters,
        name='parameterfill.fill_parameters'),
    #
    # Reports
    #
    url('^reports/start$',
        views.reports.report_parameters,
        name='reports.start'),
    url('^reports/results/(?P<criteria_string>[\w\-]+)$',
        views.reports.processing_parameters,
        name='reports.results')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
