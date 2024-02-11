import autogen
import yaml
import sys
import os

default_llm_config = {"temperature": 0.3, "max_tokens": 2048}

# Read configurations from configuration.yaml and do not use autogen to do so
config_file = sys.argv[1]
if os.path.isfile(config_file):
    full_configuration = yaml.full_load(open(config_file, "r"))

if not full_configuration:
    raise ValueError("Configuration file not found")

# User Proxy Agent
user = full_configuration["user"]
arguments = {
    "name": user["name"],
    "human_input_mode": user["human_input_mode"],
    "max_consecutive_auto_reply": user["max_consecutive_auto_reply"],
    "is_termination_msg": lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    "code_execution_config": user["code_execution_config"],
    "llm_config": {
        "config_list": [user["config_list"]],
        **default_llm_config,
    },
}
if "system_message" in user:
    arguments["system_message"] = user["system_message"]
user_proxy = autogen.UserProxyAgent(**arguments)

# Create a list of agents to be used in the group chat
agents = []

# Loop through all assistants and create an agent for each of them
configuration = {}
for assistant in full_configuration["assistants"]:
    configuration[assistant["identifier"]] = {
        "config_list": [assistant["config_list"]]
    }

    configuration[assistant["identifier"]]["llm_config"] = {
        "config_list": configuration[assistant["identifier"]]["config_list"],
        **default_llm_config,
    }

    assistentArguments = {
        "name": assistant["identifier"],
        "llm_config": configuration[assistant["identifier"]]["llm_config"],
    }
    if "system_message" in assistant:
        assistentArguments["system_message"] = assistant["system_message"]
    if "seed" in assistant:
        assistentArguments["seed"] = assistant["seed"]

    configuration[assistant["identifier"]]["agent"] = autogen.AssistantAgent(**assistentArguments)

    agents.append(configuration[assistant["identifier"]]["agent"])

if "manager" in full_configuration:
    # If there is a manager, prepend the user proxy to the agents list
    agents.prepend(user_proxy)
    # Create a group chat and a manager
    groupchat = autogen.GroupChat(agents=agents, messages=[], max_round=10)
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config={
            "config_list": full_configuration["manager"]["config_list"],
            **default_llm_config,
        },
    )
    user_proxy.initiate_chat(manager, message=full_configuration["task"])
else:
    user_proxy.initiate_chat(
        agents[0],
        message=full_configuration["task"],
        summary_method="reflection_with_llm",
    )
