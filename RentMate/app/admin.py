from django.contrib import admin

# Register your models here.
from .models import AboutUs
from .models import ContactUs
from django.core.mail import send_mail
from django.utils.html import format_html
from .models import PropertyDetail, PropertyImage

admin.site.register(ContactUs)
admin.site.register(AboutUs)


from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username', 'role', 'is_active')  # Columns to display
    search_fields = ('first_name', 'last_name', 'email', 'username')  # Fields for search
    list_filter = ('role', 'is_active')  # Add filters for better admin filtering

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

# Register the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)
##ContactUs
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'replied')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    fields = ('name', 'email', 'phone', 'subject', 'message', 'reply', 'created_at', 'replied')
    def save_model(self, request, obj, form, change):
        if 'reply' in form.changed_data:  # Check if reply was updated
            send_mail(
                subject=f"Reply to: {obj.subject}",
                message=obj.reply,
                from_email='rentmate55@gmail.com',  
                recipient_list=[obj.email],
                fail_silently=False,
            ) 
            obj.replied = True  # Mark as replied
        super().save_model(request, obj, form, change)

class PropertyImageInline(admin.TabularInline):
    """Allows adding multiple images inline in the admin panel."""
    model = PropertyImage
    extra = 3  # Show 3 empty slots for adding images

class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'unique_id', 'title', 'get_property_type_display', 'city', 'approval_status_symbol', 'approval_status'
    )
    list_editable = ('approval_status',)  # Allows editing approval status directly in the list view
    list_filter = ('approval_status', 'property_type', 'city', 'availability')
    search_fields = ('title', 'city', 'unique_id', 'street_address')
    readonly_fields = ('unique_id', 'created_at')
    inlines = [PropertyImageInline]  # Add inline images in admin panel

    def get_property_type_display(self, obj):
        """Display human-readable property type."""
        return obj.get_property_type_display()

    get_property_type_display.short_description = "Property Type"

    def approval_status_symbol(self, obj):
        """Display the approval status with symbols."""
        if obj.approval_status == 'approved':
            return format_html('<span style="color: green;">✅ Approved</span>')
        elif obj.approval_status == 'pending':
            return format_html('<span style="color: orange;">⏳ Pending</span>')
        elif obj.approval_status == 'rejected':
            return format_html('<span style="color: red;">❌ Rejected</span>')
        return obj.approval_status

    approval_status_symbol.short_description = "Approval Status Symbol"

    def display_images(self, obj):
        """Display multiple property images in the admin panel."""
        images = PropertyImage.objects.filter(property=obj)
        if images.exists():
            image_html = "".join([
                f'<img src="{img.image.url}" width="50" height="50" style="border-radius: 5px; margin: 2px;" />'
                for img in images[:5]  # Limit display to 3 images
            ])
            return format_html(image_html)
        return "No Images"
    
    display_images.short_description = "Property Images"

    def display_amenities(self, obj):
        """Show amenities as plain text."""
        if obj.amenities:
            return obj.amenities.replace(",", ", ")  # Show amenities as comma-separated text
        return "No Amenities"

    display_amenities.short_description = "Amenities"

# Register the Property model with the customized admin view
admin.site.register(PropertyDetail, PropertyAdmin)


