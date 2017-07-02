from .main import *
from .client import *
from .employee import *
from .laboratory import *
from .essaymethod import *
from .role import *
from .servicerequest import *
from .inventoryOrder import *
from .servicecontract import *
from .sampleType import *
from .essay import *
from .inventoryItem import *
from .parameterfill import *
from .reports import *
from .supply import *
from .equipment import *
from .externalprovider import *
from .inventory import *

from django.shortcuts import render


def not_found_handler(request):
    return render(request, '404.html')


def server_error_handler(request):
    return render(request, '500.html')
