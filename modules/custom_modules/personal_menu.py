import questionary
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

from ..ui import display_journal_instructions, display_panel, display_journal_saved_message, display_error_message, clear_screen
from ..editor_engine.main_e import e_main
from .journal.journals import journal_menu
from .finance_manage.finance import finance_menu
import os
import logging
from datetime import datetime

bindings = KeyBindings()

def personal():  # Main method
    clear_screen()
    
    options = [
        "1: Journals",
        "2: TODOs",
        "3: Blog",
        "4: Finance management",
        "5: Goal setting and tracking",
        "6: Task prioritization",
        "7: Weather integration",
        "8: News feed",
        "9: Main Menu"
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
    elif choice == options[3]:
        finance_menu()
    elif choice == options[4]:
        goal_setting_and_tracking()
    elif choice == options[5]:
        task_prioritization()
    elif choice == options[6]:
        weather_integration()
    elif choice == options[7]:
        news_feed()
    elif choice == options[8]:
        return_home()

def goal_setting_and_tracking():
    # Implement goal-setting and tracking features
    pass

def task_prioritization():
    # Implement task prioritization features
    pass

def weather_integration():
    # Integrate weather API (e.g., OpenWeatherMap)
    pass

def news_feed():
    # Fetch articles from reputable sources (e.g., RSS feeds) and display them
    pass

def return_home():
    pass