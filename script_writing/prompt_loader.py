from typing import Tuple

def load_from_file(file_path:str)->str:
    """
    Load the content from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file.
    """
    with open(file_path, 'r') as file:
        content = file.read()
        split_content = content.split("--system-end--")
        return split_content[0], split_content[1] if len(split_content) > 1 else ""

def load_prompts(agent:str)->Tuple[str,str]:
    """
    Load the prompts for the specified agent.

    Args:
        agent (str): The name of the agent.

    Returns:
        Tuple[str, str]: The prompt and the system message.
    """
    if agent == "script_writer":
        prompt, system_message = load_from_file("base/TheScriptWriter.md")
    elif agent == "acidos":
        prompt, system_message = load_from_file("base/AcidOSs.md")
    elif agent == "zenai":
        prompt, system_message = load_from_file("base/ZenAIMaster.md")
    else:
        raise ValueError(f"Unknown agent: {agent}")

    return prompt, system_message