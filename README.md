# Optimal Diet Planning Using Linear Programming

A Python application that uses Linear Programming to generate an
affordable daily vegetarian meal plan using a dataset of Indian food
items. It estimates the user's daily calorie requirement and determines
food combinations and serving quantities while satisfying calorie,
nutritional and meal-related constraints.

------------------------------------------------------------------------

## Team Details

**Team Name:** OptimalPoint

### Team Members

**1. Soumya Gupta** - Roll number: BA2025049

**2. Jyotiraditya Parida** - Roll number: BA2025017

------------------------------------------------------------------------

## Project Description

The project aims to generate a low-cost daily vegetarian diet plan that
meets the user's estimated calorie requirement and selected nutritional
preferences.

The application uses a synthetic dataset containing 100 common Indian
vegetarian food items. Each item includes its meal type, serving size,
calories, carbohydrates, protein, fat, fibre, sugar, cost, category,
maximum daily servings and food group.

The user provides personal details, including age, sex, height, weight
and activity level, and specifies which nutrients they would like to
increase or decrease in their daily diet.

The optimization model determines the number of servings of each food
item to include in breakfast, lunch and dinner.

The main objective is to **minimize the total daily food cost** while
satisfying the implemented constraints.

## How the Project Works

1.  **Load the dataset:** Reads food information from `diet_dataset.csv`
    using Python's CSV reader.
2.  **Collect user details:** Asks for age, sex, height, weight and
    activity level.
3.  **Calculate calorie requirement:** Estimates daily calories using
    the Mifflin-St Jeor equation and an activity multiplier.
4.  **Collect nutrient preferences:** Allows users to select nutrients
    to increase and nutrients to decrease.
5.  **Build the optimization model:** Creates integer decision variables
    representing the number of servings of each food item assigned to
    each meal.
6.  **Apply constraints:** Enforces daily calorie, nutritional,
    individual serving, food-group and meal-wise restrictions.
7.  **Optimize the cost:** Finds a feasible meal plan with the minimum
    estimated daily cost.
8.  **Display the result:** Shows selected foods, serving quantities,
    gram amounts, calories, meal costs, daily nutrition totals and total
    estimated cost.
9.  **Repeat if requested:** Allows users to enter another profile and
    generate another diet plan without restarting the application.

## User Inputs and Menu

At startup, the program asks for:

-   Age (18--100 years)
-   Sex (M/F)
-   Height (120--220 cm)
-   Weight (30--200 kg)
-   Activity level:
    -   Sedentary
    -   Lightly Active
    -   Moderately Active
    -   Very Active

The user then selects nutrients to increase and nutrients to decrease:

``` text
1. Protein
2. Carbohydrates
3. Fat
4. Fibre
5. Sugar
```

Multiple nutrient numbers can be entered, separated by spaces or commas.
Duplicate selections are rejected and a nutrient cannot be selected as
both high and low. Empty selections are also allowed.

## Optimization Model

### Decision Variables

The model uses one integer decision variable for every food--meal
combination:

-   `x[i,j]`: Integer number of servings of food item `i` assigned to
    meal `j`.

The three meals are breakfast, lunch and dinner.

With 100 food items and 3 meals, the model contains **300 integer
decision variables**.

The model is formulated as an Integer Linear Programming (ILP) problem
because all decision variables are integer-valued and the objective
function and constraints are linear.

### Objective Function

Minimize the total cost of all selected food servings:

**Minimize:** Sum of `cost[i] * x[i,j]` over all food items and meals.

Here, `cost[i]` represents the cost per serving of food item `i`.

### Main Constraints

**Daily Calories**

Total daily calories must remain between 95% and 105% of the estimated
calorie requirement.

**Meal-wise Calories**

The daily calorie target is distributed as follows:

| Meal      | Calorie Share |
|-----------|--------------:|
| Breakfast | 25%           |
| Lunch     | 40%           |
| Dinner    | 35%           |

Each meal must contain between 80% and 120% of its allocated calorie
target.

**Nutritional Limits**

| Nutrient      | Minimum                  | Maximum                  |
|---------------|--------------------------|--------------------------|
| Protein       | 0.8 × Body Weight (g)    | 2 × Body Weight (g)      |
| Carbohydrates | (35% × Calories) ÷ 4     | (65% × Calories) ÷ 4     |
| Fat           | (20% × Calories) ÷ 9     | (30% × Calories) ÷ 9     |
| Fibre         | 25 g                     | 100 g                     |
| Sugar         | 0 g                      | (10% × Calories) ÷ 4     |

**Nutrient Preferences**

For each nutrient, the model calculates the midpoint between its minimum
and maximum limits.

-   Selecting a nutrient to increase raises its minimum limit to the
    midpoint.
-   Selecting a nutrient to decrease lowers its maximum limit to the
    midpoint.
-   Nutrients without selected preferences retain their original limits.

**Serving and Food-Group Restrictions**

-   The total daily servings of each individual food item cannot exceed
    its maximum daily serving limit specified in the dataset.
-   Combined servings belonging to the same food group are restricted
    separately for each meal using predefined limits in the Python code.
-   Each food item is restricted to its permitted meal.
-   Lunch and dinner must each contain at least one serving from the
    Protein category and at least one serving from the Vegetable
    category.

If the constraints cannot all be satisfied, the solver reports that a
suitable diet plan could not be generated.

## Technologies and Libraries Used

| Technology / Library | Purpose |
|---|---|
| **Python** | Main programming language |
| **CVXPY** | Defines optimization variables, objective function and constraints |
| **NumPy** | Handles numerical arrays and food nutrient data |
| **SciPy** | Provides the optimization solver interface used through CVXPY |
| **CSV** | Reads the food dataset using Python's standard library |

## Project Structure

``` text
Diet_Planner/
│
├── code/
│   ├── main.py
│   ├── diet_optimization.py
│   ├── diet_dataset.csv
│   └── README.md
│
└── report.pdf
```

-   **main.py:** Handles user input, input validation, activity-level
    selection, nutrient preferences and the main program loop.
-   **diet_optimization.py:** Handles dataset loading, calorie
    calculation, optimization constraints, cost minimization and
    diet-plan output.
-   **diet_dataset.csv:** Contains the synthetic dataset of 100 Indian
    vegetarian food items.
-   **README.md:** Contains project information and setup instructions.
-   **report.pdf:** Contains the mathematical formulation, methodology,
    solver details and experimental results.

## Installation and Setup

### 1. Install Python

Install Python and make sure Python and `pip` are available from the terminal.

### 2. Download the Project

Download the project folder and extract it to your preferred location.

### 3. Navigate to the Code Directory

Open a terminal in the project folder and navigate to the `code` directory:

```bash
cd code
```

Make sure `main.py`, `diet_optimization.py` and `diet_dataset.csv` are present in this directory.

### 4. Install Dependencies

Run the following command to install the required libraries:

```bash
pip install numpy cvxpy scipy
```

The `csv` module does not need to be installed separately because it is included in Python's standard library.

### 5. Run the Program

From the same `code` directory, run:

```bash
python main.py
```
