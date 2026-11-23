from diet_optimization import calculate_calories, optimize_diet, nutrients


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

    print("\nSelect the nutrients you would like to INCREASE in your diet.")
    print("Example: Enter 1 3 to select Protein and Fat.")

    high_nutrients = get_nutrient_selection("High nutrients: ")

    while True:
        print("\nSelect the nutrients you would like to DECREASE in your diet.")
        print("Example: Enter 1 3 to select Protein and Fat.")

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