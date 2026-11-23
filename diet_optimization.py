
import csv
import numpy as np
import cvxpy as cp


with open("diet_dataset.csv", "r", newline="", encoding="utf-8-sig") as file:
    foods = list(csv.DictReader(file))

names = [food["food_name"] for food in foods]
meal_types = [food["meal_type"].strip().lower() for food in foods]
regions = [food["region"].strip().lower() for food in foods]
categories = [food["category"].strip().lower() for food in foods]
food_groups = [food["food_group"].strip().lower() for food in foods]

servings = np.array([int(food["serving_grams"]) for food in foods])
calories = np.array([float(food["calories"]) for food in foods])
carbs = np.array([float(food["carbs"]) for food in foods])
protein = np.array([float(food["protein"]) for food in foods])
fat = np.array([float(food["fat"]) for food in foods])
fibre = np.array([float(food["fibre"]) for food in foods])
sugar = np.array([float(food["sugar"]) for food in foods])
cost = np.array([float(food["cost"]) for food in foods])
limits = np.array([int(food["max_servings"]) for food in foods])

n = len(foods)
meal_names = ["Breakfast", "Lunch", "Dinner"]
meal_shares = [0.25, 0.40, 0.35]

nutrients = {
    1: ("Protein", protein),
    2: ("Carbohydrates", carbs),
    3: ("Fat", fat),
    4: ("Fibre", fibre),
    5: ("Sugar", sugar)
}


