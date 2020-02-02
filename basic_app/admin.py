from django.contrib import admin
from basic_app.models import CustProfileInfo
from basic_app.models import VendorProfileInfo
from basic_app.models import SoldItem
from basic_app.models import PurchasedItem
from basic_app.models import CartItem

# Register your models here.
admin.site.register(CustProfileInfo)
admin.site.register(VendorProfileInfo)
admin.site.register(SoldItem)
admin.site.register(PurchasedItem)
admin.site.register(CartItem)
