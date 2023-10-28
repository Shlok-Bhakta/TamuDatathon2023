import taipy as tp
from taipy import Gui
import cohere
import pandas as pd

prompt = ('1. Do CS221 HW (most important) \n2. Read POLS206 textbook \n3. Workout \n4. Read HIST105 novel \n'
          '5. Prep for datathon (least important)')
co = cohere.Client('s0Sws2fzSjJPeXu0zXwztHc9RisE1A8TVKxBkDgY')
response = ''
feedback = ''

food_df = pd.DataFrame({
    "Meal": ["Lunch", "Dinner", "Lunch", "Lunch", "Breakfast", "Breakfast", "Lunch", "Dinner"],
    "Category": ["Food", "Food", "Drink", "Food", "Food", "Drink", "Dessert", "Dessert"],
    "Name": ["Burger", "Pizza", "Soda", "Salad", "Pasta", "Water", "Ice Cream", "Cake"],
    "Calories": [300, 400, 150, 200, 500, 0, 400, 500],
})


def generate_schedule(state):
    state.response = co.generate(
        prompt=f"""Generate a single-day schedule for me with the following priorities: {prompt} Only give me a list 
               with times and tasks.""",
        max_tokens=125
    )[0].text


def submit_feedback(state):
    state.response = co.generate(
        prompt=f"""Here is the schedule you gave me: \"{prompt}\"
                Here is my feedback: {feedback}.
                Regenerate the schedule with this feedback in mind; only give me a list with times and tasks.""",
        max_tokens=125
    )[0].text


page = """
###Scheduler Builder

<|layout|columns=1 1|

<|first column
<|container|
Input your daily priorities: <br/>
<|{prompt}|input|class_name=schedule-input|multiline|> <br/>
<|Generate|button|on_action=generate_schedule|class_name=plain|>
|>
|>

<|second column
<|container|
Generated Schedule: <br/>
<|{response}|input|class_name=schedule-result|multiline|>
|>
|>

|>

<br/>
<|container|
Feedback on this schedule:
<|{feedback}|input|multiline|> <br />
<|Submit|button|on_action=submit_feedback|class_name=plain|>
|>
<br/>
<|{food_df}|table|>

"""

Gui(page).run(use_reloader=True, port=5001)
