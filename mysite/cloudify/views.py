from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from .models import Azureratecardtable
from operator import itemgetter					# This import is used in meterdetails for sorting JSON by a 'key'

# Additional imports for User Auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, ListVMForm, CreateVMForm, ShutDownVMForm, StartVMForm, AzureUsageForm

import os
import sys
import requests
import json
import pprint

'''
def azure_list(request):								# No class but a function.
	res = Azureratecardtable.cm.all()					# Takes "cm" from models.py
	return render(request, 'frontend/base.html', {'result' : res})
'''

@login_required											# This will redirect users to login.html before they can access landing page.
def home(request):										# No class but a function.
	#data = Azureratecardtable.cm.all()					# Takes "cm" from models.py where this query is explicitely defind to pull data for region:USA.
	#data = Azureratecardtable.objects.all()				# This query returns all objects in Azureratecardtable table.
	#return render(request, 'frontend/home.html', {'data' : data})
	return render(request, 'frontend/landing-page.html', {})


def RateCard(request):										# No class but a function.
	#data = Azureratecardtable.cm.all()					# Takes "cm" from models.py where this query is explicitely defind to pull data for region:USA.
	data = Azureratecardtable.objects.all()				# This query returns all objects in Azureratecardtable table.
	return render(request, 'frontend/ratecard.html', {'data' : data})

def meterdetails(request, MeterCategory):
	'''
	Take MeterCategory as argument, scan the JSON data, If found save value in dict_store and returns the same.
	'''
	print (MeterCategory)
	data = Azureratecardtable.objects.get(region='UK')
	item_store = [] 
	sorted_item_store = []
	i = 0;
	if (MeterCategory == "Virtual Machines"):
		for elem in range(len(data.ratecard['Meters'])):
			if (data.ratecard["Meters"][elem]['MeterCategory'] == MeterCategory and (data.ratecard["Meters"][elem]['MeterRegion'] =='UK South' or data.ratecard["Meters"][elem]['MeterRegion'] == 'UK West')):
				cost = data.ratecard["Meters"][elem]['MeterRates']['0']
				monthly_cost = cost * 730
				monthly_cost_rounded = round(monthly_cost, 2)
				# Append monthy cost
				data.ratecard["Meters"][elem]["MonthlyCost"] = monthly_cost_rounded

				# Now append he full serialized JSON stanza.
				item_store.append(data.ratecard["Meters"][elem])

			#Sort results according to "MonthlyCost" (https://wiki.python.org/moin/SortingListsOfDictionaries)
			sorted_item_store = sorted(item_store, key=itemgetter('MonthlyCost'))

	if (MeterCategory == "App Services"):
		for elem in range(len(data.ratecard['Meters'])):
			if (data.ratecard['Meters'][elem]['MeterCategory'] == MeterCategory): #and (data.ratecard["Meters"][elem]['MeterRegion'] =='UK South' or data.ratecard["Meters"][elem]['MeterRegion'] == 'UK West')):
				print (data.ratecard['Meters'][elem])
				sorted_item_store.append(data.ratecard["Meters"][elem])

	if (
		MeterCategory == "Storage" or 
		MeterCategory == "Notification Hubs" or 
		MeterCategory == "Network Watcher" or 
		MeterCategory == "Backup" or
		MeterCategory == "Container Instances" or
		MeterCategory == "RemoteApp" or
		MeterCategory == "Functions" or
		MeterCategory == "Dynamics" or
		MeterCategory == "Power BI Embedded" or
		MeterCategory == "Scheduler" or
		MeterCategory == "Cloud Services" or
		MeterCategory == "Analysis Services" or
		MeterCategory == "Media" or
		MeterCategory == "Cache" or
		MeterCategory == "Mobile Services" or
		MeterCategory == "Citrix" or
		MeterCategory == "Recovery Services" or
		MeterCategory == "Automation and Control" or
		MeterCategory == "API Management" or
		MeterCategory == "Azure App Service" or
		MeterCategory == "Site Recovery" or
		MeterCategory == "Remote Access Rights" or
		MeterCategory == "Service Bus" or
		MeterCategory == "Azure IoT Hub" or
		MeterCategory == "Service Fabric" or
		MeterCategory == "Security Center" or
		MeterCategory == "Visual Studio" or
		MeterCategory == "Power BI" or
		MeterCategory == "Cortana Intelligence" or
		MeterCategory == "Networking" or
		MeterCategory == "Container Registry" or
		MeterCategory == "Xamarin University" or
		MeterCategory == "Genomics" or
		MeterCategory == "Linux Support" or
		MeterCategory == "Data Management" or
		MeterCategory == "StorSimple" or
		MeterCategory == "Machine Learning" or
		MeterCategory == "Application Insights" or
		MeterCategory == "Azure Monitor" or
		MeterCategory == "Logic Apps" or
		MeterCategory == "Insight and Analytics" or
		MeterCategory == "Azure Data Factory" or
		MeterCategory == "Time Series Insights" or
		MeterCategory == "Identity" or
		MeterCategory == "Data Services" or
		MeterCategory == "IoT Hub Device Provisioning" or
		MeterCategory == "Event Grid" or
		MeterCategory == "Cognitive Services" or
		MeterCategory == "Azure Location Based Services" or
		MeterCategory == "Key Vault" or
		MeterCategory == "SQL Database" or
		MeterCategory == "App Service" or
		MeterCategory == "Microsoft IoT Central" or
		MeterCategory == "CDN" or
		MeterCategory == "Integration" or
		MeterCategory == "Business Analytics"
		): 
		for elem in range(len(data.ratecard['Meters'])):
			if (data.ratecard['Meters'][elem]['MeterCategory'] == MeterCategory): #and (data.ratecard["Meters"][elem]['MeterRegion'] =='UK South' or data.ratecard["Meters"][elem]['MeterRegion'] == 'UK West')):
				print (data.ratecard['Meters'][elem])
				sorted_item_store.append(data.ratecard["Meters"][elem])

	if (not sorted_item_store):
		raise Http404('Category not found!')


	return render(request, 'frontend/meterdetails.html', {'meterdetail' : sorted_item_store})		# A dict key in 3rd argument is required.


