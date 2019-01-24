from django.db import models
from datetime import datetime


# Create your models here.
class AdminSoldItems(models.Model):
	date = models.CharField(max_length=100, default=datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
	taste = models.CharField(max_length=255)
	is_nic_salt = models.BooleanField(default=True)
	quantity = models.IntegerField(default=1)
	volume = models.CharField(max_length=8, default='10')
	strength = models.CharField(max_length=8, default='20')

	def __str__(self):
		return 'SoldItem: ' + self.taste + '(' + self.date + ')';