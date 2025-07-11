#partie panel admin

from django.contrib import admin
from .models import CynaProducts, CynaProductCategories

admin.site.register(CynaProducts)
admin.site.register(CynaProductCategories)