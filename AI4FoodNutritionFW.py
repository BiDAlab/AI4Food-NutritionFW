"""
BiDA Lab - Universidad Autonoma de Madrid
Author: Sergio Romero-Tapiador
Creation Date: 23/09/2022
Last Modification: 17/10/2023
-----------------------------------------------------
This file contains the main functions of the AI4Food-Nutrition Framework. For more information, please refer to the
following GitHub repository: https://github.com/BiDAlab/AI4Food-NutritionFW
"""
# Import Libraries
import os
import time
import random
import shutil
import pandas as pd

import src.utils as utils
import src.AI4FoodNutritionFW_classes as classes

# Get the main path and additional paths
main_path = os.getcwd()
src_path = os.path.join(main_path, "src")
additional_path = os.path.join(src_path, "additional_files")

# Load the food products database
df_taxonomy = pd.read_csv(os.path.join(additional_path, "Nutritional_Level_Taxonomy.csv"), sep=",")


# Compute the subject's diet
def compute_subject_diet(subject_diet, profile_conf):
    # First, compute the number of days per week
    for current_week in range(1, subject_diet.weeks + 1):
        # Initialize the week's structure
        dish_class = classes.Dish()
        food_parameter_class = classes.FoodGroupParameters(profile_conf)
        food_parameters = food_parameter_class.get_food_groups_params()
        days_week = subject_diet.diets[utils.week_in2_str(current_week)].days_week

        # For each food parameter, select a random type of dish
        for key, freq in list(food_parameters.items()):
            food_group, num_rows = utils.search_food_group_in_taxonomy(df_taxonomy, key)

            # Manage the food groups with a lower nutritional level of 5
            if food_group.iloc[0]["nutritional_level"] < 5:
                # If there is only one row, add the dish to the subject diet directly
                if num_rows == 1:
                    if freq == 1:
                        dish_class.add_dish(key, food_group.iloc[0]["dish_type"])
                    else:
                        for i in range(freq):
                            dish_class.add_dish(key, food_group.iloc[0]["dish_type"])

                # If there are more than one row, select one of them randomly
                else:
                    if freq == 1:
                        row_selected = random.randint(0, num_rows - 1)
                        dish = food_group.iloc[row_selected]["subcategory"]
                        dish_type = food_group.iloc[row_selected]["dish_type"]
                        dish_class.add_dish(dish, dish_type)
                    # In case of more than one frequency, select as many as possible
                    else:
                        lst_rows = utils.select_values_from_n_freq(num_rows, freq, sum_value=0)
                        for i in lst_rows:
                            dish = food_group.iloc[i]["subcategory"]
                            dish_type = food_group.iloc[i]["dish_type"]
                            dish_class.add_dish(dish, dish_type)

                # Finally delete the food group from the food_parameters dictionary
                del food_parameters[key]

        # Then, assign the dish to the subject diet
        all_dish_types = dish_class.get_all_dishes()
        # For each dish type, select a random dish among the available ones and place it in a random day of the week
        for current_dish_type, current_dishes in all_dish_types.items():
            random.shuffle(current_dishes)
            lst_days = utils.select_values_from_n_freq(days_week, len(current_dishes), sum_value=1)

            for current_dish in current_dishes:
                subject_diet.diets[utils.week_in2_str(current_week)].diet[
                    utils.day_in2_str(lst_days.pop(0))].add_new_predish(current_dish, current_dish_type)

        # Second, manage the food groups with a nutritional level of 5 or higher
        for key, freq in list(food_parameters.items()):
            if freq[0] != -1:
                # If frequency is higher than 1, select the days when the dish will be placed
                for current_day in range(1, days_week + 1):
                    new_freq = utils.select_random_number(freq)

                    food_group, num_rows = utils.search_food_group_in_taxonomy(df_taxonomy, key)
                    # If there is only one row, add the dish to the subject diet directly
                    if num_rows == 1:
                        if new_freq == 1:
                            subject_diet.diets[utils.week_in2_str(current_week)].diet[
                                utils.day_in2_str(current_day)].add_new_predish(key, food_group.iloc[0]["dish_type"])
                        else:
                            for i in range(new_freq):
                                subject_diet.diets[utils.week_in2_str(current_week)].diet[
                                    utils.day_in2_str(current_day)].add_new_predish(key,
                                                                                    food_group.iloc[0]["dish_type"])

                    # If there are more than one row, select one of them randomly
                    else:
                        if new_freq == 1:
                            row_selected = random.randint(0, num_rows - 1)
                            dish = food_group.iloc[row_selected]["subcategory"]
                            dish_type = food_group.iloc[row_selected]["dish_type"]

                            subject_diet.diets[utils.week_in2_str(current_week)].diet[
                                utils.day_in2_str(current_day)].add_new_predish(dish, dish_type)
                        # In case of more than one dish, select as many as possible
                        else:
                            lst_rows = utils.select_values_from_n_freq(num_rows, new_freq, sum_value=0)
                            for i in lst_rows:
                                dish = food_group.iloc[i]["subcategory"]
                                dish_type = food_group.iloc[i]["dish_type"]
                                subject_diet.diets[utils.week_in2_str(current_week)].diet[
                                    utils.day_in2_str(current_day)].add_new_predish(dish, dish_type)

            # Finally delete the food group from the food_parameters dictionary
            del food_parameters[key]


