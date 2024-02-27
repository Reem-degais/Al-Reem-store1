from django.contrib import admin
from .models import Payment, Order, OrderProducts

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProducts
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'is_ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProducts)