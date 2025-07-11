from django.contrib import admin

from .models import CynaAddresses,CynaCards,CynaCardTypes,CynaOrderFulfillment,CynaOrders,CynaRelUserCard,AuthUser
# Register your models here.
admin.site.register(CynaAddresses)
admin.site.register(CynaCards)
admin.site.register(CynaCardTypes)
admin.site.register(CynaOrderFulfillment)
admin.site.register(CynaOrders)
admin.site.register(CynaRelUserCard)
admin.site.register(AuthUser)