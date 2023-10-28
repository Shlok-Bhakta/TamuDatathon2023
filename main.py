from taipy import Gui
import pandas as pd

value = 10

section1 = """
#Our Very First Taipy Application

<|layout|columns=1 1 1|

<|first column
<|container container-styling|
###Slider 1 <br/>
Slider value: <|{value}|> <br/>
<|{value}|slider|>
|>
|>

<|second column
<|container container-styling|
###Slider 2 <br/>
Slider value: <|{value}|> <br/>
<|{value}|slider|>
|>
|>

<|third column
<|container container-styling|
###Slider 3 <br/>
Slider value: <|{value}|> <br/>
<|{value}|slider|>
|>
|>

|>
"""
section2 = """
<|layout|columns=1 4|

<|container container-styling|
<|{content}|file_download|label=Download|>
|>

<|{data}|chart|type=bar|x=Country|y=Average Age|orientation=v|>

|>
"""


def get_data(path: str):
    dataset = pd.read_csv(path)
    return dataset


data = get_data("average_age.csv")
content = "average_age.csv"

Gui(page=section1+section2, css_file='main.css').run(use_reloader=True, port=5001)

#Gui(page="Hello *World*").run(use_reloader=True, port=5001)