from django.contrib import admin

# Register your models here.
from .models import ContactUs, Property, AboutUs, CustomUser

admin.site.register(ContactUs)
admin.site.register(Property)
admin.site.register(AboutUs)
admin.site.register(CustomUser)