# Balance the subject's diet
def balance_subject_diet(subject_diet, profile_conf):
    # First, obtain the maximum number of meals with food products categorised as main dishes
    max_meals_with_main_dishes = utils.select_random_number(profile_conf["max_meals_with_main_dishes"])

    # Second, obtain the maximum number of food products categorised as main dishes per meal
    max_main_dishes_per_meal = utils.select_random_number(profile_conf["max_main_dishes_per_meal"])

    # Balance the dishes into the different days of the week
    for current_week in range(1, subject_diet.weeks + 1):
        current_week_str = utils.week_in2_str(current_week)
        days_week = subject_diet.diets[current_week_str].days_week

        for current_day in range(1, days_week + 1):
            current_day_str = utils.day_in2_str(current_day)
            all_dishes = subject_diet.diets[current_week_str].diet[current_day_str].get_pre_dishes()
            total_meals = list(subject_diet.diets[current_week_str].diet[current_day_str].get_meals().keys())
            len_meals = len(total_meals)

            # First, balance the "main" dishes
            main_dishes = all_dishes["main"]
            random.shuffle(main_dishes)

            lst_meals = utils.select_values_from_n_freq(len_meals, max_meals_with_main_dishes, sum_value=1)
            lst_meals *= max_meals_with_main_dishes
            main_dishes_in_meals = []

            # Place the main dishes in the different meals of the day, considering some restrictions previously defined
            for current_dish in main_dishes:
                if len(lst_meals) != 0:
                    current_meal = utils.meal_in2_str(lst_meals.pop(0))
                    flag_break = True
                    while flag_break:
                        if subject_diet.diets[current_week_str].diet[current_day_str].get_num_current_dishes("main",
                                                                                                             current_meal) < max_main_dishes_per_meal:
                            # Finally add the main dish to the subject diet
                            subject_diet.diets[current_week_str].diet[current_day_str].add_new_dish(current_dish,
                                                                                                    "main",
                                                                                                    current_meal)
                            flag_break = False

                            if current_meal not in main_dishes_in_meals:
                                main_dishes_in_meals.append(current_meal)
                        else:
                            if len(lst_meals) != 0:
                                current_meal = utils.meal_in2_str(lst_meals.pop(0))
                            else:
                                flag_break = False

            # Second, balance the bread dishes
            bread_dishes = all_dishes["bread"]
            random.shuffle(total_meals)
            for current_bread in bread_dishes:
                for current_meal in total_meals:
                    if current_meal in main_dishes_in_meals:
                        if subject_diet.diets[current_week_str].diet[current_day_str].get_num_current_dishes("bread",
                                                                                                             current_meal) == 0:
                            # Finally add the bread to the subject diet
                            subject_diet.diets[current_week_str].diet[current_day_str].add_new_dish(current_bread,
                                                                                                    "bread",
                                                                                                    current_meal)
                            break

            # Third, balance the "side" dishes
            side_dishes = all_dishes["side"]
            random.shuffle(total_meals)
            for current_side in side_dishes:
                for current_meal in total_meals:
                    if current_meal in main_dishes_in_meals:
                        if subject_diet.diets[current_week_str].diet[current_day_str].get_num_current_dishes("side",
                                                                                                             current_meal) == 0:
                            # Finally add the side dish to the subject diet
                            subject_diet.diets[current_week_str].diet[current_day_str].add_new_dish(current_side,
                                                                                                    "side",
                                                                                                    current_meal)
                            break

            # Fourth, balance the "dessert" dishes
            dessert_dishes = all_dishes["dessert"]
            random.shuffle(total_meals)
            for current_dessert in dessert_dishes:
                for current_meal in total_meals:
                    if subject_diet.diets[current_week_str].diet[current_day_str].get_num_current_dishes("dessert",
                                                                                                         current_meal) == 0:
                        # Finally add the dessert to the subject diet
                        subject_diet.diets[current_week_str].diet[current_day_str].add_new_dish(current_dessert,
                                                                                                "dessert",
                                                                                                current_meal)
                        break

            # Fifth, balance the "drink" dishes
            drink_dishes = all_dishes["drinks"]
            random.shuffle(total_meals)
            for current_drink in drink_dishes:
                for current_meal in total_meals:
                    if subject_diet.diets[current_week_str].diet[current_day_str].get_num_current_dishes("drinks",
                                                                                                         current_meal) == 0:
                        # Finally add the drinks to the subject diet
                        subject_diet.diets[current_week_str].diet[current_day_str].add_new_dish(current_drink,
                                                                                                "drinks",
                                                                                                current_meal)
                        break

            # Sixth, balance the "appetizer" dishes
            appetizer_dishes = all_dishes["appetizer"]
            random.shuffle(total_meals)
            for current_appetizer in appetizer_dishes:
                for current_meal in total_meals:
                    if current_meal not in main_dishes_in_meals:
                        if subject_diet.diets[current_week_str].diet[current_day_str].get_num_current_dishes(
                                "appetizer",
                                current_meal) == 0:
                            # Finally add the appetizers to the subject diet
                            subject_diet.diets[current_week_str].diet[current_day_str].add_new_dish(current_appetizer,
                                                                                                    "appetizer",
                                                                                                    current_meal)
                            break

            # Seventh, balance the "snack" dishes
            snack_dishes = all_dishes["snack"]
            random.shuffle(total_meals)
            for current_snack in snack_dishes:
                for current_meal in total_meals:
                    if current_meal not in main_dishes_in_meals:
                        if subject_diet.diets[current_week_str].diet[current_day_str].get_num_current_dishes(
                                "snack",
                                current_meal) == 0:
                            # Finally add the snacks to the subject diet
                            subject_diet.diets[current_week_str].diet[current_day_str].add_new_dish(current_snack,
                                                                                                    "snack",
                                                                                                    current_meal)
                            break

            # Remove the pre-dishes from the subject diet
            del subject_diet.diets[current_week_str].diet[current_day_str].pre_dishes

            # Finally, remove empty meals and renumber the meals
            subject_diet.diets[current_week_str].diet[current_day_str].remove_empty_meals()


