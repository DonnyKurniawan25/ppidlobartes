from django.db import models
#from django.db.models.deletion import CASCADE, SET_NULL
#from django.db.models.fields import CharField, NullBooleanField
#from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.text import slugify
import os


# Create your models here.

class Dinas(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="dinas")
    title = models.CharField(max_length=225, null=True, blank=True)
    shortness = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    telp = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class Type_data(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=225, null=True, blank=True)
    
    def __str__(self):
        return self.type

class IpModel(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.SET_NULL)
    ip = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.ip

class Data(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=125, blank=True, null=True)
    title = models.CharField(max_length=225, null=True, blank=True)
    slug = models.SlugField(max_length=255, default='', unique=True, blank=True, null=True)
    responsible = models.CharField(max_length=225, null=True, blank=True)
    dinas = models.ForeignKey(Dinas, on_delete=models.SET_NULL, null=True, blank=True) 
    information = models.CharField(max_length=225, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    date_a = models.DateField(null=True, blank=True)
    date_b = models.DateField(null=True, blank=True)
    file = models.FileField()
    read = models.ManyToManyField(IpModel, related_name="post_views", null=True, blank=True)   # blank=True, null=True
    download = models.ManyToManyField(IpModel, related_name="post_download", null=True, blank=True) # blank=True, null=True
    type_data = models.ForeignKey(Type_data, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(max_length=225, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Data, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def total_reads(self):
        return self.read.count()

    def total_downloads(self):
        return self.download.count()

class Type_pemohon(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.SET_NULL)
    type_pemohon = models.CharField(max_length=225, null=True, blank=True)
    
    def __str__(self):
        return self.type_pemohon

class Type_action(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.SET_NULL)
    type_action = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.type_action
    
class Form_information(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, null=True, blank=True)
    kategory_pemohon = models.ForeignKey(Type_pemohon, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.ForeignKey(Type_action, on_delete=models.SET_NULL, null=True, blank=True)
    dinas = models.ForeignKey(Dinas, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.TextField(null=True, blank=True)
    telp = models.CharField(max_length=25, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    ktp = models.FileField(null=True, blank=True)
    purpose = models.TextField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status_choice = (
        ('Belum Diproses','Belum Diproses'),
        ('Diberikan', 'Diberikan'),
        ('Ditolak', 'Ditolak'),
    )
    status = models.CharField(max_length=125, choices=status_choice, null=True, blank=True)
    Information = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.purpose
    
    def delete(self, *args, **kwargs):
        self.ktp.delete()
        super().delete(*args, **kwargs)

class menu(models.Model):
    class Kinds(models.TextChoices):
        BACKEND = 0
        FRONTEND = 1
        
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.PROTECT)     
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)   
    nama = models.CharField(max_length=100)
    href = models.CharField(max_length=255, null=True, blank=True, verbose_name='Link')         
    icon = models.CharField(max_length=50, null=True, blank=True)
    order_menu = models.IntegerField(default=0)    
    kind = models.IntegerField(choices=Kinds.choices, default=Kinds.FRONTEND, blank=True)
    is_visibled = models.BooleanField(default=True)	    
    is_master_menu = models.BooleanField(default=False)	    
    is_statis_menu = models.BooleanField(default=False)	
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        #return  self.nama
        if self.kind == Kinds.FRONTEND:
            res = '[ Front-end ]'
        else:
            res = '[ Back-end ]'

        if self.parent:
            par = self.parent.nama        
        else:
            par = ''

        return "{} {} > {}".format(res, par, self.nama)     

class sengketa(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=225, null=True, blank=True) 
    address = models.TextField(null=True, blank=True) 
    profession = models.CharField(max_length=255, blank=True, null=True)
    telp = models.CharField(max_length=225,null=True, blank=True) 
    email = models.CharField(max_length=225, null=True, blank=True) 
    name_kuasa = models.CharField(max_length=225, null=True, blank=True) 
    address_kuasa = models.TextField(null=True, blank=True) 
    telp_kuasa = models.CharField(max_length=225, null=True, blank=True) 
    reason = models.TextField(null=True, blank=True) 
    date = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=225, null=True, blank=True) 

    def __str__(self):
        return self.reason

class Type_layanan(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class layanan(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.PROTECT)
    jenis = models.CharField(max_length=255, null=True, blank=True)
    type_layanan = models.ForeignKey(Type_layanan, null=True, blank=True, on_delete=models.PROTECT)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.jenis


class slideshow(models.Model):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    slide1 = models.ImageField(blank=True, null=True)
    slide2 = models.ImageField(blank=True, null=True)
    pelayanan = models.ImageField(blank=True, null=True)
    permohonan = models.ImageField(blank=True, null=True)  

    def __str__(self):
        return '{} - {}'.format(self.site, self.description)
    
    # def delete(self, **kwargs):
    #     if self.slide1:
    #         if os.path.isfile(self.slide1.path):
    #             os.remove(self.slide1.path)
        

    
