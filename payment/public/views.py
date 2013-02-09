from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from public.models import Timeslot, Order
import urllib,urllib2, base64

def index(request):
	timeslots = Timeslot.objects.order_by('-day');
	monday = timeslots.filter(day=0)
	tuesday = timeslots.filter(day=1)
	wednesday = timeslots.filter(day=2)
	thursday = timeslots.filter(day=3)
	friday = timeslots.filter(day=4)
	template = loader.get_template('external/index.html')
	context = RequestContext(request, {
		'monday':monday,
		'tuesday':tuesday,
		'wednesday':wednesday,
		'thursday':thursday,
		'friday':friday,
	})
	return HttpResponse(template.render(context))

def IsNull(value):
    return value is None or len(value) == 0

def songhelp(request):
	context = RequestContext(request, {})
	template = loader.get_template('external/help.html')
	return HttpResponse(template.render(context))

def signup(request):
	csrfContext = RequestContext(request)
	production = True
	
	sName = request.POST['inputNameFrom']
	sGender = request.POST['inputGenderFrom']
	sPhone = request.POST['inputPhoneFrom']
	rName = request.POST['inputNameTo']
	rGender = request.POST['inputGenderTo']
	location = request.POST['inputLocation']
	song = request.POST['inputSong']

	try:
		tip = float(request.POST['inputTip'])
	except ValueError:
		tip = 0.0

	amount = 1.34

	if IsNull(sName) or IsNull(sGender) or IsNull(sPhone) or IsNull(rName) or IsNull(rGender) or IsNull(location) or IsNull(song):
		context = RequestContext(request, {})
		template = loader.get_template('error.html')
		return HttpResponse(template.render(context))
	else:
		# Google Checkout redirect handling
		sandboxusername = '359393532142800'
		sandboxpassword = 'rCY7EiDRDEFcMf6wlAVnBg'

		productionusername = '972820744187740'
		productionpassword = 'JwLNM-uN6PUG1UlITqqZxw'

		sandboxurl = 'https://sandbox.google.com/checkout/api/checkout/v2/merchantCheckoutForm/Merchant/359393532142800'
		productionurl = 'https://checkout.google.com/api/checkout/v2/merchantCheckoutForm/Merchant/972820744187740'


		if production:
			url = productionurl
			username = productionusername
			password = productionpassword
		else:
			url = sandboxurl
			username = sandboxusername
			password = sandboxpassword
		
		if tip > 0:
			amount = 1.34 + tip
		
		payload = {'_type':'checkout-shopping-cart',
			'item_name_1':'Singing Gram',
			'item_description_1':'Taal Tadka Valentine\'s Day Singing Gram',
			'item_quantity_1':'1',
			'shopping-cart.items.item-1.digital-content.display-disposition':'OPTIMISTIC',
			'shopping-cart.items.item-1.digital-content.description':'Once we\'ve processed your order, your we will find embarrass the recipient for you. Happy Valentine\'s Day!',
			'item_price_1':str(amount),
			'item_currency_1':'USD',
			'_charset_':'utf-8'}

		import requests
		resp = requests.post(url, payload, auth=(username,password))
		#resp = requests.post(url,data = json.dumps(payload),headers=headers)

		content = resp.content

		index = content.find('redirect-url')
		if index is not -1:
			index += len('redirect-url') + 1
			redirecturl=content[index:]
		else:
			redirecturl='failure'

		selectedid = request.POST['timeSlotRadios']
		
		# Update db
		t = Timeslot.objects.get(id=selectedid)
		t.availability=False
		t.save()

		# Update spreadsheet
		day = Timeslot.objects.get(id=selectedid).day
		enumdays = ["M","T","W","Th","F"]
		slot = enumdays[day] + " " + Timeslot.objects.get(id=selectedid).time

		o = Order(0,'ONLINE',sName,sGender,sPhone,rName,rGender,slot,location,song)
		o.save()
		
		return HttpResponseRedirect(urllib.unquote(redirecturl))