# Generate the final subject food image dataset from the food image database (AI4Food-NutritionDB)
def generate_dataset_from_food_image_db(json_dict, ddbb_path, subject_path):
    # Iterate over the subject's diet, from weeks to the different dishes that compose the diet
    df_ddbb = pd.read_csv(os.path.join(additional_path, "AI4Food-NutritionFW_Categorisation.csv"), sep=",")
    for current_week in json_dict["diets"]:
        for current_day in json_dict["diets"][current_week]["meals"]:
            for current_meal in json_dict["diets"][current_week]["meals"][current_day]:
                for current_dish_type in json_dict["diets"][current_week]["meals"][current_day][current_meal]:
                    for current_dish in json_dict["diets"][current_week]["meals"][current_day][current_meal][
                        current_dish_type]:
                        # Replace some specific subcategories
                        if "Subcategory" in current_dish:
                            current_dish = current_dish.replace(" Subcategory", "")

                        # Search the current dish in df_ddbb in the subcategory column, considering their specific region
                        food_group = df_ddbb.loc[(df_ddbb['subcategory'] == current_dish)
                                                 & ((df_ddbb['region'] == json_dict["region"]) | (
                                df_ddbb['region'] == "INTERNATIONAL"))]

                        # Reset the index
                        food_group = food_group.reset_index(drop=True)

                        # Get number of rows
                        num_rows = food_group.shape[0]

                        while num_rows == 0:
                            # Some specific cases
                            if current_dish == "Other Salty Snacks":
                                current_dish = "Salty Snacks"
                            elif current_dish == "Dumpling" or current_dish == "Pie":
                                mixed_food_lst = ["Stuffed Dough", "Fried Food", "Mixed Meat"]
                                current_dish = random.choice(mixed_food_lst)

                            # Search the current dish in df_ddbb in the subcategory column, considering their specific region
                            food_group = df_ddbb.loc[
                                (df_ddbb['category'] == current_dish) | (df_ddbb['subcategory'] == current_dish)
                                & ((df_ddbb['region'] == json_dict["region"]) | (
                                        df_ddbb['region'] == "INTERNATIONAL"))]

                            # Reset the index
                            food_group = food_group.reset_index(drop=True)

                            # Get number of rows
                            num_rows = food_group.shape[0]

                        # Select a random product
                        if num_rows == 1:
                            row_selected = 0
                        else:
                            row_selected = random.randint(0, num_rows - 1)

                        # Select a random image from the product
                        food_product_image, food_product_path = utils.get_random_food_product_image(
                            food_group.iloc[row_selected],
                            ddbb_path)

                        # Copy the image into the subject folder
                        final_product_name = current_dish + "_" + current_meal + "_" + current_day + "_" + current_week + ".jpg"
                        product_final_path = os.path.join(subject_path, current_week, current_day, current_meal)
                        final_img_path = os.path.join(product_final_path, final_product_name)
                        src_path = os.path.join(food_product_path, food_product_image)

                        if not os.path.isdir(product_final_path):
                            os.makedirs(product_final_path)

                        # Finally, copy the image into the subject folder
                        shutil.copy(src_path, final_img_path)


