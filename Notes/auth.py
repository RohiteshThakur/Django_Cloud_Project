#!/usr/bin/python3

import os
import sys
import requests
import json
from collections import OrderedDict
import pprint

subscription_id = "<Subscription_ID>"

tenant_id       = "<Tenant_ID>"

grant_type      = "client_credentials"

client_id       = "<Client_ID>"

resource        = "https://management.azure.com/"

app_client_id   = "<Client_ID>"

client_secret   = "<Client_Secret>"

MySecretKey     = "<Client_Secret>"    



'''
Issue # We have to get the subscriptionID and offerID from the portal.

How to get values of parameters above:
subscription_id				: Azure portal > Subscriptions > select subscription > subscription ID.
tenant_id 					: Azure portal > AAD > Properties > Directory ID (Tenant ID)
client_secret & MySecretKey : Azure portal > AAD > App registrations > Enter:[Name, App type (WebAPI), Redirect URI (http://localhost)]
							  Once created, click on App, the Application ID is your client ID.
							  Client secret -> Keys (same window, Settings Blade) -> create a key it will give a secret key back.


Why such a URL's syntax?

class BingSearchAPI(object):
    """ interface with the Bing search API """
	bing_api     = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Composite?"
	bing_web_api = "https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web?"

	def replace_symbols(self, request):
		""" Custom urlencoder """
		# They specifically want %27 as the quotation which is a single quote ' ------------=> Note this:....Disgusting..huh!
		# We're going to map both ' and " to %27 to make it more python-esque
		request = string.replace(request, "'", '%27')
		request = string.replace(request, '"', '%27')
		request = string.replace(request, '+', '%2b')
		request = string.replace(request, ' ', '%20')
		request = string.replace(request, ':', '%3a')
		return request

Source: https://github.com/jcelliott/inquire/blob/master/inquire/retrieval/bing_search_api.py
Also: https://stackoverflow.com/questions/47170214/azure-rate-card-api-query-using-uribuilder

For learning API calls on Azure: # https://www.youtube.com/watch?v=ujzrq8Fg9Gc

'''



#API_ENDPOINT = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Commerce/RateCard?api-version=2015-06-01-preview&%24filter=OfferDurableId+eq+%27MS-AZR-0059p%27+and+Locale+eq+%27en-GB%27+and+Regioninfo+eq+%27GB%27+and+Currency+eq+%27GBP%27"

#Working URI
API_ENDPOINT = "https://management.azure.com/subscriptions/<Subscription_ID>/providers/Microsoft.Commerce/RateCard?api-version=2015-06-01-preview&%24filter=OfferDurableId+eq+%27MS-AZR-0059p%27+and+Locale+eq+%27en-GB%27+and+Regioninfo+eq+%27GB%27+and+Currency+eq+%27GBP%27"

#API_ENDPOINT = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Commerce/RateCard?api-version=2015-06-01-preview&$filter=OfferDurableId eq \"MS-AZR-0059P\" and Currency eq \"GBP\" and Locale eq \"en-GB\" and RegionInfo eq \"GB\""

#API_ENDPOINT = "https%3A%2F%2Fmanagement.azure.com%2Fsubscriptions%2F%7B%7Bsubscription-Id%7D%7D%2Fproviders%2FMicrosoft.Commerce%2FRateCard%3Fapi-version%3D2015-06-01-preview%26%24filter%3DOfferDurableId%20eq%20%E2%80%99MS-AZR-0059P%E2%80%99%20and%20Currency%20eq%20%E2%80%99GBP%E2%80%99%20and%20Locale%20eq%20%E2%80%99en-GB%E2%80%99%20and%20RegionInfo%20eq%20%E2%80%99GB"

#API_ENDPOINT = 

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
#print (r.headers['content-type'])
obj = (r.text)
js = json.loads(obj)
Bearer = (js['access_token'])

#print (dir(r))
#js = r.json
#print (type (js))
#output = r_str['access_token']
#print (output)

header = {'Authorization': 'Bearer'+" "+Bearer}
#print (header)
ro = requests.get(url = API_ENDPOINT, headers = header)
#print (ro.json())

print (ro.status_code)
obj = (ro.text)
js = json.loads(obj)

pprint.pprint(js)


###############################################################################################################


try:
    #with open ("{0}".format(arg), 'r') as js:
    with open ("RateCardSmall.json", 'r') as js:
        #data = (json.load(js, object_pairs_hook=OrderedDict))
        data = (json.load(js))
        print ("successful")

except (ValueError, KeyError, TypeError):
    print ("JSON format error")

except IOError as e:
    print ("I/O error({0}): {1}".format(e.errno, e.strerror))

except:
    print ("Unexpected error:", sys.exc_info()[0])
    raise

#pprint.pprint(js)
#pprint.pprint (data.items())

i= 0
#print (len(data["Meters"]))
if (len(data["Meters"])):
	for elem in range(len(data["Meters"])):              # .items() will return each key and values
	    #if (data["Meters"][elem]['MeterCategory'] == "Virtual Machines" and "UK" in data["Meters"][elem]['MeterRegion']):
	    #if ("UK" in data["Meters"][elem]['MeterRegion']):
	        #print (elem)

	    #    pprint.pprint (data["Meters"][elem]["MeterSubCategory"])
		#print ("{:^20} {:^3} {:^18} {:^30} {:^30} {:^35} {:^20}".format(data["Meters"][elem]["EffectiveDate"], data["Meters"][elem]["IncludedQuantity"], data["Meters"][elem]["MeterCategory"], data["Meters"][elem]["MeterId"], data["Meters"][elem]["MeterName"], data["Meters"][elem]["MeterSubCategory"], (str(data["Meters"][elem]["MeterRates"]))))
		#print (str(data["Meters"][elem]["MeterRates"]))
		print (data["Meters"][elem]["MeterSubCategory"])
		print (data["Meters"][elem]["MeterTags"])
		print (data["Meters"][elem]["Unit"])

'''

Same exercise in Django shell:
>>> for elem in range(len(res.ratecard["Meters"])):
...     if (res.ratecard["Meters"][elem]['MeterCategory'] == "Virtual Machines"):
...             print (res.ratecard["Meters"][elem])
... 
'''
