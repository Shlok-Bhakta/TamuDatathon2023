import taipy as tp
from taipy import Gui
import cohere

prompt = ('1. Do CS221 HW (most important) \n2. Read POLS206 textbook \n3. Workout \n4. Read HIST105 novel \n'
          '5. Prep for datathon (least important)')
co = cohere.Client('s0Sws2fzSjJPeXu0zXwztHc9RisE1A8TVKxBkDgY')
response = 'test'


def button_pressed(state):
    result = co.generate(
        prompt=f"""Generate a single-day schedule for me with the following priorities: {prompt} Only give me the list
               with times and tasks.""",
        max_tokens=200
    )[0].text
    state.response = result
    print(result)


page = """
###Scheduler Builder

<|layout|columns=1 1|

<|first column
<|container|
Input your daily priorities: <br/>
<|{prompt}|input|class_name=schedule-input|multiline|> <br/>
<|Generate|button|on_action=button_pressed|class_name=plain|>
|>
|>

<|second column
<|container|
Generated Schedule: <br/>
<|{response}|input|class_name=schedule-result|multiline|>
|>
|>

|>
"""

Gui(page).run(use_reloader=True, port=5001)
