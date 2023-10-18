"""
BiDA Lab - Universidad Autonoma de Madrid
Author: Sergio Romero-Tapiador
Creation Date: 23/09/2022
Last Modification: 17/10/2023
-----------------------------------------------------
This file contains the classes used in the AI4FoodNutrition framework. The classes are:
    - Subject: Contains the information of a subject, i.e., the ID, the region, the number of weeks, and the diet.
    - Diet: Contains specific information of the diet such as the number of days per week, the number of meals per day, and the
            type of diet (healthy, unhealthy, or medium).
    - Meal: Contains the number of dishes per meal and the dishes that compose the meal.
    - Dish: Contains the dishes of the meal. Concrete, the main dish, the bread, the dessert, the drinks, the appetizer, the
            snack, and the side dish.
    - FoodGroupParameters: Contains the parameters of the food groups of the AI4FoodNutrition framework.
"""

import os.path
import random
import collections
import src.utils as utils

"""
Class Subject: Contains the information of a subject, i.e., the ID, the region, the number of weeks, and the diet.
"""


class Subject:
    # Constructor
    def __init__(self, ID, region, profile_conf, diet_type, variable_flag, weeks):
        self.ID = ID
        self.profile_conf = profile_conf
        self.region = region
        self.weeks = int(weeks)
        self.diets = collections.OrderedDict()

        diet_type_weeks = [diet_type] * self.weeks

        # Assign a random secondary profile if it is not defined
        if variable_flag:
            if profile_conf["secondary_profile"] == "none" or profile_conf["secondary_profile"] == "None":
                if diet_type == "healthy":
                    profile_conf["secondary_profile"] = random.choice(["unhealthy", "medium"])
                elif diet_type == "unhealthy":
                    profile_conf["secondary_profile"] = random.choice(["healthy", "medium"])
                elif diet_type == "medium":
                    profile_conf["secondary_profile"] = random.choice(["healthy", "unhealthy"])

            # Random sample of weeks to be irregular
            irregular_weeks = random.sample(range(0, self.weeks), int(profile_conf["regularity_weeks"][1]))

            # Put the secondary profile in the irregular weeks
            for week in irregular_weeks:
                diet_type_weeks[week] = profile_conf["secondary_profile"]

        # Initialize the diet for every week
        for i in range(self.weeks):
            # Initialize the current week's diet
            days_week = random.randint(profile_conf["days_week"][0], profile_conf["days_week"][1])
            if days_week > 7:
                raise ValueError("The number of days per week cannot be greater than 7")
            self.diets[utils.week_in2_str(i + 1)] = Diet(days_week,
                                                         profile_conf["num_meals"], diet_type_weeks[i])

    # Save the subject's diet in a json file
    def save_subject_diet(self, path):
        dictionary_to_save = {"ID": self.ID, "region": self.region, "weeks": self.weeks, "diets": {}}

        for week in self.diets:
            dictionary_to_save["diets"][week] = {}
            dictionary_to_save["diets"][week]["diet_type"] = self.diets[week].diet_type
            dictionary_to_save["diets"][week]["days_week"] = self.diets[week].days_week
            dictionary_to_save["diets"][week]["meals"] = {}

            for day in self.diets[week].diet:
                dictionary_to_save["diets"][week]["meals"][day] = self.diets[week].diet[day].get_meals_json()

        import json
        filepath = os.path.join(path, "Subject_" + str(self.ID).zfill(3) + ".json")
        with open(filepath, 'w') as outfile:
            json.dump(dictionary_to_save, outfile, indent=4)

        return dictionary_to_save


"""
The class Diet contains specific information of the diet such as the number of days per week, the number of meals per day, and the
type of diet (healthy, unhealthy, or medium).
"""


