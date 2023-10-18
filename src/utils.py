"""
BiDA Lab - Universidad Autonoma de Madrid
Author: Sergio Romero-Tapiador
Creation Date: 23/09/2022
Last Modification: 17/10/2023
-----------------------------------------------------
This file contains the additional functions used in the framework.
"""

import os
import sys
import random
import pandas as pd

# Define the list of regions
region_lst = ["INTERNATIONAL", "CENTRAL ASIA", "EAST AND SOUTHEAST ASIA", "EUROPE", "LATIN AMERICA AND THE CARIBBEAN",
              "NORTH AFRICA AND WEST ASIA", "NORTH AMERICA"]
total_regions = len(region_lst)

# Define the global variables
num_subjects = 0
current_num_subjects = 0


# Transforms a week number into a string
def week_in2_str(week): return "week_" + str(week).zfill(1)


# Transforms a day number into a string
def day_in2_str(week): return "day_" + str(week).zfill(2)


# Transforms a meal number into a string
def meal_in2_str(meal): return "meal_" + str(meal).zfill(1)


# Checks if a string is a float number
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


# Creates the main directory of the dataset
def create_directory(path):
    ID_dataset = 0
    main_path = os.path.join(path, "AI4Food-NutritionFW Dataset_" + str(ID_dataset).zfill(3))
    check_main_directory = True

    while check_main_directory:
        if not os.path.exists(main_path):
            os.makedirs(main_path)
            check_main_directory = False
        else:
            main_path = os.path.join(path, "AI4Food-NutritionFW Dataset_" + str(ID_dataset).zfill(3))
            ID_dataset += 1

    return main_path


# Define the user's preferences in case the food group parameters is template mode
def template_mode_preferences(df_template):
    # Create a dictionary with the user's preferences
    user_preferences_dict = {"profiles": {}, "num_profiles": 0}

    # Iterate over each profile
    for index, row in df_template.iterrows():
        user_preferences_dict["profiles"][index] = {}
        user_preferences_dict["profiles"][index] = row

        user_preferences_dict["num_profiles"] += 1

    return user_preferences_dict


# Define the user's preferences in case the food group parameters is user_defined
def user_defined_preferences():
    # Parameters initialization
    n_unhealthy_subjects = 0
    n_medium_subjects = 0
    n_variable_subjects = 0

    # Define the general parameters of the framework:
    # Number of total subjects
    while True:
        try:
            num_subjects = int(input("Please, enter the number of subjects: "))
            if 1 <= num_subjects <= 100000:
                break
            else:
                print("The number of subjects must be between 1 and 100,000. Try again...")
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

    # Number of meals in a day (between 2 and 7)
    while True:
        try:
            n_meals = input(
                "Please, enter the number of meals in a day (between 2 and 7). Press enter to use a default number: ")
            if n_meals == "":
                n_meals = 5
                break

            n_meals = int(n_meals)
            if 2 <= n_meals <= 7:
                break
            else:
                print("The number of meals in a day must be between 2 and 7. Try again...")
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

    # Number of main meals in a day (between 1 and 3)
    while True:
        try:
            n_main_meals = input(
                "Please, enter the number of main meals in a day (between 1 and 3). Press enter to use a default "
                "number: ")
            if n_main_meals == "":
                n_main_meals = 2
                break

            n_main_meals = int(n_main_meals)

            if 1 <= n_main_meals <= 3:
                break
            else:
                print("The number of main meals in a day must be between 1 and 3. Try again...")
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

    # Territorial region of the dataset
    while True:
        try:
            print("Please, enter the territorial region of the dataset:\n- 0. DEFAULT")
            for i in range(len(region_lst)):
                print("- " + str(i + 1) + ". " + region_lst[i])
            territory = int(input())
            if 0 <= territory <= len(region_lst):
                break
            else:
                print("The territorial region of the dataset must be between 0 and " + str(
                    len(region_lst)) + ". Try again...")
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

    # Define the specific parameters of the framework in case the food group parameters is template mode:
    # Number of healthy subjects
    while True:
        try:
            n_healthy_subjects = int(
                input("Please, enter the number of healthy subjects (from a total of " + str(num_subjects) + "): "))
            if 0 <= n_healthy_subjects <= num_subjects:
                break
            else:
                print("The number of healthy subjects must be between 0 and " + str(num_subjects) + ". Try again...")
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

    if n_healthy_subjects != num_subjects:
        # Number of unhealthy subjects
        while True:
            try:
                n_unhealthy_subjects = int(
                    input("Please, enter the number of unhealthy subjects (from a total of " + str(
                        num_subjects - n_healthy_subjects) + "): "))
                if 0 <= n_unhealthy_subjects <= num_subjects - n_healthy_subjects:
                    break
                else:
                    print("The number of unhealthy subjects must be between 0 and " + str(
                        num_subjects - n_healthy_subjects) + ". Try again...")
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")

        if n_healthy_subjects + n_unhealthy_subjects != num_subjects:
            # Number of medium subjects
            while True:
                rest_subjects = num_subjects - n_healthy_subjects - n_unhealthy_subjects
                try:
                    n_medium_subjects = int(input(
                        "Please, enter the number of medium profile subjects (from a total of " + str(
                            rest_subjects) + "): "))
                    if 0 <= n_medium_subjects <= rest_subjects:
                        break
                    else:
                        print("The number of medium profile subjects must be between 0 and " + str(
                            rest_subjects) + ". Try again...")
                except ValueError:
                    print("Oops!  That was no valid number.  Try again...")

            # Compute the number of variable subjects
            if n_healthy_subjects + n_unhealthy_subjects + n_medium_subjects == num_subjects:
                n_variable_subjects = 0
            else:
                n_variable_subjects = rest_subjects - n_medium_subjects

    # Create a dictionary with the user's preferences
    user_preferences_dict = {"num_subjects": num_subjects, "n_meals": n_meals, "n_main_meals": n_main_meals,
                             "territory": territory, "n_healthy_subjects": n_healthy_subjects,
                             "n_unhealthy_subjects": n_unhealthy_subjects, "n_medium_subjects": n_medium_subjects,
                             "n_variable_subjects": n_variable_subjects}

    return user_preferences_dict


