from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

"""The manager class is the go between the database and the models. Every
model needs at least one manager class. Django adds one per model by default
but if you need special behaviour you can override it like in this file"""


class UserManager(BaseUserManager):

    """These methods are accessed through the .objects property on the model"""

    def create_user(self, email, password=None, **extra_fields):
        """Validates, creates and saves a new user """
        if not email:
            raise ValueError('User must have an email address')

        """self.model is short hand for creating a new user model,
        as it accesses the model propertery teh class is for"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Create a super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    """Needed to make sure our custom manager is used for this custom model"""
    objects = UserManager()

    """USERNAME_FIELD is manditory so swaps the value out for email"""
    USERNAME_FIELD = 'email'


class Ingredient(models.Model):
    """Ingredient model to be used in a recipe"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    """This manager has been added for saving of the
    Recipe model with ingredients"""

    def _create_ingredients_for_name_on_recipe(self, ingredient_names, recipe):
        if ingredient_names:
            for ingredient_name in ingredient_names:
                recipe.ingredients.create(name=ingredient_name)

    def create_recipe_with_ingredients(
            self, name, description, ingredient_names):
        """First saves a simple recipe then adds
        the ingredient for the one to many relationship"""

        recipe = self.model(
            name=name,
            description=description,
        )
        recipe.save(using=self.db)

        self._create_ingredients_for_name_on_recipe(ingredient_names, recipe)

        return recipe

    def update_recipe_ingredients(self, recipe_instance, ingredient_names):
        """First remove all current ingredients"""
        if recipe_instance.ingredients:
            for ingredient_model in recipe_instance.ingredients.all():
                recipe_instance.ingredients.remove(ingredient_model)
                ingredient_model.delete()

        """Then create the new replacement ingredients"""
        self._create_ingredients_for_name_on_recipe(
            ingredient_names=ingredient_names,
            recipe=recipe_instance,
        )

        return recipe_instance


class Recipe(models.Model):
    """Recipe object to be used to create recipes"""

    objects = RecipeManager()

    class Meta:
        """This is now immutable as Django wished to
        remove the relationship to a ingredient now
        auto_create=True"""
        managed = False

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientForARecipe'
    )

    def __str__(self):
        return self.name


class IngredientForARecipe(models.Model):
    """This join model allows a single ingredient to be related to a
    recipe in a one-to-many way"""

    class Meta:
        """The way in which I have got this to work smells
        like a hack but I reckon it will give me the outcome
        I want where  this join is created automatically
        for me without the need for any extra code"""
        managed = False
        auto_created = True

    Recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    Ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
