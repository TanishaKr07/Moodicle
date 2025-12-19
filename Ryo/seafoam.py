from __future__ import annotations
from typing import Iterable
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
import time

import json
from apik import tgtr_apik
from app import deepseek_call
import gradio as gr

with open("character_profiles/ryo.json", "r") as reader:
    ryo = json.load(reader)

tgtr_apik = tgtr_apik()

def web_chat(user_input, history):
    return deepseek_call(user_input, chat=history)[1]

class CoffeeTheme(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.amber,
        secondary_hue: colors.Color | str = colors.rose,
        neutral_hue: colors.Color | str = colors.stone,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font | str | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Quicksand"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font | str | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            body_background_fill="*neutral_900",
            body_background_fill_dark="*neutral_900",
            button_primary_text_color="white",
            block_title_text_weight="600",
            block_border_width="2px",
            block_shadow="*shadow_drop_md",
            button_primary_shadow="*shadow_drop_lg",
            button_large_padding="28px",
        )

coffee = CoffeeTheme()

with gr.Blocks(theme=coffee) as demo:
    gr.ChatInterface(
        web_chat,
        type="messages",
        chatbot=gr.Chatbot(height=500),
        title="Ryo Chatbot",
        description="Chat with Ryo"
    )

demo.launch()