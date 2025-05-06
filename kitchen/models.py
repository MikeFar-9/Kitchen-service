from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class Cook(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.username})"


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    cooks = models.ManyToManyField(
        Cook,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="DishIngredient",
        related_name="dishes"
    )
    preparing_time = models.DurationField()

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ["dish", "ingredient"]

    def __str__(self) -> str:
        return f"{self.dish.name} - {self.ingredient.name} ({self.quantity})"
