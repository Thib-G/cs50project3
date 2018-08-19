from django.contrib import admin

from .models import Category, Item, Topping, Pricing, Cart

# Register your models here.


class ItemInLine(admin.TabularInline):
    """Show items in tabular format"""
    model = Item
    extra = 1


class PricingInLine(admin.TabularInline):
    """ Show pricing in tabular format"""
    model = Pricing
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    """List categories with the following fields"""
    list_display = ['category_name', 'order_nr']
    inlines = [ItemInLine]


class ItemAdmin(admin.ModelAdmin):
    """List items with the following fields"""
    list_display = ['item_name', 'category', 'max_toppings']
    inlines = [PricingInLine]


class CartAdmin(admin.ModelAdmin):
    """List items added to cart"""
    filter_horizontal = ('pricing_items',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Topping)
admin.site.register(Cart, CartAdmin)
