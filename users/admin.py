from django.contrib import admin
from .models import User
from .models import Address
from .models import DeliveryTime
from .models import ServiceAddress

# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(DeliveryTime)
admin.site.register(ServiceAddress)


