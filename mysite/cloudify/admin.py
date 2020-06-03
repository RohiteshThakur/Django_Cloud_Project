from django.contrib import admin

# Register your models here.

from .models import Azureratecardtable

#admin.site.register(Azureratecardtable)


@admin.register(Azureratecardtable)
class RateCardAdmin(admin.ModelAdmin):
	list_display = ['region', 'ratecard']
