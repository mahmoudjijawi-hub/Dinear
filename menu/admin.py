from django.contrib import admin
from .models import Category, Product, Order, OrderItem


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'order']
    list_filter = ['category', 'is_available']
    search_fields = ['name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'quantity', 'unit_price', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']
