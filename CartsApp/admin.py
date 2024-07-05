from django.contrib import admin
from CartsApp.models import Cart,CartItem
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    '''Admin View for Cart'''
    list_display = ('cart_id','date_added',)

class CartItemAdmin(admin.ModelAdmin):
    '''Admin View for CartItem'''

    list_display = ('product','cart','quantity','is_active',)


admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
