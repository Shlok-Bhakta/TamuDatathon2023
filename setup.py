import taipy as tp
from taipy import Config
from taipy import Core

def build_message(name: str):
    return f"Hello {name}!"


input_name_data_node_cfg = Config.configure_data_node(id="input_name")
message_data_node_cfg = Config.configure_data_node(id="message")
build_msg_task_cfg = Config.configure_task("build_msg", build_message, input_name_data_node_cfg, message_data_node_cfg)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])


if __name__ == "__main__":
    Core().run()


hello_scenario = tp.create_scenario(scenario_cfg)
hello_scenario.input_name.write("Taipy")
hello_scenario.submit()
print(hello_scenario.message.read())


from taipy import Gui
import taipy as tp

page = """
Name: <|{input_name}|input|>
<|submit|button|on_action=submit_scenario|>

Message: <|{message}|text>
"""

input_name = "Taipy"
message = None


def submit_scenario(state):
    state.scenario.input_name.write(state.input_name)
    state.scenario.submit(wait=True)
    state.message = scenario.message.read()


if __name__ == "main":
    Core.run()
    scenario = tp.create_scenario(scenario_cfg)
    Gui(page).run()
