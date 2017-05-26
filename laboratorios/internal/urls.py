from django.conf.urls import url

from . import views



urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    url('^request/create$', views.request.create, name='request.create'),
    url('^request/store$', views.request.store, name='request.store'),
    url('^request$', views.request.index, name='request.index'),

]
