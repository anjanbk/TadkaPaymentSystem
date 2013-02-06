from django.http import HttpResponse
from django.template import Context, loader
from public.models import Timeslot

def index(request):
	timeslots = Timeslot.objects.order_by('-day');
	template = loader.get_template('external/index.html')
	context = Context({
		'timeslots':timeslots,
	})
	return HttpResponse(template.render(context))
