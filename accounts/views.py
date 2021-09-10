import django
from ppid.models import Dinas
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator

# membuat akses login dan logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from django.urls import reverse_lazy

#reset password
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .models import *
from .forms import *
from ppid import forms 
import logging
import os
logger = logging.getLogger(__name__)

# Create your views here.
class MyPasswordChangeView(PasswordChangeView):
    template_name = "account/password-change.html"
    success_url = reverse_lazy('dashboard')

def get_siteID(request):
    siteID = Site.objects.filter(domain=request.get_host()).values_list('id',
        flat=True)
    if siteID.count() == 0:
        return HttpResponse(
            "domain '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
             % (request.get_host(), '/admin'))
    siteID = siteID[0]
    return siteID

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, "Username atau Password Salah")
    
    context = {

    }
    return render(request, 'registration/login.html', context)

@login_required(login_url="/accounts/login/")
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url="/accounts/login/")
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = { 
        'form':form
    }
    return render(request, 'registration/register.html', context)

@login_required(login_url="/accounts/login/")
def dashboard(request):
    siteID = get_siteID(request)
    show = models.Dinas.objects.filter(site_id = siteID, user_id = request.user.id)
    
    qry = models.Dinas.objects.filter(user_id = request.user.id, site_id = siteID).values_list("id", flat=True)

    logger.error(qry)
    if qry.count() == 0:
        return HttpResponse(
            "username '%s' tidak di temukan di domain '%s'. <a href='%s'>Logout</a>"
             % (request.user.username, request.get_host(), '/logout'))

    # context['instansi'] = instansi.objects.filter(site_id=siteID)[:1]

    dip = models.Data.objects.filter(dinas_id=qry[0])
    dip_count = dip.count()

    dip_1 = models.Data.objects.filter(type_data = '2', dinas_id=qry[0])
    dip1_count = dip_1.count()

    dip_2 = models.Data.objects.filter(type_data = '3', dinas_id=qry[0])
    dip2_count = dip_2.count()

    dip_3 = models.Data.objects.filter(type_data = '4', dinas_id=qry[0])
    dip3_count = dip_3.count()

    context = {
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count
    }
    return render(request, 'account/index.html', context)

@login_required(login_url="/accounts/login/")
def data_ppid(request):
    siteID = get_siteID(request)

    show = models.Dinas.objects.filter(site_id = siteID, user_id = request.user.id)

    #query set mengambil id dinas
    qry = models.Dinas.objects.filter(user_id = request.user.id, site_id = siteID).values_list("id", flat=True)
    # dinas_id = qry[0]

    logger.error(qry)
    if qry.count() == 0:
        return HttpResponse(
            "username '%s' tidak di temukan di domain '%s'. <a href='%s'>Logout</a>"
             % (request.user.username, request.get_host(), '/logout'))

    data = models.Data.objects.filter(dinas_id=qry[0])

    context = {
        'data':data,
        'show':show,
    }
    return render(request, 'account/data_ppid.html', context)

@login_required(login_url="/accounts/login/")
def create_data(request):
    siteID = get_siteID(request)

    show = models.Dinas.objects.filter(site_id = siteID, user_id = request.user.id)

    form = DataForm()

    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            
            qry = models.Dinas.objects.filter(user_id = request.user.id, site_id = siteID).values_list("id", flat=True)
            logger.error(qry)
            if qry.count() == 0:
                return HttpResponse(
                    "username '%s' tidak di temukan di domain '%s'. <a href='%s'>Logout</a>"
                    % (request.user.username, request.get_host(), '/logout'))

            obj.dinas_id = qry[0]
            obj.user_id = request.user.id
            obj.site_id = siteID

            obj.save()
            
            return redirect('datappid')

    context = {
        'form':form,
        'show':show
    }
    return render(request, "account/create_data.html", context)

