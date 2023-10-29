import taipy as tp
from taipy.gui import Gui, notify
import cohere
import pandas as pd

prompt = ('1. Do CS221 HW (most important) \n2. Read POLS206 textbook \n3. Workout \n4. Read HIST105 novel \n'
          '5. Prep for datathon (least important)')
co = cohere.Client('s0Sws2fzSjJPeXu0zXwztHc9RisE1A8TVKxBkDgY')
response = ''
feedback = ''


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
###Schedule Builder

<|layout|columns=1 1|

<|first column
<|container|
Input your daily priorities:
<|{prompt}|input|class_name=schedule-input|multiline|>
<|Generate|button|on_action=generate_schedule|class_name=plain|>
|>
|>

<|second column
<|container|
Feedback on this schedule:
<|{feedback}|input|multiline|>
<|Submit|button|on_action=submit_feedback|class_name=plain|>
|>
|>

|>

<br/>
<|container|
Generated Schedule: <br/>
<|{response}|input|class_name=schedule-result|multiline|>
|>
<br/>

"""

Gui(page).run(use_reloader=True, port=5001)