'''
I am using Django built in Authentication. Hence, this section has been #'ed out.
def user_login(request):
	Downstream: This function is links to forms.py where we have two DB fields declared: "username" & "password" in class LoginForm.
	Upstream: Take the POST request from login.html and validates. 
	This function will then instantiate LoginForm class which brings in two class attributes: username and password.
	If we used Django's built-in form it will display the form with username and password as input, however I am useing a customized HTML form,
	I have to save the input in username and password.  

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if (form.is_valid()):									# is_valid is a function f'ker.
			cd = form.cleaned_data
			# print (form.cleaned_data)							# For debugging.
			user = authenticate(username=cd['username'], password=cd['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					#return HttpResponse('Authenticated Successfully')
					return redirect('/bootstrap/examples/landing-page.html/')   # Note: "/" before "bootstrap". This is needed when we want Django to start finding the page from /bootstrap folder.
																				# 'bootstrap/examples/... will make Django to search from /cloudify/login/bootstrap.... which is wrong.
				else: 
					return HttpResponse('Disabled Account')
			else:
				return HttpResponse('Invalid Login')
	else:
		form = LoginForm()

	return render(request, 'frontend/login.html', {'form':form})
'''

def List_VMs(request, SubId):
	if request.method == 'POST':
		print ("List_VMs function triggered")
		form = ListVMForm(request.POST)
		if (form.is_valid()):
			cd = form.cleaned_data
			SubId = cd['SubId']
			print (SubId)
			if SubId is not None:
				API_ENDPOINT = "https://management.azure.com/subscriptions/273949b5-7c43-492c-9419-a248e397d865/resources?api-version=2016-02-01"
				subscription_id = SubId
				tenant_id       = "f8cc34ec-175c-4586-acf5-d544d7bd8859"
				grant_type      = "client_credentials"
				client_id       = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				resource        = "https://management.azure.com/"
				app_client_id   = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				client_secret   = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="
				MySecretKey     = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="

				URL = "https://login.microsoftonline.com/"+tenant_id+"/oauth2/token"

				data = {'subscription_id': subscription_id,
						'tenant_id': tenant_id,
						'grant_type':grant_type,
						'client_id':client_id,
						'resource': resource,
						'app_client_id': app_client_id,
						'client_secret': client_secret,
						'MySecretKey': MySecretKey}

				r = requests.post(url = URL, data = data)
				obj = (r.text)
				js = json.loads(obj)
				Bearer = (js['access_token'])

				header = {'Authorization': 'Bearer'+" "+Bearer}

				ro = requests.get(url = API_ENDPOINT, headers = header)

				print (ro.status_code)
				obj = (ro.text)
				js = json.loads(obj)

				#pprint.pprint(js)

				return render(request, 'admin_template/results.html', {'result':js})

	return render(request, 'admin_template/manage_azure.html', {'form':form})


