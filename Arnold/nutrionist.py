import openai
import requests


#edamam keys
APP_KEY = "ee44e667d2bd6504b36f6abddcdccea6"
APP_ID = "217598f8"
#open ai key
openai.api_key = "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"

history = []

def nutritionist(message, section, user_onboard_data, conversation_history=None):
    sex = user_onboard_data.get("Sex", "Male")
    weight = user_onboard_data.get("Weight", 0)
    daily_act_level = user_onboard_data.get("Daily Activity Level", 1.6)
    veg_nonveg = user_onboard_data.get("Vegeterian/NonVegeterian", "Both")
    no_of_meals = user_onboard_data.get("No of meals", 3)
    meals = user_onboard_data.get("Current Meals", "Brown Breads, Rice, Oats, Chicken, Eggs, Paneer, Milk, Curd etc")
    cheat_meal = user_onboard_data.get("Cheat Meals", "Pizza, Burger, Chinese, Italian")
    food_reach = user_onboard_data.get("Reachable food", "Everything")
    food_name = user_onboard_data.get("Food Name", "Everything")
    query = user_onboard_data.get("Query", "")
    goal = user_onboard_data.get("Goal", "Unknown")
    
    def macro_distribution(weight, sex, daily_act_level):
        if sex in ("Male", "male", "M"):
            bmr = weight * 24
            tdee = bmr * daily_act_level
            protein = weight * 2
            fat = weight * 0.5
            protein_calories = protein * 4
            fat_calories = fat * 9
            carbs_calories = tdee - (protein_calories + fat_calories)
            carbs = (carbs_calories / 4)
            return carbs, protein, fat
        elif sex in ("Female", "female", "F"):
            bmr = weight * 24
            tdee = bmr * daily_act_level
            protein = weight * 1.7
            fat = weight * 0.5
            protein_calories = protein * 4
            fat_calories = fat * 9
            carbs_calories = tdee - (protein_calories + fat_calories)
            carbs = (carbs_calories / 4)
            return carbs, protein, fat
        else:
            bmr = weight * 24
            tdee = bmr * daily_act_level
            protein = weight * 2
            fat = weight * 0.5
            protein_calories = protein * 4
            fat_calories = fat * 9
            carbs_calories = tdee - (protein_calories + fat_calories)
            carbs = (carbs_calories / 4)
            return carbs, protein, fat

    def meal_distribution(carbs, protein, fat, no_of_meals):
        divided_carbs = carbs/no_of_meals
        divided_protein = protein/no_of_meals
        divided_fat = fat/no_of_meals
        return divided_carbs, divided_protein, divided_fat
    
    def grocery_list(carbs, protein, fat):
        week_carbs = carbs*7
        week_protein = protein*7
        week_fat = fat*7
        return week_carbs, week_protein, week_fat

    carbs, protein, fat = macro_distribution(weight, sex, daily_act_level)
    divided_carbs, divided_protein, divided_fat = meal_distribution(carbs, protein, fat, no_of_meals)
    week_carbs, week_protein, week_fat = grocery_list(carbs, protein, fat)


    prompt = ""

    if section == "intro":
        prompt = f"""Your name is Arnold AI. You are an experienced, clever and helpful fitness coach specializing in muscle build, fat loss, and recomposition and have transformed over 100000+ people lives all over the world.
                """
    elif section == "gather_requirements":
        prompt =f"""1. User Goal : {goal}
                    2. Macronutrients breakdown for user's nutrition plan : 
                    Carbohydrates : {carbs}gm, Protein : {protein}gm, Fat : {fat}gm
                3. Sources of food should be : {veg_nonveg}
                4. Current Meals sources user is having are : {meals}
                5. Food that are in user's reach are: {food_reach}
               Arnold, please go through all the requirements. Do you understand the goal and lifestyle of the user?"""
    elif section == "meal_one":
        prompt = f"""Create a nutrition plan of 3 meals by including food accesible to user {meals} which will fit the user's macronutrients that we just calulated
                    Example for meal 1 : 
                    Total window or macronutrients we have -  carbohydrates: 300gm, Protein: 300gm, Fats : 67gm 
                    Meal 1: Oatmeal: 100g Saffola Oats (60g carbohydrates, 10g protein, 7g fat) + 300ml Amul Milk (15g carbohydrates, 9g protein, 8g fat) + 60g Myprotein Whey Protein (2g carbohydrates, 50g protein, 2g fat) + 2 Bananas (54g carbohydrates, 2g protein, 0.6g fat) + 20g Almonds (4g carbohydrates, 4g protein, 11g fat) 
                    Decide the quantity of above meal according to the user's macronutrients i.e. {divided_carbs}gm, {divided_protein}gm, {divided_fat}gm. 
                    Provide the meal 1 for user in the same format of above Meal 1: """
    elif section == "meal_two":
        prompt = f"""Create a nutrition plan of 3 meals by including food accesible to user {meals} which will fit the user's macronutrients that we just calulated
                    Example for meal 2 : 
                    We will subtract the Meal 1 Macronutrients from the total window of macronutrients - carbohydrates: 300gm, Protein: 300gm, Fats : 67gm
                    Remaining window of macronutrients we have -  carbohydrates: 165gm, Protein: 225gm, Fats :38.4gm
                    Meal 2: Sandwich : 8 Britannia Brown Breads (120g carbohydrates, 24g protein, 8g fat) + 12 Egg Omelette (2g carbohydrates, 36g protein) + 2 Amul Cheese Slices (2g carbohydrates, 10g protein, 10g fat)
                    Approximate total macronutrients for the entire meal plan: carbohydrates: 301g, Protein: 302g, Fats: 67.6g
                    Decide the quantity of above meal 2 = total macronutrients i.e. {divided_carbs}gm, {divided_protein}gm, {divided_fat}gm  
                    Provide the meal 2 for user in the same format of above Meal 2: """
    elif section == "meal_three":
        prompt = f"""Create a nutrition plan of 3 meals by including food accesible to user {meals} which will fit the user's macronutrients that we just calulated
                    Example for meal 3 : 
                    We will subtract the Meal 1 Macronutrients and Meal 2 Macronutrients from Total window of macronutrients we have - carbohydrates: 300gm, Protein: 300gm, Fats : 67gm 
                    Remaining window of macronutrient we have - carbohydrates: 41gm, Protein: 155gm, Fats: 20.4gm
                    Meal 3: Dinner :  420g Chicken Breast (0g carbohydrates, 130g protein, 15g fat) + 200 Cooked Basmati Rice (40g carbohydrates, 6g protein, 0g fat) + 200g Spinach (4g carbohydrates, 5g protein, 1g fat) + 200g Broccoli (14g carbohydrates, 6g protein, 1g fat)
                    Approximate total macronutrients for the entire meal plan: carbohydrates: 301g, Protein: 302g, Fats: 67.6g
                    Decide the quantity of above meal 3 = total macronutrients i.e. {divided_carbs}gm, {divided_protein}gm, {divided_fat}gm                    
                    Provide the meal 3 for user in the same format of above Meal 3: """
    elif section == "final_macros":
        prompt = f"""Final Macronutrients for sample meal are - carbohydrates: 315gm, proteins: 292gm, fats: 63.6gm 
                    Example : Meal 1 carbohydrates + Meal 2 carbohydrates + Meal 3 carbohydrates = Total carbohydrates
                              Meal 1 proteins + Meal 2 proteins + Meal 3 proteins = Total proteins
                              Meal 1 fats + Meal 2 fats + Meal 3 fats = Total fats
                     By adding all three meals macronutrients give the final macronutrients of the user's meal plan:"""
    elif section == "replace_meal":
        prompt = f"""Create a meal of macronutrients i.e. {divided_carbs}gm, {divided_protein}gm, {divided_fat}gm using any 4 or 5 options from {meals}"""
    elif section == "cheat_meal":
        prompt = f"""Create a cheat meal of macronutrients i.e. {divided_carbs}gm, {divided_protein}gm, {divided_fat}gm using any 1 option from {cheat_meal}. So that user can enjoy this meal."""
    elif section == "food_info":
        data = fetch_food_info({food_name})
        text = data["text"]
        label = data["parsed"][0]["food"]["label"]
        nutrients = data["parsed"][0]["food"]["nutrients"]
        prompt = f"""Food Name:{text}/{label}. It contains {nutrients}. Give two lines of breif about mentioned food to the user: 
                    And give instruction to prepare a small meal with it."""
    elif section == "grocery_list":
        prompt = f"""Prepare a grocery list for the user for 7 days. Quantity for user three meals for a week are {week_carbs}gm, {week_protein}gm, {week_fat}gm. List of items are {meals}. Provide the quantity to the user for buying the items from the list. """
    elif section == "fitness_related_questions":
        prompt = f"""Fitness Question:{query}
                     Answer as concisely as possible."""

    # Ensure the message and prompt don't exceed the token limit
    def count_tokens(text):
        return len(text.split())

    max_tokens = 4096 - count_tokens(prompt)

    if max_tokens < 10:  # Leave some room for AI's response
        return "Message is too long, please shorten it."

    prompt = message + " "+ prompt
    conversation_history.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= conversation_history + [{"role": "user", "content": message}, {"role": "assistant", "content": ""}],
        max_tokens=min(max_tokens, 150),
        n=1,
        stop=None,
        temperature=0.2,
    )

    print(f"User: {prompt}")
    print(f"Arnold: {response.choices[0].message['content'].strip()}")
    print("\n") 

    result = response.choices[0].message['content'].strip()
    conversation_history.append({"role": "assistant", "content": result})
    return result, conversation_history


