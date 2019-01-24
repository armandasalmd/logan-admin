from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from .dash_analysis import DashAnalysis
from datetime import datetime
from django.apps import apps

def index(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('accounts:login')) # user is not logged in. redirecting
	elif not request.user.is_staff:
		return HttpResponseRedirect(reverse('employee:index_employee')) # log in! redirecting to employee index page
	# logged in. Loading admin index page!	
	context = { 'title': 'Pagrindinis - Logan admin' }
	context['employees'] = User.objects.filter(groups__name='employee')
	filter_request_status = 0 # 0 - no filtering-use current date, 1 - filter data success, 2 - filter data failed  

	if request.method == 'POST':
		# submit button was pressed (on add new sold item)
		DashAnalysis.add_new_sold_item(request.POST, request.user)
	elif request.method == 'GET':
		# delete query
		if 'del_id' in request.GET and DashAnalysis.delete_sold_item(request.GET):
			return HttpResponseRedirect(reverse('home:index_home')) # user is not logged in. redirecting
		elif 'filter_year' in request.GET and 'filter_month' in request.GET:
			filter_request_status = 1 if DashAnalysis.data_exist_in_date(request.GET['filter_year'], request.GET['filter_month']) else 2
	# loading "add new" form variables
	context = DashAnalysis.load_create_form_variables(context)
	context = DashAnalysis.load_last_sells(context)
	
	info_cards = []
	info_cards.append(('ti-layout-grid2 text-warning border-warning', 'Bonkutės per šią dieną', DashAnalysis.calc_period_stats(period='day', type='bottles')))
	info_cards.append(('ti-money text-success border-success', 'Dienos uždarbis', DashAnalysis.calc_period_stats(period='day', type='profit')))
	info_cards.append(('ti-layout-grid2 text-warning border-warning', 'Bonkutės per šią savaitę', DashAnalysis.calc_period_stats(period='week', type='bottles')))
	info_cards.append(('ti-money text-success border-success', 'Savaitės uždarbis', DashAnalysis.calc_period_stats(period='week', type='profit')))
	context['info_cards'] = info_cards

	# loading data statistics filter SECTION
	now = datetime.now()
	context['year_now'] = str(now.year) # filter value
	context['month_now'] = str(now.month) # filter value
	context['month_list'] = DashAnalysis.get_months()
	context['year_list'] = ['2018'] + DashAnalysis.get_years()
	context['filter_status'] = filter_request_status # 2 - failed to find data
	if filter_request_status == 1 or filter_request_status == 2:
		context['year_now'] = request.GET['filter_year']
		context['month_now'] = request.GET['filter_month']

	filter_cards = []
	if filter_request_status != 2:
		filter_cards.append(('ti-layout-grid2 text-warning border-warning', 'Parduotos bonkutės', DashAnalysis.calc_month_stats(context['year_now'], context['month_now'], type='bottles')))
		filter_cards.append(('ti-money text-success border-success', 'Uždirbti pinigai', DashAnalysis.calc_month_stats(context['year_now'], context['month_now'], type='profit')))
		filter_cards.append(('ti-medall text-danger border-danger', 'Perkamiausias', DashAnalysis.calc_month_stats(context['year_now'], context['month_now'], type='favorite_liquid')))
		filter_cards.append(('ti-filter text-info border-info', 'Parduota tūrio', DashAnalysis.calc_month_stats(context['year_now'], context['month_now'], type='volume_sold')))
	context['filter_cards'] = filter_cards

	return render(request, 'home/index.html', context)

def employee_inventory(request):
	context = { 'title': 'Inventorius - Logan admin', 'empty': False }
	context['employees'] = User.objects.filter(groups__name='employee')
	if request.method == 'GET':
		context['selected_user'] = request.GET.get('employee', None) # username str
	else:
		context['selected_user'] = User.objects.filter(groups__name='employee')[0]
		#return HttpResponseRedirect(reverse('home:index_home')) # failed

	user_obj = User.objects.get(username=context['selected_user'])
	inventories = apps.get_model('employee', 'Inventory').objects.all() # grabs all inventories
	selected_inv = None
	for inv in inventories:
		if inv.user.username == user_obj.username:
			selected_inv = inv
			break
	# until this point inv was selected
	if selected_inv != None:
		selected_items = list()
		i = 0
		liquidObj = None
		table_row = None
		for item in selected_inv.items.all():
			# item is Item object!
			liquidObj = item.liquid.all()[0]
			table_row = (i + 1, liquidObj.taste, item.volume + ' ml', item.strength + ' mg', item.quantity)
			selected_items.append(table_row)
			i += 1
		context['items'] = selected_items
	else: # fail case
		context['empty'] = True
	return render(request, 'home/inventory.html', context)


def messages(request):
	context = { 'title': 'Messsages - Logan admin' }
	context['employees'] = User.objects.filter(groups__name='employee')

	return render(request, 'home/messages.html', context)
