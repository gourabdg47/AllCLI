import questionary

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

import os
import logging
from datetime import datetime

from ...ui import display_journal_instructions, display_panel, display_journal_saved_message, display_error_message, clear_screen
from ...editor_engine.main_e import e_main

bindings = KeyBindings()

def finance_menu():
    clear_screen()
    pass