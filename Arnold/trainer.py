import openai
import datetime

openai.api_key = "sk-"
history = []


def trainer(message, section, user_onboard_data, conversation_history=None):
    # Customize the prompt based on the section
    training_level = user_onboard_data.get("Training Level", "Beginner")
    query = user_onboard_data.get("Query", "")
    log = user_onboard_data.get("Logbook", "")
    training_days_perweek = 4
    compound_lifts = [["Barbell Bench Press", "Barbell Shoulder Press", "Weighted Bar Dips"], ["Stiff Leg Deadlift", "Conventional Deadlift", "Weighted Pullups"], ["Barbell Squats", "Barbell Front Squats"]]
    exercises = [["Dumbbell Incline press", "Pec Dec Fly"],["Dumbell Shoulder Press", "Cable Lateral Raises"],["Triceps Machine Pushdown", "Rope Overhead Triceps Extensions"],["Seated Back Row", "Lat Pull Down"],["Barbell Shrugs, Dumbbell Shrugs"],["Biceps Preacher Curls", "Cable Biceps Curls"],["Leg Press", "Leg Extensions", "Leg Curls"],["Bodyweight Calf Raises", "Barbell Calf Raises"],["Weighted Decline Crunches", "Leg Raises"]]
    rep_range = "9 to 15 reps"
    injury = user_onboard_data.get("Injury", "None")
    
    prompt = ""

    def training_approach(training_level, sets_per_exercise=0):
        if training_level == "Beginner":
           approach = "Full Body"
           sets_per_exercise = 1
           sample_plan = {
            "Monday": [
            {"exercise": "Bench Press", "sets": 1, "reps": "9-15"},
            {"exercise": "Barbell Rows", "sets": 1, "reps": "9-15"},
            {"exercise": "Triceps Rope Extensions", "sets": 1, "reps": "9-15"},
            {"exercise": "Biceps Curls", "sets": 1, "reps": "9-15"},
            {"exercise": "Leg Press", "sets": 1, "reps": "9-15"},
            {"exercise": "Leg Extensions", "sets": 1, "reps": "9-15"},
            {"exercise": "Leg Raises", "sets": 1, "reps": "9-15"}
            ],
            "Wednesday": [
            {"exercise": "Barbell Squats", "sets": 1, "reps": "9-15"},
            {"exercise": "Dumbbell Lunges", "sets": 1, "reps": "9-15"},
            {"exercise": "Standing Hamstring Curls", "sets": 1, "reps": "9-15"},
            {"exercise": "Chest Press", "sets": 1, "reps": "9-15"},
            {"exercise": "Lat Pull Down", "sets": 1, "reps": "9-15"},
            {"exercise": "Triceps Skull Crusher", "sets": 1, "reps": "9-15"},
            {"exercise": "Decline Crunches", "sets": 1, "reps": "9-15"}
            ],
            "Friday": [
            {"exercise": "Barbell Shoulder Press", "sets": 1, "reps": "9-15"},
            {"exercise": "Dumbell Incline Press", "sets": 1, "reps": "9-15"},
            {"exercise": "Triceps Pushdown", "sets": 1, "reps": "9-15"},
            {"exercise": "Dumbell Biceps Curls", "sets": 1, "reps": "9-15"},
            {"exercise": "Leg Extensions", "sets": 1, "reps": "9-15"},
            {"exercise": "Leg Curls", "sets": 1, "reps": "9-15"},
            {"exercise": "Leg Raises", "sets": 1, "reps": "9-15"}
            ],
            "Sunday": [
            {"exercise": "Barbell Front Squats", "sets": 1, "reps": "9-15"},
            {"exercise": "Walking Lunges", "sets": 1, "reps": "9-15"},
            {"exercise": "Standing Hamstring Curls", "sets": 1, "reps": "9-15"},
            {"exercise": "Weighted Pushups", "sets": 1, "reps": "9-15"},
            {"exercise": "Weighted Pullups", "sets": 1, "reps": "9-15"},
            {"exercise": "Triceps Rope Extensions", "sets": 1, "reps": "9-15"},
            {"exercise": "Biceps Spider Curls", "sets": 1, "reps": "9-15"},
            ]
        }

        elif training_level == "Intermediate":
            approach = "Upper Body And Lower Body"
            sets_per_exercise = 2
            sample_plan = {}
        elif training_level == "Advance":
            approach = "Push Session, Pull Session, Pull Session"
            sets_per_exercise = 3
            sample_plan = {}
        return approach, sets_per_exercise, sample_plan

    approach, sets_per_exercise, sample_plan = training_approach(training_level)


    if section == "intro":
        prompt = "Your name is Arnold AI, a large language model trained by OpenAI. You are an experienced fitness coach specializing in desiging workout plans for muscle building. \n"
    elif section == "gather_requirements":
        prompt = f"""Given a user with training level {training_level}, design a training plan following these constraints: 1) use the {approach} method, 2) train {training_days_perweek} days per week, 3) have {sets_per_exercise} sets per exercise, 4) rep range of {rep_range}, 5) include two compound lifts from {compound_lifts} in each session, and 6) choose remaining exercises from {exercises}. Donot create the plan at this stage, just confirm do you understand the requirements?"""
    elif section == "sample_workout_plan":
            prompt = f""" Workout Plan : {sample_plan}. Provide the workout plan for all days that are mentioned in sample plan in a particular clean format to the user like Days: Monday, Exercise - Sets - Reps, Remove all the brackets. Do the task step by step. Donot provide any extra information to the user at this stage."""
    elif section == "replace_exercise":
        prompt = f"If user wants to change any exercise, provide any two alternatives from {compound_lifts} or {exercises}, with 9-15 reps and {sets_per_exercise} sets. Do it step by step. "
    elif section == "logbook_approach":
        prompt = f"User last training session log was {log}. If user hits reps more than the half of the rep range, Suggest user to increase weight by 2.5kg, otherwise suggest user to hit the same weight and try to get more reps."
    elif section == "injury":
        prompt = f"User is suffering from {injury} injury. Please manage user's training plan by executing the exercises that will effect the targeted injury muslce. Choose alternatives of exercises that will help in rehab of the user's injury. Think it through step by step. "
    elif section == "home_workout":
        prompt = f"Provide a quick home workout for user in case if user's misses the gym. Do you understand the requirement?"
    elif section == "fitness_related_questions":
        prompt = f"Fitness Question:{query}"

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
        temperature=0,
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
        temperature=0,
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
            prompt = f"Please complete the remaining response without changing the context : '{last_words}'"
            response = complete_the_remaining_response(prompt)
    return response

