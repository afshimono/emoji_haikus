from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import HumanMessagePromptTemplate


from prompt_loader import load_prompts

def generate_script(episode_name:str, episode_theme:str, gcp_api_key:str, llm_temperature:float, output_file:str) -> None:
    """
    Generate a script for the episode.

    Args:
        episode_name (str): The name of the episode.
        episode_theme (str): The theme of the episode.

    Returns:
        str: The generated script.
    """

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=llm_temperature, api_key=gcp_api_key)
    acidos_description, _ = load_prompts("acidos")
    zenai_description, _ = load_prompts("zenai")
    script_writer_system, script_writer_user = load_prompts("script_writer")
    system_writer = SystemMessage(content=script_writer_system)
    # parameter_list = ["EPISODE_THEME", "EPISODE_NAME","EPISODE_SCRIPT_TOTAL_WORDS","EPISODE_SCRIPT_QUESTIONS",
    #                   "EPISODE_SCRIPT_AVERAGE_ANSWER_WORDS",
    #                   "ACIDOS_DESCRIPTION","ZENAIMASTER_DESCRIPTION",]
    human_message_template = HumanMessagePromptTemplate.from_template(script_writer_user)
    param_values = {
        "EPISODE_THEME": episode_theme,
        "EPISODE_NAME": episode_name,
        "EPISODE_SCRIPT_TOTAL_WORDS": 1000,
        "EPISODE_SCRIPT_QUESTIONS": 2,
        "EPISODE_SCRIPT_AVERAGE_ANSWER_WORDS": 100,
        "ACIDOS_DESCRIPTION": acidos_description,
        "ZENAIMASTER_DESCRIPTION": zenai_description
    }
    formatted_human_message = human_message_template.format(**param_values)
    result = llm.invoke([system_writer,formatted_human_message])
    with open(output_file, "w") as f:
        f.write(result.content)

if __name__ == "__main__":
    import os
    episode_name = os.getenv('EPISODE_NAME')
    episode_theme = os.getenv('EPISODE_THEME')
    gcp_api_key = os.getenv('GOOGLE_API_KEY')
    llm_temperature = os.getenv('LLM_TEMPERATURE', 0.8)

    if not all([episode_name,episode_theme,gcp_api_key]):
        raise ValueError("Both EPISODE_NAME and EPISODE_THEME environment variables must be set.")
    generate_script(episode_name=episode_name, episode_theme=episode_theme, gcp_api_key=gcp_api_key, llm_temperature=llm_temperature,output_file="samples/script.txt")