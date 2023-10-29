from taipy.gui import Gui, notify
import openai as oa
from dotenv import load_dotenv
import os

load_dotenv()
oa.api_key = os.environ.get('OPENAI_API_KEY')
oa.Model.list()

# Default state values (only refer to state.var_name when modifying them)
schedule_prompt = ('1. Do CS221 HW (most important) \n2. Read POLS206 textbook \n3. Workout \n4. Read HIST105 novel \n'
                   '5. Prep for datathon (least important)')
generated_schedule = ''
schedule_feedback = ''
task_categories = {'Category': [], 'Count': []}


def generate_schedule(state):
    notify(state, 'I', 'Generating Schedule...', duration=4000)
    state.generated_schedule = oa.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a schedule-building assistant used in an academic setting, designed"
                                          "to help students optimize their daily schedules."},
            {"role": "user", "content": f"Generate a single-day schedule for me with the following priorities: "
                                        f"{state.schedule_prompt}"
                                        f"The items in this list are ordered from most important (1) to least important"
                                        f"I want you to return the result in a CSV format, "
                                        f"and I don't want any commentary on the info"},
        ]
    )['choices'][0]['message']['content']
    notify(state, 'S', 'Finished generating schedule')
    categorize_tasks(state)


def submit_feedback(state):
    notify(state, 'I', 'Implementing feedback...', duration=4000)
    state.generated_schedule = oa.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a schedule-building assistant used in an academic setting, designed"
                                          "to help students optimize their daily schedules."},
            {"role": "user", "content": f"""Here is the schedule you gave me: \"{state.generated_schedule}\"
                                            Here is my feedback: {state.schedule_feedback}.
                                            Regenerate the schedule with this feedback in mind.
                                            Provide your answer in a CSV format. Do not tell me anything about the
                                            data and do not provide my old data back to me."""},
        ]
    )['choices'][0]['message']['content']
    notify(state, 'S', 'Finished updating schedule')
    categorize_tasks(state)


def categorize_tasks(state):
    categories_str = oa.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a schedule-building assistant used in an academic setting, designed"
                                          "to help students optimize their daily schedules."},
            {"role": "user", "content": f"""Here is my schedule: \"{state.generated_schedule}\"
                                        For each task/item in the schedule, I want you to simply provide the category of
                                        that item (this also needs to be in a CSV format)
                                        Examples of categories I'm looking for include: Academic, Fitness, Leisure,
                                        Career, etc.
                                        Example of the format I'm looking for: \"Academic, Academic, Fitness, Leisure\"
                                        Do not provide commentary and do not provide headers columns"""}
        ]
    )['choices'][0]['message']['content']
    categories_copy = {'Category': ['Sample Task'], 'Count': [1]}
    for category in categories_str.split(','):
        categories_copy['Category'].append(category)
        categories_copy['Count'].append(1)
    state.task_categories = categories_copy

# def format_chart_data(state):
#     if len(state.generated_schedule) < 2:
#         return
#
#     state.chart_data['Time'].clear()
#     state.chart_data['Task'].clear()
#     for line in state.generated_schedule.split('\n')[1:]:
#         line = line.split(',')
#         state.chart_data['Time'].append(line[0])
#         state.chart_data['Task'].append(line[1])


page_md = """
#ScheduMate

<|layout|

<|container|
**Input daily priorities:**
<|{schedule_prompt}|input|class_name=schedule-input|multiline|>
<|Generate|button|on_action=generate_schedule|class_name=plain|>
|>

<|container|
**Feedback:**
<|{schedule_feedback}|input|multiline|>
<|Submit|button|on_action=submit_feedback|class_name=plain|>
|>

<|container|
**Generated Schedule:**
<|{generated_schedule}|input|class_name=schedule-result|multiline|>
|>

<|container|
**Task Categories:**
<|{task_categories}|chart|type=pie|values=Count|labels=Category|>
|>

|>
"""

Gui(page=page_md).run(use_reloader=True, dark_mode=False, title="ScheduMate", port=5001)