def register(request):
	if request.method == 'POST':
	    user_form = UserRegistrationForm(request.POST)

	    if user_form.is_valid():
	        # Create a new user object but avoid saving it yet
	        new_user = user_form.save(commit=False)
	        # Set the chosen password
	        new_user.set_password(user_form.cleaned_data['password'])
	        # Save the User object
	        new_user.save()
	        # Create the user profile
	        return render(request, 'registration/register_done.html', {'new_user': new_user})

	else:
	    user_form = UserRegistrationForm()

	return render(request, 'registration/register.html', {'user_form': user_form})


# Only for testing
def index(request):										# No class but a function.
	#data = Azureratecardtable.cm.all()					# Takes "cm" from models.py where this query is explicitely defind to pull data for region:USA.
	#data = Azureratecardtable.objects.all()				# This query returns all objects in Azureratecardtable table.
	return render(request, 'admin_template/index.html', {})



def manage_azure(request):
	if request.method == 'POST' and 'List' in request.POST:
		print ("manage_azure function triggered")
		form = ListVMForm(request.POST)
		if (form.is_valid()):
			cd = form.cleaned_data
			SubId = cd['SubId']
			print (SubId)
			if SubId is not None:
				API_ENDPOINT = "https://management.azure.com/subscriptions/273949b5-7c43-492c-9419-a248e397d865/resources?api-version=2016-02-01"
				subscription_id = SubId
				tenant_id       = "f8cc34ec-175c-4586-acf5-d544d7bd8859"
				grant_type      = "client_credentials"
				client_id       = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				resource        = "https://management.azure.com/"
				app_client_id   = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				client_secret   = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="
				MySecretKey     = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="

				URL = "https://login.microsoftonline.com/"+tenant_id+"/oauth2/token"

				data = {'subscription_id': subscription_id,
						'tenant_id': tenant_id,
						'grant_type':grant_type,
						'client_id':client_id,
						'resource': resource,
						'app_client_id': app_client_id,
						'client_secret': client_secret,
						'MySecretKey': MySecretKey}

				r = requests.post(url = URL, data = data)
				obj = (r.text)
				js = json.loads(obj)
				Bearer = (js['access_token'])

				header = {'Authorization': 'Bearer'+" "+Bearer}

				ro = requests.get(url = API_ENDPOINT, headers = header)

				print (ro.status_code)
				obj = (ro.text)
				js = json.loads(obj)
				json_pretty = json.dumps(js, sort_keys=True, indent=2)

				pprint.pprint(js)

				return render(request, 'admin_template/results.html', {'result':json_pretty})


	if request.method == 'POST' and 'Create' in request.POST:
		print (request.POST)
		print ("Create_VMs function triggered")
		form = CreateVMForm(request.POST)
		print (form)
		if (form.is_valid()):
			cd = form.cleaned_data
			SubId    	  = cd['SubId']
			ResourceGroup = cd['ResourceGroup']
			VmName   	  = cd['VmName']
			UserName 	  = cd['UserName']
			PassWord 	  = cd['PassWord']

			if SubId is not None:
				API_ENDPOINT = "https://management.azure.com/subscriptions/" + SubId + "/resourceGroups/"+ ResourceGroup + "/providers/Microsoft.Compute/virtualMachines/" + VmName + "?api-version=2017-12-01"
				subscription_id = SubId
				tenant_id       = "f8cc34ec-175c-4586-acf5-d544d7bd8859"
				grant_type      = "client_credentials"
				client_id       = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				resource        = "https://management.azure.com/"
				app_client_id   = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				client_secret   = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="
				MySecretKey     = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="

				URL = "https://login.microsoftonline.com/"+tenant_id+"/oauth2/token"

				data = {'subscription_id': subscription_id,
						'tenant_id': tenant_id,
						'grant_type':grant_type,
						'client_id':client_id,
						'resource': resource,
						'app_client_id': app_client_id,
						'client_secret': client_secret,
						'MySecretKey': MySecretKey}

				r = requests.post(url = URL, data = data)
				obj = (r.text)
				js = json.loads(obj)
				Bearer = (js['access_token'])
				#print (Bearer)

				header = {'Authorization': 'Bearer'+" "+Bearer, 'Accept' : 'application/json', 'Content-Type' : 'application/json'}

				ro = requests.get(url = API_ENDPOINT, headers = header)

				with open ('cloudify/AzureJSONTemplates/CreateVM.json', 'r') as js:  #Note: Windows don't understand ./ so provide absolute path - Always.
				    content = (json.load(js))
				    data = json.dumps(content)

				print (type(data))
				#print (header)
				ro = requests.put(url = API_ENDPOINT, data = data, headers = header)
				data = ro.json
				print (data) 
				return render(request, 'admin_template/results.html', {'result':data})


	if request.method == 'POST' and 'ShutDown' in request.POST:
		print (request.POST)
		print ("ShutDownVMs function triggered")
		form = ShutDownVMForm(request.POST)
		print (form)
		if (form.is_valid()):
			cd = form.cleaned_data
			SubId    	  = cd['SubId']
			ResourceGroup = cd['ResourceGroup']
			VmName   	  = cd['VmName']

			if SubId is not None:
				API_ENDPOINT 	= "https://management.azure.com/subscriptions/" + SubId + "/resourceGroups/" + ResourceGroup + "/providers/Microsoft.Compute/virtualMachines/" + VmName + "/powerOff?api-version=2017-12-01"
				subscription_id = SubId
				tenant_id       = "f8cc34ec-175c-4586-acf5-d544d7bd8859"
				grant_type      = "client_credentials"
				client_id       = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				resource        = "https://management.azure.com/"
				app_client_id   = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				client_secret   = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="
				MySecretKey     = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="

				URL = "https://login.microsoftonline.com/"+tenant_id+"/oauth2/token"

				data = {'subscription_id': subscription_id,
						'tenant_id': tenant_id,
						'grant_type':grant_type,
						'client_id':client_id,
						'resource': resource,
						'app_client_id': app_client_id,
						'client_secret': client_secret,
						'MySecretKey': MySecretKey}

				r = requests.post(url = URL, data = data)
				obj = (r.text)
				js = json.loads(obj)
				Bearer = (js['access_token'])

				header = {'Authorization': 'Bearer'+" "+Bearer}

				ro = requests.post(url = API_ENDPOINT, headers = header)	# Note: this is a POST request.

				print (ro.status_code)										# Only status code is returned.

				return render(request, 'admin_template/results.html', {'result':(ro.status_code)})


	if request.method == 'POST' and 'StartVM' in request.POST:
		print (request.POST)
		print ("StartVMs function triggered")
		form = StartVMForm(request.POST)
		print (form)
		if (form.is_valid()):
			cd = form.cleaned_data
			SubId    	  = cd['SubId']
			ResourceGroup = cd['ResourceGroup']
			VmName   	  = cd['VmName']

			if SubId is not None:
				API_ENDPOINT 	= "https://management.azure.com/subscriptions/" + SubId + "/resourceGroups/" + ResourceGroup + "/providers/Microsoft.Compute/virtualMachines/" + VmName + "/start?api-version=2017-12-01"
				subscription_id = SubId
				tenant_id       = "f8cc34ec-175c-4586-acf5-d544d7bd8859"
				grant_type      = "client_credentials"
				client_id       = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				resource        = "https://management.azure.com/"
				app_client_id   = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				client_secret   = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="
				MySecretKey     = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="

				URL = "https://login.microsoftonline.com/"+tenant_id+"/oauth2/token"

				data = {'subscription_id': subscription_id,
						'tenant_id': tenant_id,
						'grant_type':grant_type,
						'client_id':client_id,
						'resource': resource,
						'app_client_id': app_client_id,
						'client_secret': client_secret,
						'MySecretKey': MySecretKey}

				r = requests.post(url = URL, data = data)
				obj = (r.text)
				js = json.loads(obj)
				Bearer = (js['access_token'])

				header = {'Authorization': 'Bearer'+" "+Bearer}

				ro = requests.post(url = API_ENDPOINT, headers = header)	# Note: this is a POST request.

				print (ro.status_code)										# Only status code is returned. 202 = success.

				return render(request, 'admin_template/results.html', {'result':(ro.status_code)})

		else:
			print ("Form is not valid")


	return render(request, 'admin_template/manage_azure.html', {})
	#return render(request, 'admin_template/manage_azure.html', {})


