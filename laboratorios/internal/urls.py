from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    #
    # Login
    #
    url(r'^login$',
        login,
        {'template_name' : 'internal/login.html'},
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

]
