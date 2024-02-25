from django.contrib import admin
from .models import Payment, Order, OrderProducts

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProducts
    extra = 0
    readonly_fields = ('payment', 'user', 'prpduct', 'quantity', 'product_price', 'is_ordered')

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProducts)