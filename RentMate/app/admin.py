from django.contrib import admin

# Register your models here.
from .models import ContactUs, Property, AboutUs

admin.site.register(ContactUs)
admin.site.register(Property)
admin.site.register(AboutUs)