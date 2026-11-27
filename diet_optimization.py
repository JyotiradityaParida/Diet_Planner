import csv
import numpy as np
import cvxpy as cp


with open("diet_dataset.csv", "r", newline="", encoding="utf-8-sig") as file:
    foods = list(csv.DictReader(file))

names = [food["food_name"] for food in foods]
meal_types = [food["meal_type"].strip().lower() for food in foods]
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

group_limits = {
    "breakfast": 4, "rice": 3, "roti": 5, "dal": 1, "beans": 2,"soya": 1, "paneer": 1, "vegetable": 3, "dairy": 2, "fruit": 2
}

nutrients = {
    1: "Protein",
    2: "Carbohydrates",
    3: "Fat",
    4: "Fibre",
    5: "Sugar"
}


def calculate_calories(age, sex, height, weight, activity):
    if sex == "m":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    return bmr * activity


def optimize_diet(target, weight, high_nutrients, low_nutrients):
    x = cp.Variable((n, 3), integer=True)

    daily_x = cp.sum(x, axis=1)

    constraints = [
        x >= 0,
        daily_x <= limits
    ]

    for i in range(n):
        for j in range(3):
            if meal_types[i] == "breakfast" and j != 0:
                constraints.append(x[i, j] == 0)
            elif meal_types[i] == "main" and j == 0:
                constraints.append(x[i, j] == 0)

    for group, group_limit in group_limits.items():
        indices = [i for i in range(n) if food_groups[i] == group]

        if indices:
            for j in range(3):
                constraints.append(cp.sum(x[indices, j]) <= group_limit)

    total_calories = cp.sum(cp.multiply(calories.reshape(-1, 1), x))
    total_carbs = cp.sum(cp.multiply(carbs.reshape(-1, 1), x))
    total_protein = cp.sum(cp.multiply(protein.reshape(-1, 1), x))
    total_fat = cp.sum(cp.multiply(fat.reshape(-1, 1), x))
    total_fibre = cp.sum(cp.multiply(fibre.reshape(-1, 1), x))
    total_sugar = cp.sum(cp.multiply(sugar.reshape(-1, 1), x))
    total_cost = cp.sum(cp.multiply(cost.reshape(-1, 1), x))

    constraints += [
        total_calories >= target * 0.95,
        total_calories <= target * 1.05
    ]

    nutrient_limits = {
        1: (0.8 * weight, 2 * weight, total_protein),
        2: (total_calories * 0.35 / 4, total_calories * 0.65 / 4, total_carbs),
        3: (total_calories * 0.20 / 9, total_calories * 0.30 / 9, total_fat),
        4: (25, 100, total_fibre),
        5: (0, total_calories * 0.10 / 4, total_sugar)
    }

    for number, (minimum, maximum, total) in nutrient_limits.items():
        midpoint = (minimum + maximum) / 2

        if number in high_nutrients:
            constraints.append(total >= midpoint)
        else:
            constraints.append(total >= minimum)

        if number in low_nutrients:
            constraints.append(total <= midpoint)
        else:
            constraints.append(total <= maximum)

    for j in range(3):
        meal_calories = cp.sum(cp.multiply(calories, x[:, j]))
        meal_target = target * meal_shares[j]

        constraints += [
            meal_calories >= meal_target * 0.80,
            meal_calories <= meal_target * 1.20
        ]

        if j != 0:
            protein_indices = [
                i for i in range(n)
                if categories[i] == "protein"
            ]

            vegetable_indices = [
                i for i in range(n)
                if categories[i] == "vegetable"
            ]

            if protein_indices:
                constraints.append(cp.sum(x[protein_indices, j]) >= 1)

            if vegetable_indices:
                constraints.append(cp.sum(x[vegetable_indices, j]) >= 1)

    problem = cp.Problem(
        cp.Minimize(total_cost),
        constraints
    )

    problem.solve(solver=cp.SCIPY)

    if problem.status not in ["optimal", "optimal_inaccurate"]:
        print("\nA suitable diet plan could not be generated.")
        print("Try changing the personal details or nutrient selections.")
        return

    print("\n========== DIET PLAN ==========")
    print(f"Daily calorie requirement: {target:.0f} kcal")

    print("\nNutrients to increase:")
    if high_nutrients:
        print(", ".join(nutrients[i] for i in high_nutrients))
    else:
        print("None")

    print("\nNutrients to decrease:")
    if low_nutrients:
        print(", ".join(nutrients[i] for i in low_nutrients))
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
    print(f"Protein: {total_protein.value:.1f} g")
    print(f"Carbohydrates: {total_carbs.value:.1f} g")
    print(f"Fat: {total_fat.value:.1f} g")
    print(f"Fibre: {total_fibre.value:.1f} g")
    print(f"Sugar: {total_sugar.value:.1f} g")
    print(f"Total cost: Rs. {total_cost.value:.2f}")