# Subject diet generation
def generate_subject_diet(ID, region, profile_conf, diet_type, variable_flag, dataset_path):
    # Create the subject directory
    subject_path = os.path.join(dataset_path, "Subject_" + ID)
    os.makedirs(subject_path)

    if variable_flag:
        total_weeks = profile_conf["regularity_weeks"][0] + profile_conf["regularity_weeks"][1]
    else:
        total_weeks = profile_conf["regularity_weeks"][0]

    # Initialize the subject diet
    subject_diet = classes.Subject(ID, region, profile_conf, diet_type, variable_flag,
                                   total_weeks)

    # Compute the diet for the corresponding subject
    compute_subject_diet(subject_diet, profile_conf)

    # Balance the diet
    balance_subject_diet(subject_diet, profile_conf)

    # Save the subject's diet into a json file
    json_dict = subject_diet.save_subject_diet(subject_path)

    # Generate the food image dataset with the corresponding subject diet
    ddbb_path = os.path.join(main_path, "AI4Food-NutritionDB")
    if os.path.isdir(ddbb_path):
        generate_dataset_from_food_image_db(json_dict, ddbb_path, subject_path)

    # Update the current number of subjects and print the progress bar
    utils.print_progress_bar(utils.current_num_subjects + 1, utils.num_subjects, prefix='Progress:',
                             suffix='Complete', length=50)
    utils.update_current_num_subjects()


# Generate the subjects' diets according to the user_defined user preferences
def user_defined_preferences(user_defined_dict, path):
    # Load the profile template
    df_profile = pd.read_excel(os.path.join(additional_path, "Profile_template.xlsx"))

    # Make the column "diet_type" the index of the df_profile
    df_profile = df_profile.set_index("diet_type")

    # Obtain the profiles dictionary
    healthy_profile_conf = utils.get_profiles_dict(df_profile.loc["healthy"].to_frame().T)
    unhealthy_profile_conf = utils.get_profiles_dict(df_profile.loc["unhealthy"].to_frame().T)
    medium_profile_conf = utils.get_profiles_dict(df_profile.loc["medium"].to_frame().T)
    variable_profile_conf = utils.get_profiles_dict(df_profile.loc["variable"].to_frame().T)

    check_unhealthy_subjects = user_defined_dict['n_unhealthy_subjects'] + user_defined_dict[
        'n_healthy_subjects']
    check_medium_subjects = check_unhealthy_subjects + user_defined_dict['n_medium_subjects']

    # Assign the regions to the subjects
    # If 0, the regions will be randomly assigned
    if user_defined_dict['territory'] == 0:
        healthy_regions_lst = random.choices(range(0, utils.total_regions), k=user_defined_dict['n_healthy_subjects'])
        unhealthy_regions_lst = random.choices(range(0, utils.total_regions),
                                               k=user_defined_dict['n_unhealthy_subjects'])
        medium_regions_lst = random.choices(range(0, utils.total_regions), k=user_defined_dict['n_medium_subjects'])
        variable_regions_lst = random.choices(range(0, utils.total_regions), k=user_defined_dict['n_variable_subjects'])

        healthy_regions_lst = [utils.region_lst[i] for i in healthy_regions_lst]
        unhealthy_regions_lst = [utils.region_lst[i] for i in unhealthy_regions_lst]
        medium_regions_lst = [utils.region_lst[i] for i in medium_regions_lst]
        variable_regions_lst = [utils.region_lst[i] for i in variable_regions_lst]

    else:
        current_region = utils.region_lst[user_defined_dict['territory'] - 1]
        healthy_regions_lst = [current_region] * user_defined_dict['n_healthy_subjects']
        unhealthy_regions_lst = [current_region] * user_defined_dict['n_unhealthy_subjects']
        medium_regions_lst = [current_region] * user_defined_dict['n_medium_subjects']
        variable_regions_lst = [current_region] * user_defined_dict['n_variable_subjects']

    # Initialize the current number of subjects and the total number of subjects
    utils.initialize_current_num_subjects()
    utils.update_num_subjects(user_defined_dict['num_subjects'])

    # Print the progress bar
    utils.print_progress_bar(utils.current_num_subjects, utils.num_subjects, prefix='Progress:',
                           suffix='Complete', length=50)

    # Generate the subjects' diets
    for subject in range(0, user_defined_dict['num_subjects']):

        # Healthy subject
        if subject < user_defined_dict['n_healthy_subjects']:
            region = healthy_regions_lst.pop(0)
            generate_subject_diet(str(subject).zfill(6), region, healthy_profile_conf, "healthy",
                                  False, path)

            # Unhealthy subject
        elif user_defined_dict['n_healthy_subjects'] <= subject < check_unhealthy_subjects:
            region = unhealthy_regions_lst.pop(0)
            generate_subject_diet(str(subject).zfill(6), region, unhealthy_profile_conf, "unhealthy",
                                  False, path)

        # Medium subject
        elif check_unhealthy_subjects <= subject < check_medium_subjects:
            region = medium_regions_lst.pop(0)
            generate_subject_diet(str(subject).zfill(6), region, medium_profile_conf, "medium", False,
                                  path)

        # Variable subject
        else:
            region = variable_regions_lst.pop(0)
            generate_subject_diet(str(subject).zfill(6), region, variable_profile_conf, "healthy",
                                  True, path)


