import questionary

from .ui import display_welcome_message, display_panel, display_exit_message
from modules.folder_init import logging

from modules.custom_modules.personal_menu import personal
from modules.custom_modules.mission.mission_logs import mission
from modules.settings_modules.settings_menu import settings_main

from modules.custom_modules.work_menu import work_menu

# Centralized style configuration
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

def main_menu():
    
    """Display the main menu and handle user selection."""
    display_welcome_message()

    options = [
        "1: Personal",
        "2: Work",  # Mission logs, etc.
        "3: Settings",   # Configs, Templates, Preferences
        "4: Support Development",  # Donation option
        "5: Exit"
    ]

    choice = questionary.select(
        "Choose an action:",
        choices=options,
        style=STYLE
    ).ask()

    # Handling the user's choice
    menu_actions = {
        options[0]: personal,
        options[1]: work_menu,
        options[2]: settings_main,
        options[3]: donate,
        options[4]: exit_app
    }

    action = menu_actions.get(choice)
    if action:
        action()
    else:
        display_exit_message()
        exit()



def donate():
    """Provide users with an option to donate to support development."""
    display_panel("Support the development of this app", title="Donate", style="bold red")
    # TODO: Implement donation logic here

def exit_app():
    """Exit the application gracefully."""
    display_exit_message()
    exit()

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        # Handle unexpected errors gracefully
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        display_panel("An error occurred. Exiting the application.", title="Error", style="bold red")
        exit(1)
