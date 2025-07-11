#partie panel admin

from django.contrib import admin
from .models import CynaProducts, CynaProductCategories, CynaDiscounts, CynaRenewalIntervals

admin.site.register(CynaProducts)
admin.site.register(CynaProductCategories)
admin.site.register(CynaDiscounts)
admin.site.register(CynaRenewalIntervals)