# Generate the subjects' diets according to the template mode user preferences
def template_mode_preferences(template_dict, path):
    current_subject_ID = 0

    # For each profile defined in the xlsx file, generate the corresponding number of subjects
    for index, current_profile in enumerate(template_dict["profiles"]):
        print("\nGenerating the subjects' diets for the profile " + str(index + 1) + "...")

        # Initialize the current number of subjects and the total number of subjects
        utils.initialize_current_num_subjects()
        utils.update_num_subjects(template_dict["profiles"][current_profile]["num_subjects"])

        # Print the progress bar
        utils.print_progress_bar(utils.current_num_subjects, utils.num_subjects, prefix='Progress:',
                                 suffix='Complete', length=50)
        for _ in range(template_dict["profiles"][current_profile]["num_subjects"]):
            # Define the region
            # If the region is "all", the region will be randomly assigned
            if template_dict["profiles"][current_profile]["region"] == "all":
                region = utils.region_lst[random.randint(0, utils.total_regions - 1)]
            else:
                region = utils.region_lst.index(template_dict["profiles"][current_profile]["region"])

            # Obtain the profile configuration and the diet type
            current_profile_dict = utils.get_profiles_dict(template_dict["profiles"][current_profile].to_frame().T)
            current_diet_type = template_dict["profiles"][current_profile]["diet_type"]

            # Check if the subject's diet is variable or not
            if template_dict["profiles"][current_profile]["secondary_profile"] == "None" or \
                    template_dict["profiles"][current_profile]["secondary_profile"] == "none":
                variable_flag = False
            else:
                variable_flag = True

            # Finally, generate the subject's diet
            generate_subject_diet(str(current_subject_ID).zfill(6), region, current_profile_dict, current_diet_type,
                                  variable_flag, path)
            current_subject_ID += 1


if __name__ == '__main__':
    # Obtain the user preferences
    user_preferences_dict = utils.user_preferences(additional_path)

    print("Generating the food image database...")

    # Check if the AI4Food-NutritionDB has been downloaded and placed in the main directory
    check_path = os.path.join(main_path, "AI4Food-NutritionDB")
    if not os.path.isdir(check_path):
        print("The AI4Food-NutritionDB has not been downloaded. The json dataset will be generated instead.")

    # Set the path where the dataset will be generated
    dataset_path = utils.create_directory(main_path)

    # Generate the food image database
    if user_preferences_dict['user_defined_template_mode'] == 0:
        user_defined_preferences(user_preferences_dict, dataset_path)
    # In case the user wants to generate the dataset automatically
    else:
        template_mode_preferences(user_preferences_dict, dataset_path)

    # Print the final message
    print("\n\nThe dataset has been generated successfully in the following path: " + dataset_path)