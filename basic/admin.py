from django.contrib import admin

from .models import User, Cart, Stock

# Register your models here
admin.site.site_header = "Silki Store | Admin"

class UserAdmin(admin.ModelAdmin):
   list_display = ["first_name", "last_name", "email", "phone_number", "is_admin", "is_active", "is_staff", "is_superuser"]
   search_fields = ["first_name", "last_name", "email", "phone_number", "is_admin", "is_active", "is_staff", "is_superuser"]
   list_filter = ["is_admin", "is_staff", "is_active"]
   list_editable = ["email", "phone_number", "is_admin", "is_active", "is_staff", "is_superuser"]

class StockAdmin(admin.ModelAdmin):
    fields = ["id", "name", "type", "img", "img1", "img2", "img3", "img4", "img5", "store", "price", "offer"]
    list_display = ["id", "name", "type", "img", "img1", "img2", "img3", "img4", "img5", "store", "price", "offer"]
    search_fields = ["id", "name", "type", "img", "img1", "img2", "img3", "img4", "img5", "store", "price", "offer"]
    list_filter = ["id", "name", "type", "img", "img1", "img2", "img3", "img4", "img5", "store", "price", "offer"]




admin.site.register(User,UserAdmin)

admin.site.register(Stock, StockAdmin)

admin.site.register(Cart)