class Diet:
    # Constructor
    def __init__(self, days_week, num_meals, diet_type):
        self.diet = collections.OrderedDict()
        self.diet_type = diet_type
        self.days_week = days_week

        # For every day of the week
        for day in range(1, days_week + 1):
            day_str = utils.day_in2_str(day)
            current_num_meals = random.randint(num_meals[0], num_meals[1])
            self.diet[day_str] = Meal(current_num_meals)

    # Add a new dish to the diet, indicating the dish type, the day, and the corresponding meal
    def add_new_dish(self, dish, dish_type, day, meal):
        day_str = utils.day_in2_str(day)
        self.diet[day_str].add_new_dish(dish, dish_type, meal)

    # Remove a dish from the diet
    def remove_dish(self, dish, dish_type, day, meal):
        day_str = utils.day_in2_str(day)
        self.diet[day_str].remove_dish(dish, dish_type, meal)


"""
The class Meal contains the number of dishes per meal and the dishes that compose the meal.
"""


class Meal:
    # Constructor
    def __init__(self, num_meals):
        self.pre_dishes = Dish()
        self.meal = collections.OrderedDict()

        # For every meal of the day
        for current_meal in range(1, num_meals + 1):
            meal_str = utils.meal_in2_str(current_meal)
            self.meal[meal_str] = Dish()

    # Add a new dish to the meal, indicating the dish type and the corresponding meal
    def add_new_dish(self, dish, dish_type, meal_number):
        if "meal" in str(meal_number):
            meal_str = meal_number
        else:
            meal_str = utils.meal_in2_str(meal_number)

        self.meal[meal_str].add_dish(dish, dish_type)

    # Add a new dish to the pre-dishes temporary object
    def add_new_predish(self, dish, dish_type):
        self.pre_dishes.add_dish(dish, dish_type)

    # Remove a dish from the meal
    def remove_dish(self, dish, dish_type, meal_number):
        if "meal" in str(meal_number):
            meal_str = meal_number
        else:
            meal_str = utils.meal_in2_str(meal_number)
        # Remove specific meal
        return self.meal[meal_str].remove_dish(dish, dish_type)

    # Get the current number of dishes per meal and dish type
    def get_num_current_dishes(self, dish_type, meal_number):
        if "meal" in str(meal_number):
            meal_str = meal_number
        else:
            meal_str = utils.meal_in2_str(meal_number)

        if dish_type == "main":
            return len(self.meal[meal_str].main)
        elif dish_type == "bread":
            return len(self.meal[meal_str].bread)
        elif dish_type == "dessert":
            return len(self.meal[meal_str].dessert)
        elif dish_type == "drinks":
            return len(self.meal[meal_str].drinks)
        elif dish_type == "appetizer":
            return len(self.meal[meal_str].appetizer)
        elif dish_type == "snack":
            return len(self.meal[meal_str].snack)
        elif dish_type == "side":
            return len(self.meal[meal_str].side_dish)
        else:
            raise ValueError("Dish type not recognized")

    # Get the current number of pre-dishes
    def get_num_current_pre_dishes(self, dish_type):
        if dish_type == "main":
            return len(self.pre_dishes.main)
        elif dish_type == "bread":
            return len(self.pre_dishes.bread)
        elif dish_type == "dessert":
            return len(self.pre_dishes.dessert)
        elif dish_type == "drinks":
            return len(self.pre_dishes.drinks)
        elif dish_type == "appetizer":
            return len(self.pre_dishes.appetizer)
        elif dish_type == "snack":
            return len(self.pre_dishes.snack)
        elif dish_type == "side":
            return len(self.pre_dishes.side_dish)
        else:
            raise ValueError("Dish type not recognized")

    # Get the pre-dishes temporary object
    def get_pre_dishes(self):
        return self.pre_dishes.get_all_dishes()

    # Get all meals
    def get_meals(self):
        dict_meals = {}
        for current_meal in self.meal.keys():
            dict_meals[current_meal] = self.meal[current_meal].get_all_dishes()

        return dict_meals

    # Get all meals in json format
    def get_meals_json(self):
        dict_meals = {}
        for current_meal in self.meal.keys():
            dict_meals[current_meal] = self.meal[current_meal].get_all_dishes_json()

        return dict_meals

    # Remove empty meals and reorganize them
    def remove_empty_meals(self):
        # First, delete empty meals
        for meal in list(self.meal.keys()):
            if self.meal[meal].get_number_dishes() == 0:
                del self.meal[meal]

        # Then, reorganize the meals
        count = 1
        for current_meal in list(self.meal.keys()):
            meal_number = int(current_meal.split("_")[-1])

            if meal_number != count:
                meal_str = utils.meal_in2_str(count)
                self.meal[meal_str] = self.meal.pop(current_meal)
            count += 1


