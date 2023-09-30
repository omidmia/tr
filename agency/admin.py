from django.contrib import admin
from .models import Visa, Company, Ticket, Renew

# Register your models here.


admin.site.register(Visa)
admin.site.register(Company)
admin.site.register(Ticket)
admin.site.register(Renew)