@login_required(login_url="/accounts/login/")
def update_data(request, pk):
    siteID = get_siteID(request)
    show = models.Dinas.objects.filter(site_id = siteID, user_id = request.user.id)

    data = models.Data.objects.get(id=pk,  site_id = siteID)
    form = DataFormUpdate(instance = data)

    if request.method == 'POST':
        form = DataFormUpdate(request.POST, request.FILES, instance = data)
        if len(request.FILES) != 0:
            if len(data.file) > 0:
                os.remove(data.file.path)
                if form.is_valid():
                    obj = form.save(commit=False)
                    
                    qry = models.Dinas.objects.filter(user_id = request.user.id, site_id = siteID).values_list("id", flat=True)

                    logger.error(qry)
                    if qry.count() == 0:
                        return HttpResponse(
                            "username '%s' tidak di temukan di domain '%s'. <a href='%s'>Logout</a>"
                            % (request.user.username, request.get_host(), '/logout'))


                    obj.dinas_id = qry[0]
                    obj.site_id = siteID
                    obj.user_id = request.user.id
                    obj.save()
                    return redirect('datappid')
                    
        if form.is_valid():
            obj = form.save(commit=False)
            
            qry = models.Dinas.objects.filter(user_id = request.user.id, site_id = siteID).values_list("id", flat=True)
            logger.error(qry)
            if qry.count() == 0:
                return HttpResponse(
                    "username '%s' tidak di temukan di domain '%s'. <a href='%s'>Logout</a>"
                    % (request.user.username, request.get_host(), '/logout'))

            obj.dinas_id = qry[0]
            obj.site_id = siteID

            obj.user_id = request.user.id
            obj.save()
            return redirect('datappid')
    context = {
        'form':form,
        'show':show,
    }
    return render(request, 'account/edit_data.html', context)

@login_required(login_url="/accounts/login/")
def delete_data(request, pk):
    siteID = get_siteID(request)
    if request.method == "POST":
        data = models.Data.objects.get(id=pk, site_id = siteID)
        data.delete()
    return redirect('datappid')


@login_required(login_url="/accounts/login/")
def profile(request, pk):
    siteID = get_siteID(request)

    show = models.Dinas.objects.filter(site_id = siteID, user_id = request.user.id)

    data = models.Dinas.objects.get(id=pk, site_id = siteID, user_id = request.user.id)
    form = ProfileForm(instance = data)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = data)
        if form.is_valid():
            obj = form.save(commit=False)
            
            qry = models.Dinas.objects.filter(user_id = request.user.id).values_list("id", flat=True)

            obj.dinas_id = qry[0]
            obj.site_id = siteID

            obj.user_id = request.user.id
            obj.save()

    context = {
        'form':form,
        'show':show
    }

    return render(request, 'account/profile.html', context)

@login_required(login_url="/accounts/login/")
def permohonan_data(request):
    siteID = get_siteID(request)

    #query set mengambil id dinas
    show = models.Dinas.objects.filter(site_id = siteID, user_id = request.user.id)
    
    qry = models.Dinas.objects.filter(user_id = request.user.id).values_list("id", flat=True)
    logger.error(qry)
    if qry.count() == 0:
        return HttpResponse(
            "username '%s' tidak di temukan di domain '%s'. <a href='%s'>Logout</a>"
            % (request.user.username, request.get_host(), '/logout'))

    data = models.Form_information.objects.filter(dinas_id = qry[0])

    context = {
        'data':data,
        'show':show,
    }
    return render(request, 'account/permohonan.html', context)

@login_required(login_url="/accounts/login/")
def proses_permohonan(request,pk):
    siteID = get_siteID(request)
    show = models.Form_information.objects.filter(id=pk, site_id = siteID)
    permohonan = models.Form_information.objects.get(id=pk, site_id = siteID)
    form = RequestForm(instance = permohonan)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance = permohonan)
        if form.is_valid():
            obj = form.save(commit=False)
            
            qry = models.Dinas.objects.filter(user_id = request.user.id).values_list("id", flat=True)
            logger.error(qry)
            if qry.count() == 0:
                return HttpResponse(
                    "username '%s' tidak di temukan di domain '%s'. <a href='%s'>Logout</a>"
                    % (request.user.username, request.get_host(), '/logout'))

            obj.dinas_id = qry[0]
            obj.site_id = siteID

            obj.user_id = request.user.id
            obj.save()
            return redirect('permohonan')
    context = {
        'show':show,
        'form':form,
    }
    return render(request, 'account/detail_permohonan.html', context)

@login_required(login_url="/accounts/login/")
def delete_permohonan(request, pk):
    if request.method == "POST":
        data = models.Form_information.objects.get(id=pk)
        data.delete()
    return redirect('permohonan')