"""
The class Dish contains the dishes of the meal. Concrete, the main dish, the bread, the dessert, the drinks, the appetizer, the
snack, and the side dish.
"""


class Dish:
    # Constructor
    def __init__(self):
        self.main = []
        self.bread = []
        self.dessert = []
        self.drinks = []
        self.appetizer = []
        self.snack = []
        self.side_dish = []

    # Add a new dish to the meal, indicating the dish type
    def add_dish(self, dish, dish_type):
        if str(dish_type).lower() == "main":
            self.main.append(dish)
        elif str(dish_type).lower() == "bread":
            self.bread.append(dish)
        elif str(dish_type).lower() == "dessert":
            self.dessert.append(dish)
        elif str(dish_type).lower() == "drinks":
            self.drinks.append(dish)
        elif str(dish_type).lower() == "appetizer":
            self.appetizer.append(dish)
        elif str(dish_type).lower() == "snack":
            self.snack.append(dish)
        elif str(dish_type).lower() == "side":
            self.side_dish.append(dish)
        else:
            raise ValueError("The dish type " + str(dish_type) + " is not valid")

    # Remove a dish from a dish type
    def remove_dish(self, dish, dish_type):
        if dish_type == "main":
            if dish in self.main:
                self.main.remove(dish)
        elif dish_type == "bread":
            if dish in self.bread:
                self.bread.remove(dish)
        elif dish_type == "dessert":
            if dish in self.dessert:
                self.dessert.remove(dish)
        elif dish_type == "drinks":
            if dish in self.drinks:
                self.drinks.remove(dish)
        elif dish_type == "appetizer":
            if dish in self.appetizer:
                self.appetizer.remove(dish)
        elif dish_type == "snack":
            if dish in self.snack:
                self.snack.remove(dish)
        elif dish_type == "side":
            if dish in self.side_dish:
                self.side_dish.remove(dish)
        else:
            return False

        return True

    # Get all dishes
    def get_all_dishes(self):
        all_dishes = {"main": self.main, "bread": self.bread, "dessert": self.dessert, "drinks": self.drinks,
                      "appetizer": self.appetizer, "snack": self.snack, "side": self.side_dish}

        return all_dishes

    # Get all dishes in json format
    def get_all_dishes_json(self):
        all_dishes = {}

        if len(self.main) > 0:
            all_dishes["main"] = self.main

        if len(self.bread) > 0:
            all_dishes["bread"] = self.bread

        if len(self.dessert) > 0:
            all_dishes["dessert"] = self.dessert

        if len(self.drinks) > 0:
            all_dishes["drinks"] = self.drinks

        if len(self.appetizer) > 0:
            all_dishes["appetizer"] = self.appetizer

        if len(self.snack) > 0:
            all_dishes["snack"] = self.snack

        if len(self.side_dish) > 0:
            all_dishes["side"] = self.side_dish

        return all_dishes

    # Get the total number of dishes
    def get_number_dishes(self):
        return len(self.main) + len(self.bread) + len(self.dessert) + len(self.drinks) + len(self.appetizer) + len(
            self.snack) + len(self.side_dish)


"""
The class FoodGroupParameters contains the parameters of the food groups of the AI4FoodNutrition framework.
"""


