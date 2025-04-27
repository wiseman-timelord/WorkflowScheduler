# Script: `.\scripts\temporary.py`

# Imports
import gradio as gr
import os

# Globals
events_state = gr.State()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "data", "persistence.json")