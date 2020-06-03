"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url 					# Custom entry.

from django.views.generic import TemplateView

app_name = 'cloudify'

urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^cloudify/', include('cloudify.urls', namespace = 'cloudify', name='cloudify')), #Custom entry
    #url(r'^cloudify/', include('mysite.urls')),
    #url(r'^$', views.azure_list, name='Azure_List'),
    #url(r'^', include('cloudify.urls'))
    url(r'^cloudify/', include('cloudify.urls')),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^bootstrap/examples/landing-page.html/$', TemplateView.as_view(template_name='bootstrap/examples/landing-page.html')),  # Bypass view and access templates.
    url(r'^bootstrap/examples/profile-page.html/$', TemplateView.as_view(template_name='bootstrap/examples/profile-page.html')),
    url(r'^bootstrap/examples/signup-page.html/$', TemplateView.as_view(template_name='bootstrap/examples/signup-page.html')),
    

    #url(r'^admin_template/index.html/$', TemplateView.as_view(template_name='admin_template/index.html')),
    #url(r'^cloudify/admin_template/', include('cloudify.urls')),  # Added 22/2 for testing Azure Dashbord page.
    #url(r'^bootstrap/$', include('cloudify.urls')),
]


