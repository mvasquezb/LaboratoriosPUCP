from django.conf.urls import url
from . import views

urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    url('^laboratory/?$',
        views.labs.index,
        name='labs.index'),
    url('^laboratory/create/?$',
        views.labs.create,
        name='labs.create'),
]
