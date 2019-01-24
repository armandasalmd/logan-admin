from datetime import datetime, timedelta
from .models import *
from django.apps import apps
from django.contrib.auth.models import User
import traceback

# class with static functions
class DashAnalysis:

	def month_to_str(month):
		''' <summary>Adds 0 if month is 1 to 9</summary>
			<return>str</return>'''
		month = str(month)
		return '0' + month if len(month) == 1 else month			

	def get_months():
		return ['Sausis', 'Vasaris', 'Kovas', 'Balandis', 'Gegužė', 'Birželis', 'Liepa', 'Rugpjūtis', 'Rugsėjis', 'Spalis', 'Lapkritis', 'Gruodis']

	def get_years():
		return ['2019', '2020', '2021', '2022']

	def data_exist_in_date(year, month):
		month = DashAnalysis.month_to_str(month)
		date_from = year + '-' + month + '-01 00:00:00' # first month day, 00:00 time
		date_to = year + '-' + month + '-30 00:00:00' # last month day, 00:00 time
		filtered_items = AdminSoldItems.objects.filter(date__range=[date_from, date_to])
		if len(filtered_items) == 0: # protection of having 0 items - FAIL so query
			return False
		else:
			return True

	def calc_month_stats(year, month, type='profit', calc_profit=True):
		''' <param name="year">selected filter year</param>
			<param name="month">selected filter month</param>
			<param name="type">stats of what?{profit, bottles, favorite_liquid, volume_sold}</param>
			<param name="calc_profit">Calculate profit? or sell price?(False)</param>
			<summary>Calculates sells statistics</summary>
			<return>str(None if failed to query)</return>'''
		month = DashAnalysis.month_to_str(month)
		year = str(year)
		date_from = year + '-' + month + '-01 00:00:00' # first month day, 00:00 time
		date_to = year + '-' + month + '-30 00:00:00' # last month day, 00:00 time
		filtered_items = AdminSoldItems.objects.filter(date__range=[date_from, date_to])
		if len(filtered_items) == 0: # protection of having 0 items - FAIL so query
				return None

		if type == 'bottles':
			count = 0 # counts bottles sold
			for item in filtered_items:
				count += float(item.quantity)
			return str(int(count)) + ' vnt'
		elif type == 'profit':
			total = 0.0
			for item in filtered_items:
				total += DashAnalysis.calc_item_profit(item, calc_profit=calc_profit)
			return str(round(total, 2)) + '€'
		elif type == 'favorite_liquid':
			liquid_model_items = apps.get_model('employee', 'Liquid').objects.all()
			if len(liquid_model_items) == 0: # protection of having 0 items - FAIL so query
				return None
			d = {}
			for item in filtered_items: # forms freaquent list
				if not item.taste in d:
					d[item.taste] = item.quantity
				else:
					d[item.taste] += item.quantity
			biggest_val_key = list(d.keys())[0]
			for key in d:
				if d[biggest_val_key] < d[key]:
					biggest_val_key = key
			return biggest_val_key
		elif type == 'volume_sold':
			total = 0
			for item in filtered_items:
				total += item.quantity * int(item.volume)
			return str(total) + ' ml'

	def calc_period_stats(period='lifetime', type='profit', calc_profit=True):
		''' <param name="period">Time period {lifetime, month, week, day}</param>
			<param name="type">profit made OR bottles sold? {profit, bottles}</param>
			<param name="calc_profit">Calculate profit? or sell price?(False)</param>
			<summary>Calculates statistics for given date</summary>
			<return>str</return>'''
		period_in_days = 0
		answer = 0 # return value
		time_format = '%Y-%m-%d %H:%M:%S'
		if period == 'lifetime':
			period_in_days = 365 * 8 # lifetime = last 8 years
		elif period == 'month':
			period_in_days = 30
		elif period == 'week':
			period_in_days = 7
		elif period == 'day':
			period_in_days = 1
		time_delta_str = (datetime.today() - timedelta(days=period_in_days)).strftime(time_format)
		time_filtered_items = AdminSoldItems.objects.filter(date__range=[time_delta_str, datetime.today().strftime(time_format)])
		if type == 'bottles':
			for item in time_filtered_items:
				answer += float(item.quantity)
			return str(int(answer)) + ' vnt'
		else: # default type == profit
			for item in time_filtered_items:
				answer += DashAnalysis.calc_item_profit(item, calc_profit=calc_profit)
			return str(round(answer, 2)) + '€'

	def calc_item_profit(item_obj, calc_profit=False):
		''' <param name="item_obj">Item to calculate on</param>
			<param name="calc_profit">Calculate profit? or sell price?(False)</param>
			<summary>Calculates item s (value)/(made profit)</summary>
			<return>float</return>'''
		try:
			bottle_set = apps.get_model('employee', 'Bottle').objects.filter(volume=item_obj.volume, strength=item_obj.strength)
			if len(bottle_set) == 1: # bottle found
				if calc_profit:
					return round((bottle_set[0].owner_price - bottle_set[0].base_price) * item_obj.quantity, 2)
				else:
					return round(bottle_set[0].owner_price * item_obj.quantity, 2)
			else:
				throw('No bottle found')
		except:
			traceback.print_exc()
			print('Error in: DashAnalysis.calc_item_profit()')
			return float(0)

	def give_ago_time(past_date_str):
		''' <param name="past_date_str">Sold item date</param>
			<summary>Calculates what time ago it was i.e. 2h ago</summary>
			<return>str</return>'''
		time_now = datetime.now()
		time_past = datetime.strptime(past_date_str, '%Y-%m-%d %H:%M:%S')
		time_delta = time_now - time_past
		if time_delta.total_seconds() < 60:
			return str(int(time_delta.total_seconds())) + 's'
		elif time_delta.total_seconds() < 3600:
			return str(int(time_delta.total_seconds() // 60)) + 'm'
		elif time_delta.total_seconds() < 3600 * 24:
			return str(int(time_delta.total_seconds() // 3600)) + 'h'
		else:
			return str(int(time_delta.total_seconds() // (3600 * 24))) + 'd'
	
	def add_new_sold_item(post_d, user_obj):
		''' <param name="post_d">form POST (query dict)</param>
			<param name="user_obj">django User model</param>
			<summary>adds sold item(stored in post) to database</summary>'''
		liquid_model = apps.get_model('employee', 'Liquid')
		time_format = '%Y-%m-%d %H:%M:%S'
		pieces = []
		try:
			pieces.append(datetime.today().strftime(time_format)) # current TIME in string
			pieces.append(liquid_model.objects.order_by('taste')[int(post_d['select1']) - 1].taste) # gets selected object title/TASTE
			pieces.append(int(post_d['select2'])) # parses selected QUANTITY
			pieces.append(post_d['inline-radios']) # parses selected VOLUME
			pieces.append(post_d['2inline-radios']) # parses selected STRENGTH
			# add item to datebase
			AdminSoldItems.objects.create(date = pieces[0], taste=pieces[1], quantity=pieces[2], volume=pieces[3], strength=pieces[4])
		except:
			print('Error in: DashAnalysis.add_new_sold_item()')
			return # exit function

	def load_last_sells(context):
		''' <param name="context">dict for template loading</param>
			<summary>Supplements context with last sold items</summary>
			<return>dict(context)</return>'''
		last_sells = AdminSoldItems.objects.order_by('-date')[:4] # takes 4 newest sold items
		last_sells_rows = [] # data list for context 
		for item in last_sells:
			misc_col = item.volume + 'ml, ' + item.strength + 'mg'
			if item.quantity != 1:
				misc_col += ', ' + str(item.quantity) + 'vnt'
			# adds single row data
			last_sells_rows.append((DashAnalysis.give_ago_time(item.date), item.taste, DashAnalysis.calc_item_profit(item), misc_col))
		context['last_sold_items'] = last_sells_rows
		return context
	
	def delete_sold_item(get_d):
		''' <param name="get_d">form GET quary dict</param>
			<summary>Removes selected item from database</summary>
			<return>True if item was deleted</return>'''
		try:
			id = int(get_d['del_id'])
			solds_list = AdminSoldItems.objects.order_by('-date')[:4] # selects 4 newest solds
			solds_list[id].delete()
			return True
		except:
			print('Error in: DashAnalysis.delete_sold_item()')
			return False

	def load_create_form_variables(context):
		''' <param name="context">dict for template loading</param>
			<summary>Supplements context with selection values</summary>
			<return>dict(context)</return>'''
		bottles = apps.get_model('employee', 'Bottle').objects.all() # gets all bottles
		liquids = apps.get_model('employee', 'Liquid').objects.order_by('taste') # gets all liquids
		volume_list = []
		strength_list = []
		taste_list = []
		# loops bottles, get volumes and strengths
		for b in bottles:
			if not b.volume in volume_list:
				volume_list.append(b.volume)
			if not b.strength in strength_list:
				strength_list.append(b.strength)
		context['volumes'] = volume_list
		context['strengths'] = strength_list
		# loops liquids, get titles
		for l in liquids:
			if not l.taste in taste_list:
				taste_list.append(l.taste)
		context['tastes'] = taste_list
		return context