def get_int(prompt, minimum, maximum):
    while True:
        try:
            value = int(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Enter a value between {minimum} and {maximum}.")
        except ValueError:
            print("Enter a valid number.")


def get_float(prompt, minimum, maximum):
    while True:
        try:
            value = float(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Enter a value between {minimum} and {maximum}.")
        except ValueError:
            print("Enter a valid number.")


def get_choice(prompt, choices):
    while True:
        value = input(prompt).strip().lower()
        if value in choices:
            return value
        print("Invalid choice. Try again.")


def get_nutrient_selection(prompt):
    while True:
        value = input(prompt).strip()

        if not value:
            return []

        try:
            selected = [int(item) for item in value.replace(",", " ").split()]

            if len(selected) != len(set(selected)):
                print("Do not enter the same number more than once.")
                continue

            if all(item in nutrients for item in selected):
                return selected

            print("Choose only numbers from 1 to 5.")

        except ValueError:
            print("Enter numbers separated by spaces or commas.")


def calculate_calories(age, sex, height, weight, activity):
    if sex == "m":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    return bmr * activity


def normalize(values):
    maximum = np.max(values)

    if maximum <= 0:
        return np.zeros(len(values))

    return values / maximum


def create_preference_score(high_nutrients, low_nutrients):
    score = np.zeros(n)

    for number in high_nutrients:
        name, values = nutrients[number]
        score += normalize(values)

    for number in low_nutrients:
        name, values = nutrients[number]
        score -= normalize(values)

    return score


def optimize_diet(target, weight, high_nutrients, low_nutrients):
    preference_score = create_preference_score(
        high_nutrients,
        low_nutrients
    )

    x = cp.Variable((n, 3), integer=True)
    y = cp.Variable((n, 3), boolean=True)

    daily_x = cp.sum(x, axis=1)

    constraints = [
        x >= y,
        x <= cp.multiply(limits.reshape(-1, 1), y),
        x >= 0,
        daily_x <= limits
    ]

    for i in range(n):
        for j in range(3):
            if meal_types[i] == "breakfast" and j != 0:
                constraints.append(y[i, j] == 0)
            elif meal_types[i] == "main" and j == 0:
                constraints.append(y[i, j] == 0)

    for j in range(3):
        groups = sorted(set(food_groups))

        for group in groups:
            indices = [
                i for i in range(n)
                if food_groups[i] == group
            ]

            if len(indices) > 1:
                constraints.append(cp.sum(y[indices, j]) <= 1)

    total_calories = cp.sum(cp.multiply(calories.reshape(-1, 1), x))
    total_carbs = cp.sum(cp.multiply(carbs.reshape(-1, 1), x))
    total_protein = cp.sum(cp.multiply(protein.reshape(-1, 1), x))
    total_fat = cp.sum(cp.multiply(fat.reshape(-1, 1), x))
    total_fibre = cp.sum(cp.multiply(fibre.reshape(-1, 1), x))
    total_sugar = cp.sum(cp.multiply(sugar.reshape(-1, 1), x))
    total_cost = cp.sum(cp.multiply(cost.reshape(-1, 1), x))

    constraints += [
        total_calories >= target * 0.95,
        total_calories <= target * 1.05,
        total_carbs * 4 >= total_calories * 0.35,
        total_carbs * 4 <= total_calories * 0.65,
        total_fat * 9 >= total_calories * 0.20,
        total_fibre >= 25,
        total_sugar * 4 <= total_calories * 0.10,
        total_protein >= 0.8 * weight
    ]

    for number in high_nutrients:
        if number == 4:
            constraints.append(total_fibre >= 25)

    for number in low_nutrients:
        if number == 5:
            constraints.append(total_sugar * 4 <= total_calories * 0.10)

    for j in range(3):
        meal_calories = cp.sum(cp.multiply(calories, x[:, j]))
        meal_foods = cp.sum(y[:, j])
        meal_target = target * meal_shares[j]

        constraints += [
            meal_calories >= meal_target * 0.65,
            meal_calories <= meal_target * 1.35
        ]

        if j == 0:
            constraints += [
                meal_foods >= 2,
                meal_foods <= 4
            ]
        else:
            constraints += [
                meal_foods >= 3,
                meal_foods <= 5
            ]

            protein_indices = [
                i for i in range(n)
                if categories[i] == "protein"
            ]

            vegetable_indices = [
                i for i in range(n)
                if categories[i] == "vegetable"
            ]

            if protein_indices:
                constraints.append(cp.sum(y[protein_indices, j]) >= 1)

            if vegetable_indices:
                constraints.append(cp.sum(y[vegetable_indices, j]) >= 1)

    regional_options = ["north", "south"]
    regional_choice = cp.Variable((2, 3), boolean=True)
    regional_mismatch = cp.Variable((n, 3), boolean=True)

    for j in range(3):
        constraints.append(cp.sum(regional_choice[:, j]) == 1)

        for i in range(n):
            if regions[i] in regional_options:
                region_index = regional_options.index(regions[i])

                constraints.append(
                    y[i, j] <= regional_choice[region_index, j] + regional_mismatch[i, j]
                )

        constraints.append(cp.sum(regional_mismatch[:, j]) <= 1)

    first_problem = cp.Problem(
        cp.Minimize(total_cost),
        constraints
    )

    first_problem.solve(solver=cp.SCIPY)

    if first_problem.status not in ["optimal", "optimal_inaccurate"]:
        print("\nA suitable diet plan could not be generated.")
        print("Try changing the personal details or nutrient preferences.")
        return

    minimum_cost = total_cost.value

    second_constraints = constraints + [
        total_cost <= minimum_cost * 1.25
    ]

    selection_score = cp.sum(
        cp.multiply(preference_score.reshape(-1, 1), x)
    ) - 2 * cp.sum(regional_mismatch)

    second_problem = cp.Problem(
        cp.Maximize(selection_score),
        second_constraints
    )

    second_problem.solve(solver=cp.SCIPY)

    if second_problem.status not in ["optimal", "optimal_inaccurate"]:
        print("\nCould not generate the improved meal plan.")
        return

    print("\n========== DIET PLAN ==========")
    print(f"Daily calorie requirement: {target:.0f} kcal")

    print("\nNutrients to increase:")
    if high_nutrients:
        print(", ".join(nutrients[i][0] for i in high_nutrients))
    else:
        print("None")

    print("\nNutrients to decrease:")
    if low_nutrients:
        print(", ".join(nutrients[i][0] for i in low_nutrients))
    else:
        print("None")

    print(f"\nEstimated daily cost: Rs. {total_cost.value:.2f}")

    for j in range(3):
        print(f"\n========== {meal_names[j].upper()} ==========")

        meal_total = 0
        meal_cost = 0

        for i in range(n):
            quantity = round(x.value[i, j])

            if quantity > 0:
                food_calories = calories[i] * quantity
                food_cost = cost[i] * quantity
                food_grams = servings[i] * quantity

                meal_total += food_calories
                meal_cost += food_cost

                print(
                    f"{names[i]}: {quantity} serving(s), "
                    f"{food_grams} g, {food_calories:.0f} kcal, "
                    f"Rs. {food_cost:.2f}"
                )

        print(f"Meal calories: {meal_total:.0f} kcal")
        print(f"Meal cost: Rs. {meal_cost:.2f}")

    print("\n========== DAILY NUTRITION ==========")
    print(f"Calories: {total_calories.value:.1f} kcal")
    print(f"Carbohydrates: {total_carbs.value:.1f} g")
    print(f"Protein: {total_protein.value:.1f} g")
    print(f"Fat: {total_fat.value:.1f} g")
    print(f"Fibre: {total_fibre.value:.1f} g")
    print(f"Sugar: {total_sugar.value:.1f} g")
    print(f"Total cost: Rs. {total_cost.value:.2f}")


while True:
    print("\n========== DIET PLANNER ==========")

    age = get_int("Enter age: ", 18, 100)
    sex = get_choice("Enter sex (M/F): ", ["m", "f"])
    height = get_float("Enter height in cm: ", 120, 220)
    weight = get_float("Enter weight in kg: ", 30, 200)

    print("\nActivity Level")
    print("1. Sedentary")
    print("2. Lightly Active")
    print("3. Moderately Active")
    print("4. Very Active")

    activity_choice = get_int("Choose activity level: ", 1, 4)
    activity_factors = [1.2, 1.375, 1.55, 1.725]
    activity = activity_factors[activity_choice - 1]

    print("\n========== NUTRIENT PREFERENCES ==========")
    print("1. Protein")
    print("2. Carbohydrates")
    print("3. Fat")
    print("4. Fibre")
    print("5. Sugar")

    print("\nEnter the numbers of nutrients you want HIGH.")
    print("Example: 1 4")

    high_nutrients = get_nutrient_selection("High nutrients: ")

    while True:
        print("\nEnter the numbers of nutrients you want LOW.")
        print("Example: 3 5")

        low_nutrients = get_nutrient_selection("Low nutrients: ")

        if not set(high_nutrients).intersection(low_nutrients):
            break

        print("The same nutrient cannot be selected as both high and low.")

    target = calculate_calories(
        age,
        sex,
        height,
        weight,
        activity
    )

    print(f"\nEstimated daily calorie requirement: {target:.0f} kcal")

    optimize_diet(
        target,
        weight,
        high_nutrients,
        low_nutrients
    )

    again = get_choice(
        "\nGenerate another diet plan? (Y/N): ",
        ["y", "n"]
    )

    if again == "n":
        print("Thank you for using the Diet Planner!")
        break
