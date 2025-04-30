from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cook, DishType, Ingredient, Dish, DishIngredient


admin.site.register(Cook, UserAdmin)
admin.site.register(DishType)
admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(DishIngredient)
