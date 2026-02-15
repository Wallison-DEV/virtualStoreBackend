from django.contrib import admin
from .models import OrderItemModel, OrderModel

class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    # Campos que o admin não deve editar manualmente
    readonly_fields = ('price_at_purchase',)
    extra = 0

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'status', 'total_amount', 'created_at')
    readonly_fields = ('pix_code', 'bar_code', 'total_amount', 'status')
    inlines = [OrderItemInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, OrderItemModel):
                instance.price_at_purchase = instance.product.base_price
            instance.save()
        form.instance.save() 