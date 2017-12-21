from django.contrib import admin
from app1.models import Goods, Managers, Customers, Orders, Suppliers, Contacts, Supply_orders, Complaints
# Register your models here.


class customersAdmin(admin.ModelAdmin):
    list_display=('name','address','email')
    search_fields=('name','email')

admin.site.register(Goods)
admin.site.register(Managers)
admin.site.register(Customers,customersAdmin)
admin.site.register(Orders)
admin.site.register(Suppliers)
admin.site.register(Contacts)
admin.site.register(Supply_orders)
admin.site.register(Complaints)