# Create a function that allows to define the user's preferences
def user_preferences(path):
    # Define template or user_defined mode
    while True:
        try:
            user_defined_template_mode = int(
                input("Please, select User-defined (0) or Template (1) mode. Remind that Template mode reads "
                      "the file \"Profile_dataset_example.xlsx\": "))
            if user_defined_template_mode == 0 or user_defined_template_mode == 1:
                break
            else:
                print("The number must be either 0 (User-defined) or 1 (Template) mode. Try again...")
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

    # Define the general parameters of the framework regarding the user_defined/template mode:
    if user_defined_template_mode == 0:
        user_preferences_dict = user_defined_preferences()
    else:
        # Read the profile dataset example
        try:
            df = pd.read_excel(os.path.join(path, "Profile_dataset_example.xlsx"))
        except FileNotFoundError:
            raise Exception(
                "The file \"Profile_dataset_example.xlsx\" is not in the main folder. Review the main folder.")

        user_preferences_dict = template_mode_preferences(df)

    user_preferences_dict["user_defined_template_mode"] = user_defined_template_mode

    return user_preferences_dict


# Parse each food parameter from the profile template mode
def unzip_values(value):
    if value == "-":
        min_value = -1
        max_value = -1
    elif isfloat(value):
        min_value = float(value)
        max_value = float(value)
    elif value[0].isdigit() and value[2].isdigit() and value[1] == "-":
        min_value = float(value[0])
        max_value = float(value[2])
    else:
        raise TypeError("The value " + value + " is not valid. Try again...")

    return min_value, max_value


# Select a random number between two values from a list
def select_random_number(lst_values):
    # Check if lst_values is a list and has only two values
    if isinstance(lst_values, list) and len(lst_values) == 2:
        min_value, max_value = lst_values
        return random.randint(min_value, max_value)
    else:
        return None


# Select a list of "freq" random numbers between 0 and num
def select_values_from_n_freq(num, freq, sum_value):
    # Check if freq is higher than num_days
    if freq >= num:
        times = freq // num
        rest = freq % num

        lst_selected_values = list(range(0 + sum_value, num + sum_value)) * times
        lst_selected_values += random.sample(range(0 + sum_value, num + sum_value), rest)
        return lst_selected_values
    else:
        return random.sample(range(1, num + sum_value), freq)


# Parse the profile template
def get_profiles_dict(df_profile):
    # Create a dict of profiles
    profiles_dict = {}

    # Create as variables as columns of the profile template
    for column in df_profile.columns:
        profiles_dict[column] = {}

    # Iterate over rows of the profile template
    for index, row in df_profile.iterrows():
        # Iterate over a series, extracting both the index and the value
        for column, value in row.iteritems():
            if column == "diet_type" or column == "region" or column == "secondary_profile" or column == "":
                # Check if the number of rows is 1
                if len(df_profile.index) == 1:
                    profiles_dict[column] = value
                else:
                    profiles_dict[column][int(index + 1)] = value
            else:
                min_value, max_value = unzip_values(value)
                if len(df_profile.index) == 1:
                    profiles_dict[column] = [min_value, max_value]
                else:
                    profiles_dict[column][int(index + 1)] = [min_value, max_value]

    return profiles_dict


# Search the food group in the taxonomy dataframe
def search_food_group_in_taxonomy(df_taxonomy, key):
    # Search the key in df_taxonomy in the root, category and subcategory columns
    food_group = df_taxonomy.loc[
        (df_taxonomy['root'] == key) | (df_taxonomy['category'] == key) | (
                df_taxonomy['subcategory'] == key)]

    # Reset the index
    food_group = food_group.reset_index(drop=True)

    if food_group is None:
        raise Exception("The food group " + key + " is not in the taxonomy. Review the taxonomy file.")

    # Get number of rows
    num_rows = food_group.shape[0]

    return food_group, num_rows


# Obtain a random food product image from the database
def get_random_food_product_image(product, ddbb_path):
    product_path = os.path.join(ddbb_path, product["category"], product["subcategory"])
    products_list = os.listdir(product_path)
    products_filtered = []

    # Get all the products that match with the product name and the abbreviated database
    for current_product in products_list:
        if product["product"] in current_product and product["abbreviated_database"] in current_product:
            products_filtered.append(current_product)

    if len(products_filtered) == 0:
        raise Exception(
            "The product " + product["product"] + " is not in the product folder. Review the product folder.")

    # Return a random product
    return random.choice(products_filtered), product_path


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd='\r'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()


# Update the number of subjects
def update_num_subjects(value):
    global num_subjects
    num_subjects = value


# Update the current number of subjects
def update_current_num_subjects():
    global current_num_subjects
    current_num_subjects += 1


# Initialize the current number of subjects
def initialize_current_num_subjects():
    global current_num_subjects
    current_num_subjects = 0


