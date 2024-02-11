import autogen

default_llm_config = {"temperature": 0.3, "max_tokens": 2048}


def get_user_proxy(configuration):
    """
    Create and return a UserProxyAgent object based on the given configuration.

    Args:
        configuration (dict): A dictionary containing the configuration parameters.

    Returns:
        UserProxyAgent: An instance of the UserProxyAgent class.

    """
    arguments = {
        "name": configuration["name"],
        "human_input_mode": configuration["human_input_mode"],
        "max_consecutive_auto_reply": configuration["max_consecutive_auto_reply"],
        "is_termination_msg": lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        "code_execution_config": configuration["code_execution_config"],
        "llm_config": {
            "config_list": [configuration["config_list"]],
            **default_llm_config,
        },
    }
    if "system_message" in configuration:
        arguments["system_message"] = configuration["system_message"]
    return autogen.UserProxyAgent(**arguments)


def get_assistants(configuration):
    """
    Create and return a list of AssistantAgent objects based on the given configuration.

    Args:
        configuration (list): A list of dictionaries representing the configuration for each assistant.

    Returns:
        list: A list of AssistantAgent objects.

    """
    assistants = []
    for assistant in configuration:
        arguments = {
            "name": assistant["identifier"],
            "llm_config": {
                "config_list": [assistant["config_list"]],
                **default_llm_config,
            },
        }
        if "system_message" in assistant:
            arguments["system_message"] = assistant["system_message"]
        if "seed" in assistant:
            arguments["seed"] = assistant["seed"]

        agent = autogen.AssistantAgent(**arguments)
        assistants.append(agent)

    return assistants


def get_manager(configuration, agents):
    """
    Create and return a GroupChatManager object.

    Parameters:
    - configuration (dict): A dictionary containing configuration information.
    - agents (list): A list of agents participating in the group chat.

    Returns:
    - GroupChatManager: A GroupChatManager object.

    """
    # Create a group chat and a manager
    groupchat = autogen.GroupChat(agents=agents, messages=[], max_round=10)
    return autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config={
            "config_list": [configuration["config_list"]],
            **default_llm_config,
        },
    )
