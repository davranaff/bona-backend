from django.contrib import admin

from app.models import *

# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(DeliveryCountries)
admin.site.register(ProductCountry)
admin.site.register(ProductType)
admin.site.register(Banner)