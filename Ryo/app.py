import json
from prompt_engine import build_prompt
from apik import tgtr_apik
import requests
import regex as re

with open("character_profiles/ryo.json", "r") as reader:
    ryo = json.load(reader)

tgtr_apik = tgtr_apik()

def deepseek_call(user_input, chat): #user_input = user's msg to chatbot/ Ryo; current convo log
    chat_prompt = build_prompt(user_input, ryo, chat) 
    # chat_prompt is a string containing instructions to the system to behave like Ryo (system_prompt),
    # the user's input message (user_input)
    response = requests.post( #API call to the TogetherAI API
        "https://api.together.xyz/inference",
        headers={
            "Authorization": f"Bearer {tgtr_apik}",
            "Content-Type": "application/json"
        },
        json={ # JSON object containing the parameters for the API call
            "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free", # DeepSeek model through TogetherAI
            "prompt": chat_prompt,
            "max_tokens": 1000, # maximum number of tokens in the response
            "temperature": 0.7, # controls the randomness of the response
            # lower temperature means the response is more predictable and focused,
            # while higher temperature means the response is more random and creative
        }
    )


    full_response = response.json()["output"]["choices"][0]["text"] # includes the full "thinking" process of the model

    # Extract Ryo's reply from the full response
    all_options = re.findall(r'"[^"]+"', full_response) #Must be double quotes at the start and end of the string.
    # Between those quotes, there must be at least (hence, +) one character, which can be anything 
    # except a double quote (hence, [^"]).
    # The character class that we have defined over here is called a negated double-quotes character class.
    # That is, the class contains any character except a double quote.
    if len(all_options) >= 1 and all_options[-1][1:-1] != user_input:
            ryo_reply = all_options[-1][1:-1]  # Just the first line
    else:
        ryo_reply = "It seems like I am having trouble generating a response.\
                Please refresh this message to try again. Alternatively, please provide \
                    me a new message to respond to."
    #ryo_reply = full_response
    return chat_prompt, ryo_reply #both are strings

def new_chat(): #start a new chat with Ryo
    chat = "" #chat log, which is empty at the start of a new chat
    print("You can start chatting with Zen now. Type 'quit' to end the chat.")
    chat_status = True #default chat activated
    while chat_status: #while the chat is active/ user has not typed "quit"
        user_input = input("You: ") #user inputs their message
        if user_input == "quit": #if the user explicitely writes "quit", chat ends
            chat_status = False #chat deactivated
            print("Chat ended. Thank you for chatting with Zen!")
        else:
            deepseek_response = deepseek_call(user_input, chat) # else user's input is 
            # sent to the system to respond as Ryo
            # deepseek_response is a tuple of chat_prompt and ryo_reply
            chat_prompt = deepseek_response[0] #system_prompt (personality/ quirks/ instructions etc. to 
            # deepseek to behave like Ryo), user's input msg
            ryo_reply = deepseek_response[1] #ryo's extracted response
            print("Zen: ",ryo_reply) #printing out Ryo's response to display it to the user
            
            # Append the interaction to the chat log
            
            interaction = "user: " + user_input + "\n" + \
                        "ryo: " + ryo_reply + "\n"
            # brief summary of the user's input and Ryo's response
            # to be added to the chat log
            chat += interaction #updating the chat log with the latest interaction
            #chat is essentially the memory of the conversation so far, and is updated in the
            # system_prompt for each interaction to provide context for Ryo's responses
            