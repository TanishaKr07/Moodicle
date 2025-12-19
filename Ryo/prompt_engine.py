import json
import numpy as np

def build_prompt(user_input, character, chat):
    role = character["role"]
    personality = ", ".join(character["personality"])
    quirks = ", ".join(character["quirks"])
    #eg_dialogs = "\n- " + "\n- ".join(character["example_dialogs"])
    instructions = "You are Zen, the user's personal trained therapist. \
        You reflect on the user's entries in an introspective and thoughtful way. \
            You are not just another chatbot, you are the user's companion, and someone \
                who helps the user make sense of their own emotions. Encourage the user to \
                    open up, ask questions to the user, offer advice if you can.\
                        Whatever you intend on saying to the user, put it in double quotations always.\
                            This is the most important part to distinguish your thinking from what you \
                                actually end up saying to the user.\n\n"
    
    system_prompt =  (
        f"{role}"
        f"Your personality is {personality}. "
        f"You have the following quirks: {quirks}. " 
        #wrapping the eg_dialog in quotations with the help of the escape character \
        f"{instructions}"
        f"You have had the following conversation with the user till now: {chat}\
            "
    ) #concatenates all the multiple individual strings in this string-only tuple into a single, long string
    #print(chat)

    
    chat_prompts = (
        f"system: {system_prompt}\n"
        f"Reply only as Zen to the user's message: {user_input}\n"
        #f"Respond in a way that is consistent with your personality and quirks in one line only.\n"
    )
    #DeepSeek expects the prompt to be a single string, so we concatenate all parts into one string.
    #This is different from how OpenAI expects the prompt to be a list of messages.
    #Use OpenAI's format if you want to use a gpt-3.5-turbo model.
    return chat_prompts