from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from ..models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

def upload(request,id):
    if ("b_cancel" in request.POST):
        return redirect('internal:serviceRequest.attachmentList', id)

    if ("b_upload" in request.POST):
        if (len(request.FILES) != 0):
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                if len(myfile.name) < 55:
                    #fs = FileSystemStorage()
                    sr_object = ServiceRequest.objects.get(pk=id)
                    description = str(request.POST.get('text_description'))
                    requestAttach= RequestAttachment.objects.create(request =sr_object,description = description,fileName="default")
                    fs = requestAttach.file
                    filename = fs.save(myfile.name, myfile)
                    requestAttach.fileName = requestAttach.file.name.split('/')[-1]
                    requestAttach.save()
                    messages.success(request, 'Se ha subido el archivo '+'"'+ requestAttach.fileName + '"' + ' exitosamente!')
                    return redirect('internal:serviceRequest.attachmentList', id)
                else:
                    messages.error(request,'El nombre del archivo que intentó subir no debe exceder los 50 caracteres!')
                    return redirect('internal:serviceRequest.upload', id)
        else:
            messages.error(request, 'Debe seleccionar un archivo!')
            return redirect('internal:serviceRequest.upload', id)
    else:
        return render(request, 'internal/serviceRequest/attachFile.html')
    #else:
    #    ra = RequestAttachment.objects.get(description = 'baka5')
    #    filename = ra.file.name.split('/')[-1]
    #    response = HttpResponse(ra.file, content_type='text/plain')
    #    response['Content-Disposition'] = 'attachment; filename=%s' % filename

     #   return response
 #       return render(request, 'internal/serviceRequest/attachFile.html')

 #   return redirect('internal:serviceRequest.attachmentList',id)
    #return render(request, 'internal/serviceRequest/attachFile.html')

def attachmentList(request,id):
    search = request.GET.get('search')
    sr_object = ServiceRequest.objects.get(pk=id)
    if search:
        requestAttachment_list = RequestAttachment.objects.filter(
            request=sr_object, fileName__icontains = search)
    else:
        requestAttachment_list = RequestAttachment.objects.filter(
            request=sr_object)

    paginator = Paginator(requestAttachment_list, 3)
    pageNumber = request.GET.get('page')
    try:
        requestAttachmentPageCurrent = paginator.page(pageNumber)
    except PageNotAnInteger:
        requestAttachmentPageCurrent = paginator.page(1)
    except EmptyPage:
        requestAttachmentPageCurrent = paginator.page(paginator.num_pages)

    context = {'serviceRequest': sr_object,
        'requestAttachment_list': requestAttachmentPageCurrent,
        'paginator': paginator,
    }
    template = 'internal/serviceRequest/files.html'
    return render(request, template, context)

def showAttachedFile(request,id):
    template = 'internal/serviceRequest/showAttachedFile.html'
    context = {
        'selected_file': RequestAttachment.objects.get(pk=id),
    }
    return render(request, template, context)

def deleteAttachedFile(request,id):
    requestAttached = RequestAttachment.objects.get(pk=id)
    idRequest = requestAttached.request.pk
    filename = requestAttached.fileName;
    requestAttached.file.delete()
    requestAttached.delete()
    messages.success(request, 'El archivo ' + '"' + filename + '"' +' se eliminó exitosamente!')
    return redirect('internal:serviceRequest.attachmentList',idRequest)

def downloadAttachedFile(request,id):
    requestAttachment = RequestAttachment.objects.get(pk=id)
    filename = requestAttachment.file.name.split('/')[-1]
    response = HttpResponse(requestAttachment.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

