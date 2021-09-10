from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Dinas)
admin.site.register(Type_data)
admin.site.register(Data)
admin.site.register(IpModel)
admin.site.register(Form_information)
admin.site.register(Type_pemohon)
admin.site.register(Type_action)
admin.site.register(sengketa)
admin.site.register(Type_layanan)
admin.site.register(layanan)
admin.site.register(slideshow)

# tambahan tabel menu
admin.site.register(menu)