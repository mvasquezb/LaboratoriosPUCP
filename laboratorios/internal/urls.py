from django.conf.urls import url

from . import views


urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    #
    # Laboratory
    #
    url('^laboratory/?$',
        views.laboratory.index,
        name='laboratory.index'),
    url('^laboratory/create/?$',
        views.laboratory.create,
        name='laboratory.create'),
    url('^laboratory/delete/?$',
        views.laboratory.delete,
        name='laboratory.delete'),
    url('^laboratory/edit/(?P<id_lab>\d+)/$',
        views.laboratory.edit,
        name='laboratory.edit'),
    url('^laboratory/assignMonitor/(?P<id>\d+)/$',
        views.laboratory.assignMonitor,
        name='laboratory.assignMonitor'),
    #
    # LaboratoryType
    #
    url('^laboratoryType/?$',
         views.laboratoryType.index,
         name='laboratoryType.index'),
    url('^laboratoryType/create/?$',
         views.laboratoryType.create,
         name='laboratoryType.create'),
    url('^laboratoryType/edit/(?P<id>\d+)/$',
         views.laboratoryType.edit,
         name='laboratoryType.edit'),
    url('^laboratoryType/edit2/?$',
        views.laboratoryType.edit2,
        name='laboratoryType.edit2'),
    url('^laboratoryType/delete/?$',
         views.laboratoryType.delete,
         name='laboratoryType.delete'),
    #
    # Essay Type
    #
    url('^essayType/?$',
        views.essayType.index,
        name='essayType.index'),
    url('^essayType/create?$',
        views.essayType.create,
        name='essayType.create'),
    url('^essayType/edit/(?P<id>\d+)/$',
        views.essayType.edit,
        name='essayType.edit'),
    url('^essayType/delete/?$',
        views.essayType.delete,
        name='essayType.delete'),
    #
    #Test Type
    #
    url('^testType/?$',
        views.testType.index,
        name='testType.index'),
    url('^testType/create?$',
        views.testType.create,
        name='testType.create'),
    url('^testType/edit/(?P<id>\d+)/$',
        views.testType.edit,
        name='testType.edit'),
    url('^testType/delete/?$',
        views.testType.delete,
        name='testType.delete'),
    #
    # Role
    #
    url('^role/$',
        views.role.index,
        name='role.index'),
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
    # ServiceRequest
    #
    url('^servicerequest/create/(?P<pk>\d+)$',
        views.servicerequest.create,
        name='servicerequest.create'),
    url('^servicerequest/select_client$',
        views.servicerequest.select_client,
        name='servicerequest.select_client'),
    url('^servicerequest/create_client$',
        views.servicerequest.create_client,
        name='servicerequest.create_client'),
    url('^servicerequest/store$',
        views.servicerequest.store,
        name='servicerequest.store'),
    url('^servicerequest$',
        views.servicerequest.index,
        name='servicerequest.index'),
    #
    # User
    #
    url('^user/$',
        views.user.index,
        name='user.index'),
    url('^user/create$',
        views.user.create,
        name='user.create'),
    url('^user/edit/(?P<pk>\d+)$',
        views.user.edit,
        name='user.edit'),
    url('^user/delete/(?P<pk>\d+)$',
        views.user.delete,
        name='user.delete'),
    #
    # Test
    #
    url('^test/create/$',
        views.test.TestParameterCreate.as_view(),
        name='test.create'),
    url('^test/store$',
        views.test.store,
        name='test.store'),
    url('^test/$',
        views.test.index,
        name='test.index'),
    url('^test/edit/(?P<pk>\d+)$',
        views.test.TestParameterUpdate.as_view(),
        name='test.edit'),
    url('^test/delete/(?P<pk>\d+)$',
        views.test.TestDelete.as_view(),
        name='test.delete'),
    #
    #Access
    #
    url('^access$',
        views.access.index,
        name='access.index'),
    url('^access/create$',
        views.access.create,
        name='access.create'),
    url('^access/edit/(?P<pk>\d+)$',
        views.access.edit,
        name='access.edit'),
    url('^access/delete/(?P<pk>\d+)$',
        views.access.delete,
        name='access.delete'),


    #
    #Client
    #
    url('^client/$',
        views.client.index,
        name='client.index'),
    url('^client/create$',
        views.client.create,
        name='client.create'),
    url('^client/edit/(?P<pk>\d+)$',
        views.client.edit,
        name='client.edit'),
    url('^client/delete/(?P<pk>\d+)$',
        views.client.delete,
        name='client.delete'),


    #
    # EssayTemplate
    #
    url('^essayTemplate/$',
        views.essayTemplate.index,
        name='essayTemplate.index'),
    url('^essayTemplate/create$',
        views.essayTemplate.create,
        name='essayTemplate.create'),
    url('^essayTemplate/edit/(?P<pk>\d+)$',
        views.essayTemplate.edit,
        name='essayTemplate.edit'),
    url('^essayTemplate/delete/(?P<pk>\d+)$',
        views.essayTemplate.delete,
        name='essayTemplate.delete'),
    #
    # Service
    #
    url('^service/index/?$',
        views.service.index,
        name='service.index'),
    url('^service/(?P<pk>\d+)/?$',
        views.service.show,
        name='service.show'),
    #
    # EssayFill
    #
    url('^service/(?P<service_id>\d+)/essay/?$',
        views.essayfill.index,
        name='essayfill.index'),
    url('^service/(?P<service_id>\d+)/essay/(?P<essay_id>\d+)/?$',
        views.essayfill.show,
        name='essayfill.show'),
    #
    # TestFill
    #
    url('^service/(?P<service_id>\d+)/essay/(?P<essay_id>\d+)/test/?$',
        views.testfill.index,
        name='testfill.index'),
    url('^service/(?P<service_id>\d+)/essay/(?P<essay_id>\d+)/test/(?P<test_id>\d+)/?$',
        views.testfill.show,
        name='testfill.show'),
    url('^service/(?P<service_id>\d+)/essay/(?P<essay_id>\d+)/test/(?P<test_id>\d+)/update/?$',
        views.testfill.update,
        name='testfill.update'),
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
    url('^sampleType/delete/?$',
         views.sampleType.delete,
         name='sampleType.delete'),
]
