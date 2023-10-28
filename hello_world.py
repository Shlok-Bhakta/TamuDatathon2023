import taipy as tp
from taipy import Config, Core, Gui


################################################################
#            Configure application                             #
################################################################
def build_message(name):
    return f"Hello {name}!"


# A first data node configuration to model an input name.
input_name_data_node_cfg = Config.configure_data_node(id="input_name")
# A second data node configuration to model the message to display.
message_data_node_cfg = Config.configure_data_node(id="message")
# A task configuration to model the build_message function.
build_msg_task_cfg = Config.configure_task("build_msg", build_message, input_name_data_node_cfg, message_data_node_cfg)
# The scenario configuration represents the whole execution graph.
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])

################################################################
#            Design graphical interface                        #
################################################################

input_name = "Taipy"
message = None
test = 2


def submit_scenario(state):
    state.scenario.input_name.write(state.input_name)
    state.scenario.submit()
    state.message = scenario.message.read()
    state.test = 1234


page = """
Name: <|{input_name}|input|>

<|submit|button|on_action=submit_scenario|>

Message: <|{message}|text|> <br/>
Number: <|{test}|text|>
"""

if __name__ == "__main__":
    ################################################################
    #            Instantiate and run Core service                  #
    ################################################################
    Core().run()

    ################################################################
    #            Manage scenarios and data nodes                   #
    ################################################################
    scenario = tp.create_scenario(scenario_cfg)

    ################################################################
    #            Instantiate and run Gui service                   #
    ################################################################

    Gui(page).run(use_reloader=True, port=5001)

