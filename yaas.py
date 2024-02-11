import yaml
import sys
import os
from utils import get_user_proxy, get_assistants, get_manager

# Read configurations from configuration.yaml and do not use autogen to do so
config_file = sys.argv[1]
if os.path.isfile(config_file):
    configuration = yaml.full_load(open(config_file, "r"))

if not configuration:
    raise ValueError("Configuration file not found")

# User Proxy Agent
user_proxy = get_user_proxy(configuration["user"])

# Create a list of agents to be used in the group chat
agents = get_assistants(configuration["assistants"])

if "manager" in configuration:
    # If there is a manager, prepend the user proxy to the agents list
    agents = [user_proxy] + agents
    manager = get_manager(configuration["manager"], agents)
    user_proxy.initiate_chat(manager, message=configuration["task"])
else:
    user_proxy.initiate_chat(
        agents[0],
        message=configuration["task"],
        summary_method="reflection_with_llm",
    )
