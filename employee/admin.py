from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Liquid)
admin.site.register(Bottle)
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(SoldItems)