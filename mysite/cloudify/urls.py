from django.conf.urls import url 						# Custom entry
from . import views										# Custom entry

from django.contrib.auth import views as auth_views
# ^$ matches an empty string. Django ignores the "/" in the end.


# If we just want to pass the function's name defined in views.py, i.e. [url(r'^$', home, name='home'),]. Import them as below:
# from .views import home, meterdetails, ....

urlpatterns = [
    # Azureratecardtable views
    #url(r'^$', views.azure_list, name='Azure_List'),
    url(r'^$', views.home, name='home'),
    url(r'^ratecard/$', views.RateCard, name='ratecard'),
    #url(r'^meterdetails/(\w+\s\w+)/', views.meterdetails, name='meterdetails'),    # This is applicable for resources with names separated by on or more space
    url(r'^meterdetails/(\w+\s*\w*\s*\w*)/', views.meterdetails, name='meterdetails'),
    url(r'^login/$', auth_views.login, name='login'),
    #url (r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url (r'^logout/$', auth_views.logout, name='logout'),
    url (r'^register/$', views.register, name='register'),
    #url(r'^bootstrap/$', views.bootstrap, name='bootstrap'),
    url (r'^admin_template/index/$', views.index, name='index'),                 # For testing admin_template/index.html
    url (r'^admin_template/manage_azure.html/$', views.manage_azure, name='manage_azure'),
    url (r'^admin_template/azure_usage.html/$', views.azure_usage, name='azure_usage'),
    #url (r'^(?P<slug>[-\w]+)/$', views.List_VMs, name='List_VMs'),
    url (r'^(?P<slug>[-\w]*)/$', views.manage_azure, name='manage_azure'),

]