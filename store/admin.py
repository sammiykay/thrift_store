from django.contrib import admin
from .models import *


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(View)
admin.site.register(ContactUs)
admin.site.register(Shipping)
admin.site.register(DeliveryDriver)

# admin.site.site_header = "TF Temilorx Signature Admin"
# admin.site.site_title = "TF Temilorx Signature Admin Portal"
# admin.site.index_title = "Welcome to Computerized campus shopping intranet admin"
# Register your models here.

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['order', 'customer', 'status', 'delivery_method', 'delivery_date']
    list_filter = ['status', 'delivery_method']
    search_fields = ['order__transaction_id', 'customer__name']
    readonly_fields = ['order', 'customer', 'address']  # Prevent some fields from being edited

    def has_add_permission(self, request):
        # Disallow adding delivery records manually from the admin, since they should be auto-generated.
        return True