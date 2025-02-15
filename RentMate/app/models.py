from django.db import models

# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquires"
    def __str__(self):
        return f"Inquiry from {self.name}"
    

class Property(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  # Users can enter any category
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='property_images/')
    description = models.TextField()
    
    
    # Optional Room details
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    kitchens = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    storage_room = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Property Listing"
    def __str__(self):
        return self.title

   
class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='property_images/')

    class Meta:
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title 