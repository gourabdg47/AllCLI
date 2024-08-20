import questionary

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

import os
import logging
from datetime import datetime

from ..ui import display_journal_instructions, display_panel, display_journal_saved_message, display_error_message, clear_screen
from .mission.mission_logs import mission

bindings = KeyBindings()


def work_menu(): # Main method
    
    clear_screen()
    options = [
        "1: Missions",
        "2: TODO",
        "3: Task Manager",
        "4: Main Menu"
    ]

    choice = questionary.select(
        "Choose an action:",
        choices=options,
        style=questionary.Style([
            ('qmark', 'fg:#E91E63 bold'),
            ('question', 'fg:#673AB7 bold'),
            ('answer', 'fg:#2196F3 bold'),
            ('pointer', 'fg:#03A9F4 bold'),
            ('highlighted', 'fg:#03A9F4 bold'),
            ('selected', 'fg:#4CAF50 bold'),
            ('separator', 'fg:#E0E0E0'),
            ('instruction', 'fg:#9E9E9E'),
            ('text', 'fg:#FFFFFF'),
            ('disabled', 'fg:#757575 italic')
        ])
    ).ask()

    if choice == options[0]:
        mission()
    elif choice == options[1]:
        pass
    elif choice == options[2]:
        pass
    elif choice == options[3]:
        return_home()
    
def return_home():
    pass




