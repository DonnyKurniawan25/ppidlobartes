from django.http import request
from django.shortcuts import render, redirect, HttpResponse
from django.template import context
from django.template.context import Context
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site

from django.core.paginator import EmptyPage, Paginator

#untuk membuat query
from django.db.models import Count, OuterRef, Subquery

def get_siteID(request):
    siteID = Site.objects.filter(domain=request.get_host()).values_list('id',
        flat=True)
    if siteID.count() == 0:
        return HttpResponse(
            "domain '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
             % (request.get_host(), '/admin'))
    siteID = siteID[0]
    return siteID

def error_404_view(request, exception):
    return render(request, 'ppid/404.html')

# Create your views here.
def data_type(request):
    return render(request, 'ppid/data_type.html')
    
class DIPdetail(DetailView):
    model = Data
    template_name = 'ppid/detail-dip.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context1 = self.get_context_data(object = self.object)
        ip = get_client_ip(self.request)
        print(ip)
        if IpModel.objects.filter(ip=ip).exists():
            print("Ip already")
            post_id = request.GET.get('post-id')
            print(post_id)
            post = Data.objects.get(pk=post_id)
            post.read.add(IpModel.objects.get(ip=ip))
        else:
            IpModel.objects.create(ip=ip)
            post_id = request.GET.get('post_id')
            post = Data.objects.get(pk=post_id)
            post.read.add(IpModel.objects.get(ip=ip))
        
        return self.render_to_response(context1)

    def get_context_data(self, **kwargs):
        
        subQry = Subquery(Data.objects.filter(dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
        opd_count = Dinas.objects.all().annotate(jumlah=subQry)
        dip = Data.objects.all()
        dip_count = dip.count()
        dip1_count = Data.objects.filter(type_data = '2').count()
        dip2_count = Data.objects.filter(type_data = '3').count()
        dip3_count = Data.objects.filter(type_data = '4').count()

        context =  super().get_context_data(**kwargs)

        context['opd_count'] = opd_count
        context['dip_count'] = dip_count
        context['dip1_count'] = dip1_count
        context['dip2_count'] = dip2_count
        context['dip3_count'] = dip3_count
        return context

class DIPdownload(DetailView):
    model = Data
    template_name = 'ppid/download-file.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object = self.object)
        ip =get_client_ip(self.request)
        print(ip)
        if IpModel.objects.filter(ip=ip).exists():
            print("Ip already")
            post_id = request.GET.get('post-id')
            print(post_id)
            post = Data.objects.get(pk=post_id)
            post.download.add(IpModel.objects.get(ip=ip))
        else:
            IpModel.objects.create(ip=ip)
            post_id = request.GET.get('post_id')
            post = Data.objects.get(pk=post_id)
            post.download.add(IpModel.objects.get(ip=ip))
        
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):

        subQry = Subquery(Data.objects.filter(dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
        opd_count = Dinas.objects.all().annotate(jumlah=subQry)
        dip = Data.objects.all()
        dip_count = dip.count()

        dip1_count = Data.objects.filter(type_data = '2').count()
        dip2_count = Data.objects.filter(type_data = '3').count()
        dip3_count = Data.objects.filter(type_data = '4').count()

        context =  super().get_context_data(**kwargs)

        context['opd_count'] = opd_count
        context['dip_count'] = dip_count
        context['dip1_count'] = dip1_count
        context['dip2_count'] = dip2_count
        context['dip3_count'] = dip3_count
        return context
     
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    #mengambil fungsi site
    siteID = get_siteID(request)

    # data = Data.objects.exclude(site_id=siteID)
    site = Site.objects.filter(id = siteID)

    site1 = Site.objects.filter(id = '1')
    site2 = Site.objects.filter(id = '2')
    site3 = Site.objects.filter(id = '3')
    site4 = Site.objects.filter(id = '4')
    site5 = Site.objects.filter(id = '5')

    show = Data.objects.filter(site_id = '1').order_by("-id")[:20]
    showsekolah = Data.objects.filter(site_id = '2').order_by("-id")[:20]
    showpuskesmas = Data.objects.filter(site_id = '3').order_by("-id")[:20]
    showdesa = Data.objects.filter(site_id = '4').order_by("-id")[:20]
    showkecamatan = Data.objects.filter(site_id = '5').order_by("-id")[:20]

    dip_count = Data.objects.filter(site_id = siteID).count()
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    #slider
    slide = slideshow.objects.filter(site_id = siteID)

    context = {
        # 'data':data,
        'slide':slide,
        'site':site,
        'site1':site1,
        'site2':site2,
        'site3':site3,
        'site4':site4,
        'site5':site5,
        'show':show,
        'showkecamatan':showkecamatan,
        'showsekolah':showsekolah,
        'showdesa':showdesa,
        'showpuskesmas':showpuskesmas,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
    }
    return render(request, 'ppid/index.html', context)

def data_opd(request, pk):
    siteID = get_siteID(request)
    site = Site.objects.filter(id = siteID)
    
    #Filter Data Berdasar dinas
    dataopd = Data.objects.filter(dinas_id = pk, site_id = siteID )

    #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    dip_show = Dinas.objects.filter(id = pk, site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'dataopd':dataopd,
        'dip':dip,
        'dip_show':dip_show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/data_opd.html', context)

def addreas(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)

    show = Data.objects.filter(title__icontains='alamat', site_id = siteID )
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/addreas.html', context)

def visimisi(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='misi',site_id = siteID )
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/visimisi.html', context)

def structure(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='struktur', site_id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/structure.html', context)

def tupoksi(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='tupoksi', site_id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/tupoksi.html',context)

def profile(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='profil', site_id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/profile.html', context)

def opd(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='profil', site_id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/opd.html', context)

def profileppid(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)


    context = {
        'site':site,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request,'ppid/profile-ppid.html', context) 

def visimisippid(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/visimisi-ppid.html', context)

def structureppid(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/structure-ppid.html', context)

def authorityppid(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/authority-ppid.html',context)

def noticeppid(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/notice-ppid.html', context)

def complaint(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/complaint.html', context)

def contact(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/contact.html', context)

def DIP(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()

    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)
    
    p = Paginator(dip, 10)

    page_num = request.GET.get('page',1)

    try:
        dip = p.page(page_num)
    except EmptyPage:
        dip = p.page(1)


    context = {
        'site':site,
        'dip':dip,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd':opd,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/DIP.html', context)

def mekanisme(request):
    return render(request, 'ppid/mekanisme.html')

    site = Site.objects.filter(id = siteID)
def disputeresolution(request):
    return render(request, 'ppid/dispute-resolution.html')

    site = Site.objects.filter(id = siteID)
def search(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)
    
    if request.method == "POST":
        searched = request.POST['searched']

        datas = Data.objects.filter(title__icontains=searched, site_id = siteID)

        return render(request, 'ppid/search.html',{'searched':searched, 'datas':datas,'dip':dip,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,})
    else:
        return render(request, 'ppid/search.html')

def berkala(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
     #Filter Data Berdasar dinas
    dataopd = Data.objects.filter(type_data = '2', site_id = siteID)

    #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(dataopd, 10)

    page_num = request.GET.get('page',1)

    try:
        dataopd = p.page(page_num)
    except EmptyPage:
        dataopd = p.page(1)

    context = {
        'site':site,
        'dataopd':dataopd,
        'dataopd':dataopd,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/berkala.html', context)

def sertamerta(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
     #Filter Data Berdasar dinas
    dataopd = Data.objects.filter(type_data = '3', site_id = siteID)

    #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(dataopd, 10)

    page_num = request.GET.get('page',1)

    try:
        dataopd = p.page(page_num)
    except EmptyPage:
        dataopd = p.page(1)

    context = {
        'site':site,
        'dataopd':dataopd,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/sertamerta.html', context)

def setiapsaat(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
     #Filter Data Berdasar dinas
    dataopd = Data.objects.filter(type_data = '4', site_id = siteID)

    #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(dataopd, 10)

    page_num = request.GET.get('page',1)

    try:
        dataopd = p.page(page_num)
    except EmptyPage:
        dataopd = p.page(1)

    context = {
        'site':site,
        'dataopd':dataopd,
        'dataopd':dataopd,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/setiapsaat.html', context)

def rulespermohonan(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='tata cara', site_id = siteID)

    #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/rulespermohonan.html', context)
    
def standarharga(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
   #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/standarharga.html', context)

def permintaandata(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Form_information.objects.filter(site_id = siteID)

    #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/permintaandata.html', context)

def form_request(request):
    siteID = get_siteID(request)
    site = Site.objects.filter(id = siteID)
    show = Form_information.objects.filter(site_id = siteID)

     #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    form = RequestForm()
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('formrequest')

    context = {
        'site':site,
        'form':form,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/form_request.html', context)
    
def rulessengketa(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/rulessengketa.html', context)

def pengajuankeberatan(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='keberatan', site_id = siteID )
    #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/pengajuankeberatan.html', context)

def laporan(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='laporan', site_id = siteID) 
     #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
   
    return render(request, 'ppid/laporan.html', context)

def sop(request):
    siteID = get_siteID(request)
    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='sop', site_id = siteID ) 
    
     #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/sop.html', context)

def regulasi(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='undang',site_id = siteID) 
    
     #Count data
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/regulasi.html', context)

def kegiatan(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='kegiatan', site_id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/kegiatan.html', context)

def agenda(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='agenda', site_id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/agenda.html', context)

def hakmasyarakat(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='masyarakat', site_id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/hakmasyarakat.html', context)

def akuntabilitas(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = Data.objects.filter(title__icontains='akuntabilitas', site_id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)
    p = Paginator(show, 10)

    page_num = request.GET.get('page',1)

    try:
        show = p.page(page_num)
    except EmptyPage:
        show = p.page(1)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/akuntabilitas.html', context)

def form_sengketa(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    show = sengketa.objects.filter(site_id = siteID)

    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    form = SengketaForm()
    if request.method == 'POST':
        form = SengketaForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.site_id = siteID
            obj.save()
            return redirect('formsengketa')

    context = {
        'site':site,
        'form':form,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/form_sengketa.html', context)

def jumlah_permohonan_layanan(request):
    siteID = get_siteID(request)
    site = Site.objects.filter(id = siteID)
    show = layanan.objects.filter(site_id = siteID, type_layanan = '1')

    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/jumlah_permohonan_layanan.html', context)

def waktu_pemenuhan_layanan(request):
    siteID = get_siteID(request)
    site = Site.objects.filter(id = siteID)
    show = layanan.objects.filter(site_id = siteID, type_layanan = '2')

    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/waktu_pemenuhan_layanan.html', context)

def layanan_dikabulkan(request):
    siteID = get_siteID(request)
    site = Site.objects.filter(id = siteID)
    show = layanan.objects.filter(site_id = siteID, type_layanan = '3')

    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/layanan_dikabulkan.html', context)

def layanan_ditolak(request):
    siteID = get_siteID(request)
    site = Site.objects.filter(id = siteID)
    show = layanan.objects.filter(site_id = siteID, type_layanan = '4')

    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'show':show,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/layanan_ditolak.html', context)

def rancangan(request):
    siteID = get_siteID(request)

    site = Site.objects.filter(id = siteID)
    dip = Data.objects.filter(site_id = siteID)
    dip_count = dip.count()
 
    dip1_count = Data.objects.filter(type_data = '2', site_id = siteID).count()
    dip2_count = Data.objects.filter(type_data = '3', site_id = siteID).count()
    dip3_count = Data.objects.filter(type_data = '4', site_id = siteID).count()

    subQry = Subquery(Data.objects.filter(site_id = siteID, dinas_id = OuterRef('id')).values('dinas_id').annotate(jml=Count('id')).values('jml'))
    opd_count = Dinas.objects.filter(site_id = siteID).annotate(jumlah=subQry)

    context = {
        'site':site,
        'dip_count':dip_count,
        'dip3_count':dip3_count,
        'dip2_count':dip2_count,
        'dip1_count':dip1_count,
        'opd_count':opd_count,
    }
    return render(request, 'ppid/rancangan.html', context)