def main(history=None):
    user_onboard_data = {
    "Training Level": "Beginner",
    "Injury": "Rotator Cuff",
    "Query": "",
    "Logbook":"Weight: 50kg, Set:1, Reps 9",
    }
    section_mapping = {
        "1": "intro",
        "2": "gather_requirements",
        "3": "sample_workout_plan",
        "4": "workout_plan",
        "5": "injury",
        "6": "logbook_approach",
        "7": "fitness_related_questions",
        "8": "home_workout",
        "9": "restart",
        "10": "exit"
    }

    while True:
        user_input = input("""
        Press 1 for Intro,
        Press 2 for To gather user's training requirement,
        Press 3 for Just Press you know!,
        Press 4 for To get customized plan,
        Press 5 for rehab exercises,
        Press 6 for training log suggestion,
        Press 7 for queries,
        Press 8 for home workout,
        Press 9 for Restart Arnold,
        Press 10 for Exit \n
        Enter the number corresponding to the desired section (1-10): """)
        
        if user_input not in section_mapping:
            print("Invalid input. Please enter a number between 1 and 10.")
            continue
        
        section = section_mapping[user_input]
        
        if section == "restart":
            history = []
            continue
        elif section == "exit":
            break
        else:
            response = trainer(
                message="",
                section=section,
                user_onboard_data=user_onboard_data,
                conversation_history=history
            )
        if section == "intro" or section == "gather_requirements" or section == "sample_workout_plan" or section == "workout_plan" or section == "home_workout" or section == "logbook_approach" or section == "injury" or section == "fitness_related_questions": 
            incom = complete_response_one(response)
            if not incom:
                history.append({"role": "assistant", "content": response})
            else:
                history.append({"role": "assistant", "content": incom})        

main(history)
