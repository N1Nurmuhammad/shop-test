from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.shop.models import *


class MembershipInline(admin.TabularInline):
    model = OrderModel.products.through


@admin.register(ClientModel)
class ClientModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = ["full_name", "birthdate"]
    search_fields = ["full_name", "birthdate"]


@admin.register(EmployeeModel)
class EmployeeModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = ["full_name", "birthdate"]
    search_fields = ["full_name", "birthdate"]


@admin.register(ProductModel)
class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = ["name", "quantity", "price"]
    search_fields = ["name", "quantity", "price"]


@admin.register(OrderModel)
class OrderModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = ["client", "employee", "price", "date"]
    search_fields = ["client__name", "employee__name", "price", "date"]
    raw_id_fields = ["client", "products", "employee"]
    date_hierarchy = "date"
    inlines = [MembershipInline]
