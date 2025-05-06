from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import timedelta
from decimal import Decimal

from .models import DishType, Ingredient, Dish, DishIngredient


# Create your tests here.
class ModelTests(TestCase):
    def setUp(self):
        # Create a test user (cook)
        self.cook = get_user_model().objects.create_user(
            username="testcook",
            password="testpassword",
            first_name="Test",
            last_name="Cook",
            years_of_experience=5,
        )

        # Create a dish type
        self.dish_type = DishType.objects.create(name="Test Dish Type")

        # Create an ingredient
        self.ingredient = Ingredient.objects.create(name="Test Ingredient")

        # Create a dish
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="This is a test dish",
            price=Decimal("9.99"),
            dish_type=self.dish_type,
            preparing_time=timedelta(minutes=30),
        )
        self.dish.cooks.add(self.cook)

        # Create a dish ingredient
        self.dish_ingredient = DishIngredient.objects.create(
            dish=self.dish, ingredient=self.ingredient, quantity=2.5
        )

    def test_cook_creation(self):
        """Test that a cook can be created"""
        self.assertEqual(self.cook.username, "testcook")
        self.assertEqual(self.cook.years_of_experience, 5)
        self.assertEqual(str(self.cook), "Test Cook (testcook)")

    def test_dish_type_creation(self):
        """Test that a dish type can be created"""
        self.assertEqual(self.dish_type.name, "Test Dish Type")
        self.assertEqual(str(self.dish_type), "Test Dish Type")

    def test_ingredient_creation(self):
        """Test that an ingredient can be created"""
        self.assertEqual(self.ingredient.name, "Test Ingredient")
        self.assertEqual(str(self.ingredient), "Test Ingredient")

    def test_dish_creation(self):
        """Test that a dish can be created"""
        self.assertEqual(self.dish.name, "Test Dish")
        self.assertEqual(self.dish.price, Decimal("9.99"))
        self.assertEqual(self.dish.dish_type, self.dish_type)
        self.assertEqual(self.dish.preparing_time, timedelta(minutes=30))
        self.assertEqual(self.dish.cooks.count(), 1)
        self.assertEqual(str(self.dish), "Test Dish - 9.99")

    def test_dish_ingredient_creation(self):
        """Test that a dish ingredient can be created"""
        self.assertEqual(self.dish_ingredient.dish, self.dish)
        self.assertEqual(self.dish_ingredient.ingredient, self.ingredient)
        self.assertEqual(self.dish_ingredient.quantity, 2.5)
        self.assertEqual(str(self.dish_ingredient), "Test Dish - Test Ingredient (2.5)")


class ViewTests(TestCase):
    def setUp(self):
        # Create a test user (cook)
        self.cook = get_user_model().objects.create_user(
            username="testcook",
            password="testpassword",
            first_name="Test",
            last_name="Cook",
            years_of_experience=5,
        )

        # Create a dish type
        self.dish_type = DishType.objects.create(name="Test Dish Type")

        # Create an ingredient
        self.ingredient = Ingredient.objects.create(name="Test Ingredient")

        # Create a dish
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="This is a test dish",
            price=Decimal("9.99"),
            dish_type=self.dish_type,
            preparing_time=timedelta(minutes=30),
        )
        self.dish.cooks.add(self.cook)

        # Create a client
        self.client = Client()

    def test_login_required(self):
        """Test that login is required for accessing views"""
        # Test index view
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test dish list view
        response = self.client.get(reverse("dish-list"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_authenticated_access(self):
        """Test that authenticated users can access views"""
        # Log in
        self.client.login(username="testcook", password="testpassword")

        # Test index view
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

        # Test dish list view
        response = self.client.get(reverse("dish-list"))
        self.assertEqual(response.status_code, 200)

    def test_dish_crud(self):
        """Test CRUD operations for dishes"""
        # Log in
        self.client.login(username="testcook", password="testpassword")

        # Test dish creation
        dish_data = {
            "name": "New Test Dish",
            "description": "This is a new test dish",
            "price": "12.99",
            "dish_type": self.dish_type.id,
            "cooks": [self.cook.id],
            "preparing_time": "00:45:00",
        }
        response = self.client.post(reverse("dish-create"), dish_data)
        self.assertEqual(Dish.objects.filter(name="New Test Dish").count(), 1)

        # Test dish update
        new_dish = Dish.objects.get(name="New Test Dish")
        update_data = {
            "name": "Updated Test Dish",
            "description": "This is an updated test dish",
            "price": "14.99",
            "dish_type": self.dish_type.id,
            "cooks": [self.cook.id],
            "preparing_time": "00:45:00",
        }
        response = self.client.post(
            reverse("dish-update", args=[new_dish.id]), update_data
        )
        self.assertEqual(Dish.objects.filter(name="Updated Test Dish").count(), 1)

        # Test dish deletion
        response = self.client.post(reverse("dish-delete", args=[new_dish.id]))
        self.assertEqual(Dish.objects.filter(name="Updated Test Dish").count(), 0)
