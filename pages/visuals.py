from taipy.gui import Markdown

data = {
  "Country": ["Rest of the world", "Russian Federation", "Peru"],
  "Area": [1445674.66, 815312, 72330.4]
}

visuals_md = Markdown("""
<|navbar|>
<|{data}|chart|type=pie|values=Area|labels=Country|>
""")