def complete_the_remaining_response(message):
    prompt = message
    # Ensure the message and prompt don't exceed the token limit
    def count_tokens(text):
        return len(text.split())

    max_tokens = 4096 - count_tokens(prompt)
    if max_tokens < 10:  # Leave some room for AI's response
        return "Message is too long, please shorten it."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt},
                  {"role": "assistant", "content": ""}],
        max_tokens=min(max_tokens, 150),
        n=1,
        stop=None,
        temperature=0.8,
    )

    print(f"User: {prompt}")
    print(f"Arnold: {response.choices[0].message['content'].strip()}")

    result = response.choices[0].message['content'].strip()

    return result

def is_response_incomplete(response):
    if response is None:
        return False
    return response.strip()[-1] not in (".", "!", "?")

    
def get_last_n_words(text, n=100):
    words = text.split()
    return " ".join(words[-n:])

def complete_response_one(response_tuple):
    response = response_tuple[0]
    incomplete_response = True
    while incomplete_response:
        incomplete_response = is_response_incomplete(response)
        if incomplete_response:
            last_words = get_last_n_words(response)
            prompt = f"Please complete the following response without changing the context or altering the content: '{last_words}'"
            response = complete_the_remaining_response(prompt)
    return response

def complete_meal_one(response_tuple):
    response = response_tuple[0]
    incomplete_response = True
    while incomplete_response:
        incomplete_response = is_response_incomplete(response)
        if incomplete_response:
            last_words = get_last_n_words(response)
            prompt = f"Complete the Meal 1: Oatmeal.The initial response is as follows: '{last_words}'"
            response = complete_the_remaining_response(prompt)
    return response

