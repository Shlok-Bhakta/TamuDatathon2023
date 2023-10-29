from taipy.gui import Markdown
import openai as oa

OPENAI_API_KEY = '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'
oa.api_key = OPENAI_API_KEY
oa.Model.list()

# Default state values (only refer to state variables)
prompt = ('1. Do CS221 HW (most important) \n2. Read POLS206 textbook \n3. Workout \n4. Read HIST105 novel \n'
          '5. Prep for datathon (least important)')
response = ''
feedback = ''
categories = []


def generate_schedule(state):
    state.response = oa.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a schedule-building assistant used in an academic setting, designed"
                                          "to help students optimize their daily schedules."},
            {"role": "user", "content": f"Generate a single-day schedule for me with the following priorities: "
                                        f"{state.prompt}"
                                        f"The items in this list are ordered from most important (1) to least important"
                                        f"I want you to return the result in a CSV format"},
        ]
    )['choices'][0]['message']['content']
    categorize_tasks(state)


def submit_feedback(state):
    state.response = oa.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a schedule-building assistant used in an academic setting, designed"
                                          "to help students optimize their daily schedules."},
            {"role": "user", "content": f"""Here is the schedule you gave me: \"{state.response}\"
                                            Here is my feedback: {state.feedback}.
                                            Regenerate the schedule with this feedback in mind.
                                            Provide your response in a CSV format."""},
        ]
    )['choices'][0]['message']['content']


def categorize_tasks(state):
    categories_str = oa.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a schedule-building assistant used in an academic setting, designed"
                                          "to help students optimize their daily schedules."},
            {"role": "user", "content": f"""Here is my schedule: \"{state.response}\"
                                        I want you to categorize the items in this schedule and provide your answer 
                                        in a csv format.
                                        Examples of categories I'm looking for include: Academic, Fitness, Leisure,
                                        Career, etc."""}
        ]
    )['choices'][0]['message']['content']


schedule_md = Markdown("""
<|navbar|>
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

""")