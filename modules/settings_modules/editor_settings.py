import questionary

from ..ui import display_welcome_message, display_panel, display_exit_message
from modules.folder_init import logging
from .editor_conf.key_bindings import kb_main

STYLE = questionary.Style([
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

def editor_main():
    
    display_welcome_message()

    options = [
        "1: Key-bindings",
        "2: Configuration",
        "3: Main Menu"
    ]

    choice = questionary.select(
        "Choose an action:",
        choices=options,
        style=STYLE
    ).ask()

    # Handling the user's choice
    menu_actions = {
        options[0]: key_bindings,
        options[1]: editor_configurations,
        options[2]: main_menu
    }

    action = menu_actions.get(choice)
    if action:
        action()
    else:
        display_exit_message()
        exit()
        
def key_bindings():
    kb_main()

def editor_configurations():
    pass

def main_menu():
    pass