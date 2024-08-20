import questionary

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

import os
import logging
from datetime import datetime

from ..ui import display_journal_instructions, display_panel, display_journal_saved_message, display_error_message, clear_screen
from ..editor_engine.main_e import e_main
from .journal.journals import journal_menu
from .finance_manage.finance import finance_menu

bindings = KeyBindings()

        


def personal(): # Main method
    
    clear_screen()
    
    options = [
        "1: Journals",
        "2: Finance management ",
        "3: Main Menu"
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
        journal_menu()
    elif choice == options[1]:
        finance_menu()
    elif choice == options[2]:
        return_home()
    
def return_home():
    pass




