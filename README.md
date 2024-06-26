# AI4Food-NutritionFW

Welcome to the AI4Food-NutritionFW GitHub repository!

## Introduction

<a href="http://atvs.ii.uam.es/atvs/">
    <img src="./media/BiDA-logo.png" alt="BiDA Lab" title="BiDA Lab" align="right" height="150" width="350" target="_blank"/>
</a>

In this repository, you will find a framework designed to create food image datasets according to configurable eating behaviours. The [AI4Food-NutritionFW framework](https://doi.org/10.1109/ACCESS.2023.3322770) considers various aspects such as region and lifestyle and simulates a user-friendly scenario where food images are taken using a smartphone. Additionally, it is supported by the [AI4Food-NutritionDB](https://github.com/BiDAlab/AI4Food-NutritionDB), a comprehensive nutrition database that includes food images and a nutrition taxonomy. 

For further details, please visit [our article](https://doi.org/10.1109/ACCESS.2023.3322770).

## Table of Contents

- [Overview](#overview)  
    - [AI4Food-NutritionFW Framework Description](#ai4foodfw)
    - [Eating Behaviour Configuration and Profile Creation](#firsts_modules)
    - [AI4Food-NutritionDB and Food Image Dataset Generation](#lasts_modules)
- [AI4Food-NutritionFW Framework User Guide](#ai4foodfw-guide)
    - [Framework Overview](#ai4foodfwguide-overview)
    - [Getting Started](#ai4foodfwguide-gst)
    - [Using the Framework](#ai4foodfwguide-use)
    - [Applications](#ai4foodfwguide-app)
    - [Troubleshooting](#ai4foodfwguide-trouble)
- [Citation](#cite)
- [Contact](#contact)

## <a name="overview">Overview<a>
Nowadays millions of images are shared on social media and web platforms. In particular, many of them are food images taken from a smartphone over time, providing information related to the individual's diet. On the other hand, eating behaviours are directly related to some of the most prevalent diseases in the world. Exploiting recent advances in image processing and Artificial Intelligence (AI), this scenario represents an excellent opportunity to: i) **create new methods that analyse the individuals' health from what they eat, and ii) develop personalised recommendations to improve nutrition and diet under specific circumstances (e.g., obesity or COVID)**. Having tunable tools for creating food image datasets that facilitate research in both lines is very much needed.

This repository proposes **AI4Food-NutritionFW, a framework for the creation of food image datasets according to configurable eating behaviours**. AI4Food-NutritionFW simulates a user-friendly and widespread scenario where images are taken using a smartphone. Finally, we automatically evaluate a healthy index of the subject's eating behaviours using multidimensional metrics based on guidelines for healthy diets proposed by international organisations.


### <a name="ai4foodfw">AI4Food-NutritionFW Framework Description<a>

<p align="center"><img src="./media/AI4Food-NutritionFW.png" alt="AI4Food-NutritionFW" title="AI4Food-NutritionFW Framework"/></p>

As illustrated in the figure above, first, we define the general and food group parameters of the proposed framework to model the different eating behaviour configurations. After that, modifying previous parameters, we can define different profiles. Finally, with the help of the **AI4Food-NutritionDB**, we can generate datasets with different eating behaviours, select the number of subjects and profiles as desired, or even create new ones. All these tasks are **tunable, allowing researchers to build their own datasets and include different configurations**. The entire software implementation was done in Python, ensuring accessibility for all users.

### <a name="firsts_modules">Eating Behaviour Configuration and Profile Creation<a>
We initially define the parameters of the AI4Food-NutritionFW to characterise the different eating behaviour profiles. Specifically, we define 2 types of parameters based on general and food-related aspects. First, we consider 6 general parameters that describe the structure of the diet, and second, we provide a parameter for each food group found on the nutritional pyramids (75 in total). Consequently, all 81 parameters considered in this work must be configured to define each eating behaviour profile. These parameters determine the daily and weekly frequency intake of the food products corresponding to the individual's eating behaviour. As guidelines from international organisations are based on daily and weekly recommendations, we determine that all diets must follow a 7-day diet, simulating a natural week. We describe next the details of the general and food group parameters. 

Finally, each parameter is then adjusted within a range of values that define a new profile. A final value associated with each parameter is randomly generated between each range in order to differentiate subjects from the same profile, and also to generate different eating behaviours. This task requires a preliminary analysis from a general (comparison among profiles) to a specific point of view to build a reliable dataset. For instance, healthy eating profiles have intake frequencies related to the healthy recommendations and therefore, the parameters will be set according to these guidances. 

After determining the range of values that characterise each profile, the next step computes the parameter values for each unique subject. Random values within the possible ones are then computed to obtain the frequency of each specific parameter, for instance, for a healthy profile with 50 subjects, between 3 and 5 meals, and between 4 and 6 fruits per day, the AI4Food-NutritionFW will be set to each subject a unique value in these ranges. In addition, a balancing process is then executed to have a realistic distribution of values: as parameters are related to food groups and food intake nutritional levels, each frequency is properly distributed among weeks and days.

### <a name="lasts_modules">AI4Food-NutritionDB and Food Image Dataset Generation<a>
One of the main contributions of the proposed **AI4Food-NutritionFW** is to simulate a real environment where people take a picture of food images, providing information related to their eating behaviours. This is done by automatically selecting food images based on the chosen configuration from a large pool of realistic and diverse images: the [AI4Food-NutritionDB database](https://github.com/BiDAlab/AI4Food-NutritionDB), the first database that considers food images and a nutrition taxonomy based on recommendations by national and international organisations, including four different categorisations: 6 different nutritional levels defined in accordance to the food intake frequency, 19 main food categories (e.g., “Meat”), 73 food subcategories (e.g., “White Meat”), and 893 final food products (e.g., “Chicken”). As the food group parameters of our proposed AI4Food-NutritionFW are directly related to the food image database, a food image of the corresponding group is randomly selected for each meal and day, recreating a realistic situation. The world region is the only restriction considered. Finally, this task is repeated among all the subjects and profiles designed previously and, as a result, a new dataset is generated.

## <a name="ai4foodfw-guide">AI4Food-NutritionFW Framework User Guide<a>
Welcome to the User Guide for the AI4Food-NutritionFW Framework, a powerful tool designed to assist you in generating food image datasets that simulate various eating behaviour diets. This comprehensive guide will help you understand the framework's purpose, how to use it effectively, and its potential applications.

### <a name="ai4foodfwguide-overview">Framework Overview

The AI4Food-NutritionFW Framework is a unique tool for creating food image datasets that simulate real-world eating behaviour diets. Key features and functionalities include:

- **User-defined and Template Modes:** Users can choose between User-defined mode, allowing customisation of dataset parameters, or Template mode, which utilises a pre-defined dataset template

- **User-Friendly:** The framework is designed to be user-friendly and does not require any prior programming skills.

- **Configurability:** Users can customise various dataset parameters, including the number of subjects, meals per day, main meals, and territorial regions.

### <a name="ai4foodfwguide-gst"> Installation and Initial Setup

To get started with the AI4Food-NutritionFW Framework, follow these steps:

1. **Download:** Download or clone this GitHub repository.

2. **Install Dependencies:** Ensure you have Python installed on your system. You can install any necessary Python packages by running the following command:

   ```bash
   pip install -r requirements.txt
   ```
    **Note that only pandas and openpyxl libraries are needed for the framework.**

3. **Download Data:** Download the [food image database](https://github.com/BiDAlab/AI4Food-NutritionDB) if you plan to generate image datasets. Alternatively, you can obtain the subjects' diet text data in JSON format describing food diets.


### <a name="ai4foodfwguide-use">Using the Framework

Follow these steps to use the AI4Food-NutritionFW Framework:

1. **Run the Framework:**

   Open your console or terminal and navigate to the directory where the framework is located. Run the following command:

   ```bash
   python AI4FoodNutritionFW.py
   ```

2. **Select Mode:**

   Upon running the program, you will be presented with an option to choose between **User-defined (0) or Template (1) mode**. In Template mode, a pre-defined dataset template is used.

    2.1. **User-defined Mode:**
    If you choose User-defined mode, you will be prompted for general dataset parameters. Here's what you need to input:
    
    - Number of subjects.
    - Number of meals in a day (between 2 and 7).
    - Number of main meals in a day (between 1 and 3).
    - Territorial region of the dataset (options provided).
    - Number of healthy subjects (from the total number of subjects).
    - If subjects already exist, specify the number of unhealthy subjects.
    - If subjects already exist, specify the number of medium profile subjects.
    
    The framework will then generate the dataset, displaying a progress bar.
    
    2.2. **Template Mode:**
    
    In Template mode, the framework will generate the dataset using the pre-defined template and display a progress bar. To modify or create a new dataset, you should edit the ["Profile_dataset_example.xlsx" file](https://github.com/BiDAlab/AI4Food-NutritionFW/blob/main/src/additional_files/Profile_dataset_example.xlsx). **Note that changes to this file will affect the entire dataset.**

3. **Completion:**

   Once the dataset generation is complete, the framework will display the message: "The dataset has been generated successfully in the following path: XXX," where XXX is the current path where the GitHub repository was downloaded.

Below is an illustrative example of the framework in action:

<p align="center"><img src="./media/AI4Food-NutritionFW Screenshot.jpg" alt="AI4Food-NutritionFW Screenshot" title="AI4Food-NutritionFW Screenshot"/></p>

### <a name="ai4foodfwguide-hs">Healthy Score
Finally, in order to obtain a score that quantifies the subject's eating behaviour, we compare the similarity of the subject's intake frequency of each food group with the optimal ranges. This is carried out using a Healthy Score based on the Normalised Mahalanobis Distance (*NMD*), where *NMD* is the [0,1] normalised value of the Mahalanobis Distance (*MD*). This distance calculates the similarity between a vector $x_i$ and a set of vectors represented by its mean $\bar{x}$ and Covariance matrix $C_x$ as follows:

<div align="center">
    
$MD_i = \sqrt{(x_i-\bar{x}) C_x^{-1} (x_i-\bar{x})^T}$
</div>


, where $x_i$ is a row vector of size 9 quantifying the 9 specific intakes for subject $i$, $\bar{x}$ is also a row vector of size 9 with the mean for the optimal range $\sigma_j$ for each type of intake $j=1,\ldots,9$, and $C_x=\sigma^T I \sigma$, where $\sigma=[\sigma_1,\ldots,\sigma_9]$ and $I$ is a $9\times9$ identity matrix. In our proposed approach, as implemented in the formulation above, $\bar{x}$ and $C_x$ values are obtained using the optimal ranges of each food group (following healthy recommendations) as this represents the ideal profile of healthy eating behaviour. 

The final Healthy Score is then calculated through the following equation:

<div align="center">
    
$HealthyScore = 1 - NMD$
</div>

As a result, Healthy Scores close to 1 mean healthy eating behaviours whereas Healthy Scores close to 0 mean unhealthy eating ones. In this repository, we include the [Healthy Score](https://github.com/BiDAlab/AI4Food-NutritionFW/blob/main/HealthyScore.py) to assess the eating behaviour diets generated from the AI4Food-NutritionFW. To use it, run the following command:

```bash
python HealthyScore.py
```

Then, all the generated datasets will be listed, allowing the user to select the desired one. The program calculates the Healthy Score by employing the Mahalanobis Distance to measure the similarity of a subject's diet to the optimal diet profile. 

<p align="center"><img src="./media/Healthy Score Program.jpg" alt="Healthy Score Program" title="Healthy Score Program"/></p>

Once the healthy scores have been computed, the program provides a visual representation of the dataset's healthiness, similar to the graph plotted in the [current paper](https://doi.org/10.1109/ACCESS.2023.3322770). Within this visualization, green represents healthy users, red indicates unhealthy users, yellow is for medium profile users, and orange is used to signify variable profiles. This visual representation enables users to identify the healthiness of individual diets and dietary patterns within the dataset. The program, by default, sets a decision boundary at 0.4 (0.36 in the paper), meaning that diets with a healthy score greater than 0.4 are classified as healthy. 

<p align="center"><img src="./media/Healthy Score Graph.jpeg" alt="Healthy Score Graph" title="Healthy Score Graph"/></p>

**It's important to note that the dataset you wish to evaluate must be placed in the same directory folder as the "HealthyScore.py" program.**

### <a name="ai4foodfwguide-app">Applications

The food image datasets generated with the AI4Food-NutrititonFW Framework have various applications, including:

- **Nutrition Research:** These datasets can be used to study eating behaviours and dietary choices in different regions, aiding in nutrition research.

- **Health Studies:** Researchers and healthcare professionals can analyse eating behaviours to better understand dietary preferences and their implications on health.

- **AI Research:** These datasets are valuable for training machine learning models to recognise and classify different foods, making them useful in AI research related to image recognition and diet analysis.

### <a name="ai4foodfwguide-trouble">Troubleshooting

If you encounter any issues while using the framework, here are some common troubleshooting steps:

1. **Check Dependencies:** Ensure that you have installed all required dependencies as mentioned in the installation section.

2. **Review Data:** Double-check your input data files, ensuring they are in the correct format and located in the expected directories.

3. **Contact us:** If you face technical challenges or have questions, consider contacting us for assistance.

## <a name="cite">Citation<a>
-**[AI4Food-NutritionFW_2023](https://doi.org/10.1109/ACCESS.2023.3322770)** S. Romero-Tapiador,  R. Tolosana, A. Morales, J. Fierrez, R. Vera-Rodriguez, I. Espinosa-Salinas, E. Carrillo-de Santa Pau, A. Ramirez-de Molina and J. Ortega-Garcia, **"AI4Food-NutritionFW: A Novel Framework for the Automatic Synthesis and Analysis of Eating Behaviours"**, *IEEE Access*, vol. 11, pp. 112199-112211, 2023.

```
@ARTICLE{romerotapiador2023ai4foodnutritionfw,
  author={Romero-Tapiador, Sergio and Tolosana, Ruben and Morales, Aythami and Fierrez, Julian and Vera-Rodriguez, Ruben and Espinosa-Salinas, Isabel and Freixer, Gala and Pau, Enrique Carrillo de Santa and De Molina, Ana Ramírez and Ortega-Garcia, Javier},
  journal={IEEE Access}, 
  title={AI4Food-NutritionFW: A Novel Framework for the Automatic Synthesis and Analysis of Eating Behaviours}, 
  year={2023},
  volume={11},
  pages={112199-112211},
  doi={10.1109/ACCESS.2023.3322770}}
  ```
    
All these articles are publicly available in the [publications](http://atvs.ii.uam.es/atvs/listpublications.do) section of the BiDA-Lab group webpage. Please, remember to reference the above articles on any work made public.
    
## <a name="contact">Contact<a>
  
For more information, please contact us via email at [sergio.romero@uam.es](mailto:sergio.romero@uam.es) or [ruben.tolosana@uam.es](mailto:ruben.tolosana@uam.es). 

