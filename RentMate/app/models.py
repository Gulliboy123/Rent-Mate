from django.db import models
import random
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        NORMAL_USER = "normal_user", "Normal User"
        PROPERTY_MANAGER = "property_manager", "Property Manager"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.NORMAL_USER
    )

    def is_property_manager(self):
        return self.role == self.Role.PROPERTY_MANAGER

    def is_admin(self):
        return self.role == self.Role.ADMIN


# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    replied = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquires"
    def __str__(self):
        return f"Inquiry from {self.name}"
    


   
class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='property_images/')

    class Meta:
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title 
  


class PropertyDetail(models.Model):
    PROPERTY_TYPES = [('flat', 'Flat'), ('room', 'Room')]
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]

    unique_id = models.CharField(max_length=10, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(choices=PROPERTY_TYPES, max_length=10)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    neighbourhood = models.CharField(max_length=100)
    num_kitchens = models.IntegerField(default=0)
    num_bedrooms = models.IntegerField(default=0)
    num_bathrooms = models.IntegerField(default=0)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.CharField(max_length=20, choices=[('available', 'Available'), ('unavailable', 'Unavailable')])
    license_number = models.CharField(max_length=100)
    amenities = models.TextField()  # Store as JSON or comma-separated values
    approval_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = str(random.randint(1, 99))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(PropertyDetail, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="property_images/")

    def __str__(self):
        return f"Image for {self.property.title}"