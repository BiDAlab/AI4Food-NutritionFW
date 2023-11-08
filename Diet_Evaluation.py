"""
BiDA Lab - Universidad Autonoma de Madrid
Author: Sergio Romero-Tapiador
Creation Date: 23/10/2023
Last Modification: 08/11/2023
-----------------------------------------------------
This file contains the main functions of the Diet Evaluator using the Healthy Score. For more information, please refer
to the following GitHub repository: https://github.com/BiDAlab/AI4Food-NutritionFW
"""
import os
import numpy as np
import src.utils as utils
import matplotlib.pyplot as plt

# Obtain the current path
main_path = os.getcwd()
src_path = os.path.join(main_path, "src")
additional_path = os.path.join(src_path, "additional_files")

# Main function
if __name__ == '__main__':
    # Search the last dataset path and get the user list
    selected_dataset, dataset_path = utils.search_database(main_path)

    # Initialize the covariance matrix and the dataframe
    cov_matrix, df_taxonomy = utils.initialize_objects(additional_path)

    # Get the users diets
    user_diets = utils.get_user_diets(dataset_path, df_taxonomy)

    # Initialize the mahalanobis distance dictionary
    mahalanobis_dst = {}

    # For each user and week, calculate the mahalanobis distance
    for user in user_diets.keys():
        # Get the variable flag for variable profile diets
        variable = user_diets[user]["variable"]
        for week in user_diets[user].keys():
            if week != "profile" and week != "variable":
                # Convert the diet dict to a diet matrix and calculate the mahalanobis distance
                current_user_matrix = utils.get_matrix(user_diets[user][week])
                diet_type = user_diets[user][week]["profile"]

                if variable is True:
                    ID = user + "_" + week + "_" + "variable"
                else:
                    ID = user + "_" + week + "_" + diet_type

                mahalanobis_dst[ID] = utils.mahalanobis_distance(current_user_matrix, cov_matrix)

    # Apply log transformation to the mahalanobis distance values
    for key in mahalanobis_dst.keys():
        mahalanobis_dst[key] = np.log1p(mahalanobis_dst[key])

    # Normalize the mahalanobis distance values
    for key in mahalanobis_dst.keys():
        # If the mahalanobis distance is greater than the maximum value, assign the maximum value
        if mahalanobis_dst[key] > utils.max_value:
            mahalanobis_dst[key] = utils.max_value

        mahalanobis_dst[key] = (mahalanobis_dst[key] - utils.min_value) / (utils.max_value - utils.min_value)

    # Calculate the Healthy Score, which is 1 - mahalanobis_dst values
    healthy_score = {}
    for key in mahalanobis_dst.keys():
        healthy_score[key] = 1 - mahalanobis_dst[key]

    # Obtain a list of x and y values and a list of colors
    plot_lst_x = []
    plot_lst_y = []
    plot_lst_color = []

    # Iterate over the healthy score dictionary
    for key, healthy_score_value in healthy_score.items():
        # Append the healthy score value to the x list
        plot_lst_x.append(healthy_score_value)

        # Get the ID number and append it to the y list
        ID_number = int(key.split("_")[1])
        plot_lst_y.append(ID_number)

        # Get the profile
        profile = key.split("_")[-1]

        # Assign a color to each profile
        if profile == "healthy":
            plot_lst_color.append(utils.colors["Healthy"])  # Green color
        elif profile == "medium":
            plot_lst_color.append(utils.colors["Medium"])  # Yellow color
        elif profile == "unhealthy":
            plot_lst_color.append(utils.colors["Unhealthy"])  # Red color
        elif profile == "variable":
            plot_lst_color.append(utils.colors["Variable"])  # Blue color

    # Scatter plot the data using the x and y lists, limiting the x_axis to 0 and 1
    plt.scatter(plot_lst_x, plot_lst_y, c=plot_lst_color, marker="o")
    plt.axvline(x=0.4, color=utils.colors["DecisionBoundary"], linewidth=4)
    plt.xlim(0, 1)

    # Label and title the plot
    plt.title("Diet Evaluation of the \"" + selected_dataset + "\" Dataset", fontsize=utils.fontsize)
    plt.xlabel("Healthy Score based on Normalised Mahalanobis Distance (NMD)", fontsize=utils.fontsize)
    plt.ylabel("Subject's ID", fontsize=utils.fontsize)
    plt.legend(handles=[utils.healthy_patch, utils.medium_patch, utils.unhealthy_patch, utils.variable_patch,
                        utils.decboun_patch], prop={'size': utils.fontsize - 3})

    # Plot the data
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