class FoodGroupParameters:
    # Constructor
    def __init__(self, profile_conf):
        self.food_params = collections.OrderedDict()

        # First level food groups
        self.food_params["First Level"] = utils.select_random_number(profile_conf["first_level"])
        self.food_params["Sweet Products"] = utils.select_random_number(profile_conf["sweet_products"])
        self.food_params["Dairy Dessert"] = utils.select_random_number(profile_conf["dairy_dessert"])
        self.food_params["Pastries"] = utils.select_random_number(profile_conf["pastries"])
        self.food_params["Chocolate Products"] = utils.select_random_number(profile_conf["chocolate_products"])
        self.food_params["Fruit Dessert"] = utils.select_random_number(profile_conf["fruit_dessert"])
        self.food_params["Other Sweet Products"] = utils.select_random_number(profile_conf["other_sweet_products"])
        self.food_params["Fast Food"] = utils.select_random_number(profile_conf["fast_food"])
        self.food_params["Burger"] = utils.select_random_number(profile_conf["burger"])
        self.food_params["Pizza"] = utils.select_random_number(profile_conf["pizza"])
        self.food_params["Hot Dog"] = utils.select_random_number(profile_conf["hot_dog"])
        self.food_params["Fries"] = utils.select_random_number(profile_conf["fries"])
        self.food_params["Vegetable Snacks"] = utils.select_random_number(profile_conf["vegetable_snacks"])
        self.food_params["Bean Snacks"] = utils.select_random_number(profile_conf["bean_snacks"])
        self.food_params["Other Salty Snacks"] = utils.select_random_number(profile_conf["other_salty_snacks"])
        self.food_params["Pate"] = utils.select_random_number(profile_conf["pate"])
        self.food_params["Sauce"] = utils.select_random_number(profile_conf["sauce"])
        self.food_params["Sugary Drinks"] = utils.select_random_number(profile_conf["sugary_drinks"])
        self.food_params["Other Drinks"] = utils.select_random_number(profile_conf["other_drinks"])

        # Second level food groups
        self.food_params["Second Level"] = utils.select_random_number(profile_conf["second_level"])
        self.food_params["Fatty Meat"] = utils.select_random_number(profile_conf["fatty_meat"])
        self.food_params["Red Meat"] = utils.select_random_number(profile_conf["red_meat"])
        self.food_params["Breaded Meat"] = utils.select_random_number(profile_conf["breaded_meat"])
        self.food_params["Varied Meat"] = utils.select_random_number(profile_conf["varied_meat"])
        self.food_params["Sausage"] = utils.select_random_number(profile_conf["sausage"])
        self.food_params["Mixed Meat"] = utils.select_random_number(profile_conf["mixed_meat"])
        self.food_params["Dumpling"] = utils.select_random_number(profile_conf["dumpling"])
        self.food_params["Pie"] = utils.select_random_number(profile_conf["pie"])
        self.food_params["Stuffed Dough"] = utils.select_random_number(profile_conf["stuffed_dough"])
        self.food_params["Fried Food"] = utils.select_random_number(profile_conf["fried_food"])
        self.food_params["Coffee"] = utils.select_random_number(profile_conf["coffee"])
        self.food_params["Alcoholic Drinks"] = utils.select_random_number(profile_conf["alcoholic_drinks"])

        # Third level food groups
        self.food_params["Third Level"] = utils.select_random_number(profile_conf["third_level"])
        self.food_params["Sandwich and Similar"] = utils.select_random_number(profile_conf["sandwich_N_similar"])
        self.food_params["Sandwich"] = utils.select_random_number(profile_conf["sandwich"])
        self.food_params["Wrap"] = utils.select_random_number(profile_conf["wrap"])
        self.food_params["Fried Seafood"] = utils.select_random_number(profile_conf["fried_seafood"])
        self.food_params["Fried Beans"] = utils.select_random_number(profile_conf["fried_beans"])
        self.food_params["Fried Dairy Products"] = utils.select_random_number(profile_conf["fried_dairy_products"])
        self.food_params["Fried or Breaded Fish"] = utils.select_random_number(profile_conf["fried_or_breaded_fish"])
        self.food_params["Toast"] = utils.select_random_number(profile_conf["toast"])
        self.food_params["Other Types of Bread"] = utils.select_random_number(profile_conf["other_types_of_bread"])
        self.food_params["Other Types of Salad"] = utils.select_random_number(profile_conf["other_types_of_salad"])
        self.food_params["Rice and Meat"] = utils.select_random_number(profile_conf["rice_N_meat"])
        self.food_params["Meat and Vegetables"] = utils.select_random_number(profile_conf["meat_N_vegetables"])
        self.food_params["Mixed Food"] = utils.select_random_number(profile_conf["mixed_food"])
        self.food_params["Vegetable Drinks"] = utils.select_random_number(profile_conf["vegetable_drinks"])

        # Fourth level food groups
        self.food_params["Fourth Level"] = utils.select_random_number(profile_conf["fourth_level"])
        self.food_params["Soups and Stews"] = utils.select_random_number(profile_conf["soups_N_stews"])
        self.food_params["Soups and Creams"] = utils.select_random_number(profile_conf["soups_N_creams"])
        self.food_params["Stews"] = utils.select_random_number(profile_conf["stews"])
        self.food_params["Fish and Seafood"] = utils.select_random_number(profile_conf["fish_N_seafood"])
        self.food_params["Varied Fish"] = utils.select_random_number(profile_conf["varied_fish"])
        self.food_params["Mixed Fish"] = utils.select_random_number(profile_conf["mixed_fish"])
        self.food_params["Mollusk"] = utils.select_random_number(profile_conf["mollusk"])
        self.food_params["Crustacean"] = utils.select_random_number(profile_conf["crustacean"])
        self.food_params["Varied Seafood"] = utils.select_random_number(profile_conf["varied_seafood"])
        self.food_params["Mixed Seafood"] = utils.select_random_number(profile_conf["mixed_seafood"])
        self.food_params["Beans"] = utils.select_random_number(profile_conf["beans"])
        self.food_params["Cooked Beans"] = utils.select_random_number(profile_conf["cooked_beans"])
        self.food_params["Mixed Beans"] = utils.select_random_number(profile_conf["mixed_beans"])
        self.food_params["Eggs Subcategory"] = utils.select_random_number(profile_conf["eggs_subcategory"])
        self.food_params["Eggs"] = utils.select_random_number(profile_conf["eggs"])
        self.food_params["Mixed Eggs"] = utils.select_random_number(profile_conf["mixed_eggs"])
        self.food_params["Dairy Products"] = utils.select_random_number(profile_conf["dairy_products"])
        self.food_params["Cheese"] = utils.select_random_number(profile_conf["cheese"])
        self.food_params["Yogurt"] = utils.select_random_number(profile_conf["yogurt"])
        self.food_params["White Meat"] = utils.select_random_number(profile_conf["white_meat"])
        self.food_params["Fried Vegetables"] = utils.select_random_number(profile_conf["fried_vegetables"])
        self.food_params["Nut Snacks"] = utils.select_random_number(profile_conf["nut_snacks"])
        self.food_params["Rice and Fish"] = utils.select_random_number(profile_conf["rice_N_fish"])
        self.food_params["Rice and Beans"] = utils.select_random_number(profile_conf["rice_N_beans"])
        self.food_params["Sushi"] = utils.select_random_number(profile_conf["sushi"])

        # Fifth level food groups
        self.food_params["Fifth Level"] = profile_conf["fifth_level"]
        self.food_params["Vegetables"] = profile_conf["vegetables"]
        self.food_params["Cooked Vegetables"] = profile_conf["cooked_vegetables"]
        self.food_params["Mixed Vegetables"] = profile_conf["mixed_vegetables"]
        self.food_params["Side Dish Salad"] = profile_conf["side_dish_salad"]
        self.food_params["Fruits"] = profile_conf["fruits"]

        # Sixth level food groups
        self.food_params["Sixth Level"] = profile_conf["sixth_level"]
        self.food_params["Noodle and Pasta"] = profile_conf["noodle_N_pasta"]
        self.food_params["Italian Pasta"] = utils.select_random_number(profile_conf["italian_pasta"])
        self.food_params["Noodle"] = profile_conf["noodle"]
        self.food_params["Other Types of Pasta"] = profile_conf["other_types_of_pasta"]
        self.food_params["Rice Subcategory"] = profile_conf["rice_subcategory"]
        self.food_params["Rice"] = profile_conf["rice"]
        self.food_params["Mixed Rice"] = profile_conf["mixed_rice"]
        self.food_params["Bread"] = profile_conf["bread"]

        self.remove_food_params()

    # Remove those food params that are not defined by the user
    def remove_food_params(self):
        for key in list(self.food_params.keys()):
            if self.food_params[key] == -1 or self.food_params[key] == 0:
                del self.food_params[key]

    # Obtain the food groups parameters
    def get_food_groups_params(self):
        return self.food_params
