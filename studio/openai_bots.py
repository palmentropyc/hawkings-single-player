import os
from colorama import init, Fore, Style
from openai import OpenAI


# Inicializar colorama
init()



def crear_assistant_openai(api_key, name, prompt):
    client = OpenAI(api_key=api_key)
    
    print(f"{Fore.GREEN}API Key: {api_key}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Name: {name}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Prompt: {prompt}{Style.RESET_ALL}")
    try:
        assistant = client.beta.assistants.create(
            name=name,
            instructions=prompt,
            model="gpt-4o",
            tools=[{"type": "file_search"}],
        )        

        return assistant.id
    except Exception as e:
        print(f"{Fore.RED}Error al crear o actualizar el asistente: {str(e)}{Style.RESET_ALL}")
        return None
