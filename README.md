# Optimal Diet Planning Using Linear Programming

A Python application that uses Linear Programming to generate an affordable daily vegetarian meal plan from an Indian food dataset. It estimates the user's daily calorie requirement and selects foods and serving quantities while satisfying calorie, nutrient and meal-related constraints.

---

## Team Details

**Team Name:** OptimalPoint

### Team Members

**1. Soumya Gupta**
- Member ID: BA2025049

**2. Jyotiraditya Parida**
- Member ID: BA2025017

---

## Project Description

The project aims to find a low-cost daily diet plan that meets the user's estimated calorie requirement and selected nutritional preferences.
The application uses a dataset of common Indian vegetarian food items. Each item includes its meal type, serving size, calories, carbohydrates, protein, fat, fibre, sugar and cost.
The user provides personal details, including age, height, weight, sex and activity level, and specifies which nutrients they would like to increase or limit in their daily diet. The optimization model determines which foods to include in breakfast, lunch and dinner, along with the number of servings of each food.
The main objective is to **minimize the total daily food cost** while satisfying the model's constraints.

## How the Project Works

1. **Load the dataset:** Reads food information from `diet_dataset.csv`.
2. **Collect user details:** Asks for age, sex, height, weight and activity level.
3. **Calculate calorie requirement:** Estimates daily calories using the Mifflin--St Jeor equation and an activity multiplier.
4. **Collect nutrient preferences:** Lets the user select nutrients to increase and nutrients to decrease.
5. **Build the optimization model:** Creates decision variables for food servings and food selection across three meals.
6. **Apply constraints:** Enforces daily calorie, nutrient, serving, food-group and meal-wise restrictions.
7. **Optimize the cost:** Finds a feasible meal plan with the minimum estimated cost.
8. **Display the result:** Shows selected foods, serving quantities, calories, meal costs, daily nutrition totals and total estimated cost.

## User Inputs and Menu

At startup, the program asks for:

- Age
- Sex (M/F)
- Height in centimetres
- Weight in kilograms
- Activity level:
  - Sedentary
  - Lightly Active
  - Moderately Active
  - Very Active

The user then selects nutrients to increase and nutrients to decrease:

```text
1. Protein
2. Carbohydrates
3. Fat
4. Fibre
5. Sugar
```

Multiple nutrient numbers can be entered, separated by spaces or commas. A nutrient cannot be selected as both high and low. After the meal plan is displayed, the program asks whether another plan should be generated.

## Optimization Model

### Decision Variables

- `x[i,j]`: Integer number of servings of food item `i` assigned to meal `j`.
- `y[i,j]`: Binary variable indicating whether food item `i` is selected for meal `j` (1 = selected, 0 = not selected).

The three meals are breakfast, lunch and dinner.

### Objective Function

Minimize the total cost of all selected food servings:

**Minimize:** sum of `cost[i] * x[i,j]` over all foods and meals.

Here, `cost[i]` is the cost per serving of food item `i`.

### Main Constraints

**Daily calories**

Total daily calories must be between 95% and 105% of the estimated calorie requirement.

**Meal-wise calories**

The daily calorie target is distributed as follows:

### Meal Calorie Share

| Meal | Calorie Share |
|---|---:|
| Breakfast | 25% |
| Lunch | 40% |
| Dinner | 35% |

Each meal must contain between **80% and 120%** of its allocated calorie target.

### Nutritional Limits

| Nutrient | Minimum | Maximum |
|---|---|---|
| Protein | 0.8 × Body Weight (g) | 2 × Body Weight (g) |
| Carbohydrates | (35% × Calories) ÷ 4 | (65% × Calories) ÷ 4 |
| Fat | (20% × Calories) ÷ 9 | (30% × Calories) ÷ 9 |
| Fibre | 25 g | 100 g |
| Sugar | 0 g | (10% × Calories) ÷ 4 |

If the constraints cannot all be satisfied, the solver reports that a suitable plan could not be generated.

## Technologies and Libraries Used

| Technology / Library | Purpose |
|---|---|
| **Python** | Main programming language |
| **CVXPY** | Defines optimization variables, objective function and constraints |
| **NumPy** | Handles numerical arrays and food nutrient data |
| **SciPy** | Provides the optimization solver used through CVXPY |
| **CSV** | Reads the dataset and is included in Python's standard library |

## Project Structure

```text
OptimalPoint/
│
├── main.py
├── diet_optimization.py
├── diet_dataset.csv
└── README.md
```

- **main.py:** Handles user input, input validation, activity-level selection, nutrient preferences and the main program loop.
- **diet_optimization.py:** Handles dataset loading, calorie calculation, nutrient constraints, the optimization model and diet-plan output.
- **diet_dataset.csv:** Contains the Indian vegetarian food dataset.
- **README.md:** Contains project information and setup instructions.

## Installation and Setup

### 1. Install Python

Install Python and make sure Python and `pip` are available from the terminal.

### 2. Download or Clone the Project

Download the project files or clone the repository:

```bash
git clone https://github.com/JyotiradityaParida/Diet_Planner.git
cd Diet_Planner/code
```

### 3. Keep the Required Files Together

Make sure `main.py`, `diet_optimization.py` and `diet_dataset.csv` are in the same project folder. The program reads the CSV file from its current working directory.

### 4. Install Dependencies

Run:

```bash
pip install numpy cvxpy scipy
```

The `csv` module does not need to be installed separately because it is included with Python.

### 5. Run the Program

Run the main file:

```bash
python main.py
```
