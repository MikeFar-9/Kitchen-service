from django.shortcuts import redirect
from django.urls import path

from . import views


urlpatterns = [
    # Index
    path("", views.IndexView.as_view(), name="index"),

    # Dish URLs
    path("dishes/", views.DishListView.as_view(), name="dish-list"),
    path(
        "dishes/<int:pk>/",
        views.DishDetailView.as_view(),
        name="dish-detail"
    ),
    path("dishes/create/", views.DishCreateView.as_view(), name="dish-create"),
    path(
        "dishes/<int:pk>/update/",
        views.DishUpdateView.as_view(),
        name="dish-update"
    ),
    path(
        "dishes/<int:pk>/delete/",
        views.DishDeleteView.as_view(),
        name="dish-delete"
    ),

    # DishType URLs
    path(
        "dish-types/",
        views.DishTypeListView.as_view(),
        name="dish-type-list"
    ),
    path(
        "dish-types/create/",
        views.DishTypeCreateView.as_view(),
        name="dish-type-create"
    ),
    path(
        "dish-types/<int:pk>/update/",
        views.DishTypeUpdateView.as_view(),
        name="dish-type-update"
    ),
    path(
        "dish-types/<int:pk>/delete/",
        views.DishTypeDeleteView.as_view(),
        name="dish-type-delete"
    ),

    # Ingredient URLs
    path(
        "ingredients/",
        views.IngredientListView.as_view(),
        name="ingredient-list"
    ),
    path(
        "ingredients/create/",
        views.IngredientCreateView.as_view(),
        name="ingredient-create"
    ),
    path(
        "ingredients/<int:pk>/update/",
        views.IngredientUpdateView.as_view(),
        name="ingredient-update"
    ),
    path(
        "ingredients/<int:pk>/delete/",
        views.IngredientDeleteView.as_view(),
        name="ingredient-delete"
    ),

    # DishIngredient URLs
    path(
        "dishes/<int:dish_id>/add-ingredient/",
        views.add_ingredient_to_dish,
        name="add-ingredient-to-dish"
    ),
    path(
        "dishes/<int:dish_id>/remove-ingredient/<int:ingredient_id>/",
        views.remove_ingredient_from_dish,
        name="remove-ingredient-from-dish"
    ),

    # Cook URLs
    path("cooks/", views.CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>/", views.CookDetailView.as_view(), name="cook-detail"),
    path("cooks/create/", views.CookCreateView.as_view(), name="cook-create"),
    path(
        "cooks/<int:pk>/update/",
        views.CookUpdateView.as_view(),
        name="cook-update"
    ),
]

urlpatterns += [
    path("login/", lambda request: redirect("/accounts/login/")),
]