def complete_meal_two(response_tuple):
    response = response_tuple[0]
    incomplete_response = True
    while incomplete_response:
        incomplete_response = is_response_incomplete(response)
        if incomplete_response:
            last_words = get_last_n_words(response)
            prompt = f"Complete the Meal 2: Sandwich. The initial response is as follows: '{last_words}'"
            response = complete_the_remaining_response(prompt)
    return response

def complete_meal_three(response_tuple):
    response = response_tuple[0]
    incomplete_response = True
    while incomplete_response:
        incomplete_response = is_response_incomplete(response)
        if incomplete_response:
            last_words = get_last_n_words(response)
            prompt = f"Complete the Meal 3: Dinner. The initial response is as follows: '{last_words}'"
            response = complete_the_remaining_response(prompt)
    return response

def fetch_food_info(food_name):
    API_URL = f"https://api.edamam.com/api/food-database/v2/parser?app_id={APP_ID}&app_key={APP_KEY}&ingr={food_name}" 
    response = requests.get(API_URL)
    food_info = response.json()
    return food_info

def main(history=None):
    user_onboard_data = {
    "Sex": "Male",
    "Weight": 75,
    "Daily Activity Level": 1.6,
    "Veg/NonVeg": "Both",
    "No of meals": 3,
    "Current Meals": "Oats, Whey Protein, Almonds, Milk, Banana, Brown Bread, Eggs, Cheese Slice, Rice, Spinach, Brocolli, Chicken Breast",
    "Cheat Meals": "Chinese",
    "Reachable food": "Everything",
    "Goal": "fat-loss",
    "Food Name": "Oats",
    "Query": "What is intermittent fasting?"
    }
    section_mapping = {
        "1": "intro",
        "2": "gather_requirements",
        "3": "meal_one",
        "4": "meal_two",
        "5": "meal_three",
        "6": "final_macros",
        "7": "cheat_meal",
        "8": "replace_meal",
        "9": "food_info",
        "10": "grocery_list",
        "11": "fitness_related_questions",
        "12": "restart",
        "13": "exit"
    }

    while True:
        user_input = input("""
        Press 1 for Intro,
        Press 2 for To gather user's nutrition requirement,
        Press 3 for Design Meal number 1,
        Press 4 for Design Meal number 2,
        Press 5 for Design Meal number 3,
        Press 6 for Final Macros of nutrition plan,
        Press 7 for Design a cheat meal,
        Press 8 for Replace a meal,
        Press 9 for To know about food,
        Press 10 for Prepare a grocery list,
        Press 11 for Ask you query,
        Press 12 for Restart Nutrionist,
        Press 13 for Exit \n
        Enter the number corresponding to the desired section (1-13): """)
        
        if user_input not in section_mapping:
            print("Invalid input. Please enter a number between 1 and 13.")
            continue
        
        section = section_mapping[user_input]
        
        if section == "restart":
            history = []
            continue
        elif section == "exit":
            break
        else:
            response = nutritionist(
                message="",
                section=section,
                user_onboard_data=user_onboard_data,
                conversation_history=history
            )
        if section == "intro" or section == "gather_requirements" or section == "final_macros" or section == "cheat_meal" or section == "replace_meal" or section == "food_info" or section == "grocery_list" or section == "fitness_related_questions": 
            incom = complete_response_one(response)
            print(incom)
            if not incom:
                history.append({"role": "assistant", "content": response})
            else:
                history.append({"role": "assistant", "content": incom})
        if section == "meal_one":
            sec_incom = complete_meal_one(response)
            if not sec_incom:
                history.append({"role": "assistant", "content": response})
            else:
                history.append({"role": "assistant", "content": sec_incom})
        if section == "meal_two":
            sec_incom = complete_meal_two(response)
            if not sec_incom:
                history.append({"role": "assistant", "content": response})
            else:
                history.append({"role": "assistant", "content": sec_incom})
        if section == "meal_three":
            sec_incom = complete_meal_three(response)
            if not sec_incom:
                history.append({"role": "assistant", "content": response})
            else:
                history.append({"role": "assistant", "content": sec_incom})
        

main(history)
