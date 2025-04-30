from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from .models import Dish, DishType, Cook, Ingredient, DishIngredient


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "kitchen/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dishes_count"] = Dish.objects.count()
        context["dish_types_count"] = DishType.objects.count()
        context["cooks_count"] = Cook.objects.count()
        context["ingredients_count"] = Ingredient.objects.count()
        context["background_image"] = True
        return context


# Dish views
class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "kitchen/dish_list.html"
    context_object_name = "dishes"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(dish_type__name__icontains=search_query)
            )
        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"
    context_object_name = "dish"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredient_list"] = Ingredient.objects.all()
        return context


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    fields = [
        "name", "description", "price",
        "dish_type", "cooks", "preparing_time"
    ]
    success_url = reverse_lazy("dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    fields = [
        "name", "description", "price",
        "dish_type", "cooks", "preparing_time"
    ]

    def get_success_url(self):
        return reverse_lazy("dish-detail", kwargs={"pk": self.object.pk})


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("dish-list")


# DishType views
class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_types"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    template_name = "kitchen/dish_type_form.html"
    fields = ["name"]
    success_url = reverse_lazy("dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "kitchen/dish_type_form.html"
    fields = ["name"]
    success_url = reverse_lazy("dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("dish-type-list")


# Ingredient views
class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    template_name = "kitchen/ingredient_list.html"
    context_object_name = "ingredients"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    template_name = "kitchen/ingredient_form.html"
    fields = ["name"]
    success_url = reverse_lazy("ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    template_name = "kitchen/ingredient_form.html"
    fields = ["name"]
    success_url = reverse_lazy("ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    template_name = "kitchen/ingredient_confirm_delete.html"
    success_url = reverse_lazy("ingredient-list")


# DishIngredient views
@login_required
def add_ingredient_to_dish(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)

    if request.method == "POST":
        ingredient_id = request.POST.get("ingredient")
        quantity = request.POST.get("quantity")

        if ingredient_id and quantity:
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            DishIngredient.objects.create(
                dish=dish,
                ingredient=ingredient,
                quantity=float(quantity)
            )

    return redirect("dish-detail", pk=dish_id)


@login_required
def remove_ingredient_from_dish(request, dish_id, ingredient_id):
    dish_ingredient = get_object_or_404(
        DishIngredient,
        dish_id=dish_id,
        ingredient_id=ingredient_id
    )
    dish_ingredient.delete()

    return redirect("dish-detail", pk=dish_id)


# Cook views
class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    template_name = "kitchen/cook_list.html"
    context_object_name = "cooks"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    template_name = "kitchen/cook_detail.html"
    context_object_name = "cook"


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    template_name = "kitchen/cook_form.html"
    fields = [
        "username", "password", "first_name",
        "last_name", "email", "years_of_experience"
    ]
    success_url = reverse_lazy("cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    template_name = "kitchen/cook_form.html"
    fields = [
        "first_name", "last_name",
        "email", "years_of_experience"
    ]

    def get_success_url(self):
        return reverse_lazy("cook-detail", kwargs={"pk": self.object.pk})
