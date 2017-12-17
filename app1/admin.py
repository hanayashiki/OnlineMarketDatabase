from django.contrib import admin
from app1.models import goods, managers, customers, orders, suppliers, contacts, supply_orders, complains
# Register your models here.


class customersAdmin(admin.ModelAdmin):
    list_display=('name','address','email')
    search_fields=('name','email')

admin.site.register(goods)
admin.site.register(managers)
admin.site.register(customers,customersAdmin)
admin.site.register(orders)
admin.site.register(suppliers)
admin.site.register(contacts)
admin.site.register(supply_orders)
admin.site.register(complains)
