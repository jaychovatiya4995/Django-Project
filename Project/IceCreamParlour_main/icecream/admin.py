from django.contrib import admin
from .models import Icecream, Size, Product, Category


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Icecream)
admin.site.register(Size)
admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)

