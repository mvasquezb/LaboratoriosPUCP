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
    # Essay Template
    #
    url('^essayTemplate/?$',
        views.essayTemplate.index,
        name='essayTemplate.index'),
    url('^essayTemplate/create/?$',
        views.essayTemplate.create,
        name='essayTemplate.create'),
    url('^essayTemplate/edit/(?P<id>\d+)/$',
        views.essayTemplate.edit,
        name='essayTemplate.edit'),
    url('^essayTemplate/delete/?$',
        views.essayTemplate.delete,
        name='essayTemplate.delete'),
    #
    # Test Template
    #
    url('^testTemplate/?$',
        views.testTemplate.index,
        name='testTemplate.index'),
    url('^testTemplate/create/?$',
        views.testTemplate.create,
        name='testTemplate.create'),
    url('^testTemplate/edit/(?P<id>\d+)/$',
        views.testTemplate.edit,
        name='testTemplate.edit'),
    url('^testTemplate/delete/?$',
        views.testTemplate.delete,
        name='testTemplate.delete'),
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
    url('^servicerequest/create$',
        views.servicerequest.create,
        name='servicerequest.create'),
    url('^servicerequest/store$',
        views.servicerequest.store,
        name='servicerequest.store'),
    url('^servicerequest$',
        views.servicerequest.index,
        name='servicerequest.index'),
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
    url('^employee/delete/(?P<pk>\d+)$',
        views.employee.delete,
        name='employee.delete'),
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
    # Access
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
    # Client
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
]
