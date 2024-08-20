import questionary
import os
import logging
from datetime import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

from ...ui import (
    display_journal_instructions,
    display_panel,
    display_journal_saved_message,
    display_error_message,
    clear_screen
)
from ...editor_engine.main_e import e_main
from configs import config

bindings = KeyBindings()

JOURNAL_DIR = config.JOURNAL_DIRECTORY
SAVE_FLAG = False

def journal_menu():
    """Display the journal menu and handle user input."""
    clear_screen()
    options = [
        "1: Write Journal",
        "2: My Journals",
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
        write_journal()
    elif choice == options[1]:
        clear_screen()
        read_or_edit_journal()
    elif choice == options[2]:
        return_to_main_menu()

def write_journal():
    """Create a new journal entry using the custom editor engine."""
    journal_filepath = get_journal_filepath()
    e_main(journal_filepath)

def read_or_edit_journal():
    """Display a list of journal entries for the user to select and edit."""
    try:
        journal_files = [f for f in os.listdir(JOURNAL_DIR) if os.path.isfile(os.path.join(JOURNAL_DIR, f))]
        if not journal_files:
            display_error_message("No journal entries found.")
            return

        selected_journal = questionary.select(
            "Select a journal entry to edit:",
            choices=journal_files,
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

        if selected_journal:
            edit_journal(selected_journal)

    except Exception as e:
        logging.error(f"Error listing journal entries: {e}")
        display_error_message("Failed to list journal entries!")

def edit_journal(filename):
    """Edit the selected journal entry using the custom editor engine."""
    try:
        journal_filepath = os.path.join(JOURNAL_DIR, filename)
        e_main(journal_filepath)
    except Exception as e:
        logging.error(f"Error editing journal entry '{filename}': {e}")
        display_error_message("Failed to edit journal entry.")

def get_journal_filepath():
    """Generate a file path for the journal entry, based on user input or the current timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    user_journal_name = questionary.text(f"Enter Journal Name [DEFAULT: journal_{timestamp}.txt]: ").ask()

    if user_journal_name:
        if user_journal_name.lower() == 'exit-':
            return_to_main_menu()
        return f"{JOURNAL_DIR}/{user_journal_name}.txt"
    else:
        return f"{JOURNAL_DIR}/journal_{timestamp}.txt"

def return_to_main_menu():
    """Return to the main menu."""
    from ...menu import main_menu
    main_menu()