def azure_usage(request):
	if request.method == 'POST' and 'AzureUsage' in request.POST:
		print (request.POST)
		print ("Azure Usage function triggered")
		form = AzureUsageForm(request.POST)
		print (form)
		if (form.is_valid()):
			cd = form.cleaned_data
			SubId    	  = cd['SubId']

			if SubId is not None:
				API_ENDPOINT 	= "https://management.azure.com/subscriptions/"+ SubId +"/providers/Microsoft.Consumption/usageDetails?api-version=2018-01-31"
				subscription_id = SubId
				tenant_id       = "f8cc34ec-175c-4586-acf5-d544d7bd8859"
				grant_type      = "client_credentials"
				client_id       = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				resource        = "https://management.azure.com/"
				app_client_id   = "6a02b44e-5643-4c31-b726-8cab6cf8b258"
				client_secret   = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="
				MySecretKey     = "zOQSlLNtsECjBm4tRtnVRUTFGaKHn7yfQaDIZzn2rYs="

	
			URL = "https://login.microsoftonline.com/"+tenant_id+"/oauth2/token"

			data = {'subscription_id': subscription_id,
					'tenant_id': tenant_id,
					'grant_type':grant_type,
					'client_id':client_id,
					'resource': resource,
					'app_client_id': app_client_id,
					'client_secret': client_secret,
					'MySecretKey': MySecretKey}

			r = requests.post(url = URL, data = data)

			print (r.status_code)

			obj = (r.text)
			js = json.loads(obj)
			Bearer = (js['access_token'])

			header = {'Authorization': 'Bearer'+" "+Bearer}
			#print (header)
			ro = requests.get(url = API_ENDPOINT, headers = header)
			obj = (ro.text)
			json_data = json.loads(obj)

			billing_items = []
			resource_type = []
			br_mapper = {}
			for item in range(len(json_data["value"])):
			    billing_items.append(json_data["value"][item]["properties"]["instanceName"])

			billing_items = list(set(billing_items))
			#print (billing_items)

			for billing_item in billing_items:
				for item in range(len(json_data["value"])):
					if (billing_item in json_data["value"][item]["properties"]["instanceName"]):
						resource_type.append(json_data["value"][item]["properties"]["instanceId"].split("/")[-2])
						break

			#print (billing_items)
			#print (resource_type)
			br_mapper = dict(zip(billing_items, resource_type))
			print (br_mapper)
			

			#return render(request, 'admin_template/azure_usage_tables.html', {'json_data': json_data, 'billing_items': billing_items, 'resource_type': resource_type})
			return render(request, 'admin_template/azure_usage_tables.html', {'json_data': json_data, 'map': br_mapper})

	return render(request, 'admin_template/azure_usage.html', {})