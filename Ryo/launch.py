import json
from apik import tgtr_apik
from app import deepseek_call
import gradio as gr
from gradio.themes.base import Base



with open("character_profiles/ryo.json", "r") as reader:
    ryo = json.load(reader)

tgtr_apik = tgtr_apik()

def web_chat(user_input, history):
    return deepseek_call(user_input, chat=history)[1]

custom_css = """
.message.user {
    background-color: #f2b54e !important; /* amber bubble */
}
.message.user * {
    color: black !important;  /* ensure all nested elements like span, p, strong, etc. are black */
    font-weight: 800
}
.message.bot {
    background-color: #302b28 !important;aun
}

"""


with gr.Blocks(css=custom_css,theme=gr.themes.Citrus(primary_hue="amber", neutral_hue="stone", font=
                                      [gr.themes.GoogleFont("Comfortaa")])) as demo:
    gr.ChatInterface(
        web_chat,
        type="messages",
        chatbot=gr.Chatbot(height=500),
        title="Zen Chatbot",
        description="Chat with Zen",
)
    
demo.launch()