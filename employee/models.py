from django.db import models
from django.contrib.auth.models import User

# python manage.py check
# python manage.py makemigrations <app>
# python manage.py migrate


class Bottle(models.Model): # constant
	volume = models.CharField(max_length=8)
	strength = models.CharField(max_length=8)

	base_price = models.FloatField(default=0)
	owner_price = models.FloatField(default=0)
	selling_price = models.FloatField(default=0)

	def __str__(self):
		return 'Bottle: ' + self.volume + 'ml (' + self.strength + ')';

class Liquid(models.Model): # constant
	taste = models.CharField(max_length=255)
	description = models.CharField(max_length=2550)
	is_nic_salt = models.BooleanField(default=True)
	
	def __str__(self):
		return 'Liquid: ' + self.taste;

class Item(models.Model): # duplicates allowed
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	liquid = models.ManyToManyField(Liquid) # list of 1 item (1 to 1)
	volume = models.CharField(max_length=8, default='10')
	strength = models.CharField(max_length=8, default='20')

	def __str__(self):
		mliquid = self.liquid.all()[0]
		return 'Item: ' + mliquid.taste + '(' + self.volume + 'ml - ' + self.strength + ')';

class Inventory(models.Model):
	# list of items inventory has
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	items = models.ManyToManyField(Item) # !important - (1 to many) - list of items

	def __str__(self):
		try:
			return 'Inventory: ' + self.user.username;
		except:
			return 'Inventory'


class SoldItems(models.Model):
	date = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)

	def __str__(self):
		return 'SoldItems: ' + self.user.username;