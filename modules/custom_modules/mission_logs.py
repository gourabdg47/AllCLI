import questionary
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
import os
import logging
from datetime import datetime
from ..ui import display_journal_instructions, display_panel, display_journal_saved_message, display_error_message, clear_screen
from ..editor_engine.main_e import e_main
from ..encryption import encrypt_file, decrypt_file  # Import the encryption functions

from jinja2 import Template
from datetime import datetime


bindings = KeyBindings()

MISSION_DIR = "mission_logs"
PROMPT_FLAG = False
MISSION_LOG_TEMPLATE = "templates/mission_logs/mission_log_template.jinja"

_MISSION_DATA = {}


def get_list_input(prompt_text):
    
    items = []
    while True:
        item = questionary.text(f"{prompt_text} (leave blank to finish):").ask()
        if not item:
            break
        items.append(item)
    return items

def access_template(write_filepath, mission_data):
    # Loading the template from the file
    with open(MISSION_LOG_TEMPLATE, "r") as template_file:
        mission_template = template_file.read()
        
    # Create a Template object
    template = Template(mission_template)

    # Render the template with data
    rendered_mission_log = template.render(mission_data)
    print("rendered_mission_log: ", rendered_mission_log)
    print("write_filepath: ", write_filepath)
    # Write the rendered log to a text file
    with open(write_filepath, "w") as file:
        file.write(rendered_mission_log)
        
def get_mission_data():
    # Get today's date and current time
    current_date = datetime.now().strftime("%B %d, %Y")
    current_time = datetime.now().strftime("%I:%M %p")
    
    _MISSION_DATA = {
        "mission_name": questionary.text("Enter Mission Name:").ask(),
        "date": current_date,  # Automatically set to today's date
        "time": current_time,  # Automatically set to the current time
        "objective": questionary.text("Enter Mission Objective:").ask(),
        "tasks": get_list_input("Enter a task"),
        "challenges": get_list_input("Enter a challenge"),
        "outcome": questionary.text("Enter Outcome:").ask(),
        "next_steps": questionary.text("Enter Next Steps:").ask()
    }
    
    return _MISSION_DATA


def mission():
    clear_screen()
    options = [
        "1: Write Mission Log",
        "2: Read / Edit Mission Log"
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
        read_edit_journal()

def read_edit_journal():
    try:
        files = [f for f in os.listdir(MISSION_DIR) if os.path.isfile(os.path.join(MISSION_DIR, f))]
        if not files:
            display_error_message("No mission logs found.")
            return

        selected_file = questionary.select(
            "Select a mission log to edit:",
            choices=files,
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

        if selected_file:
            decrypt_file(os.path.join(MISSION_DIR, selected_file))  # Decrypt the file before editing
            edit_journal_entry(selected_file)

    except Exception as e:
        logging.error(f"Error listing mission logs: {e}")
        display_error_message(f"Failed to list mission logs!")

def edit_journal_entry(filename):
    try:
        file_path = os.path.join(MISSION_DIR, filename)
        e_main(file_path)  # Call custom editor engine to edit the log
        encrypt_file(file_path)  # Re-encrypt the file after editing

    except Exception as e:
        logging.error(f"Error editing mission log '{filename}': {e}")
        display_error_message("Failed to edit mission log.")

def write_journal():
    display_panel("Mission Log", title="Log Your Mission", style="bold green")

    mission_details = get_mission_data()

    display_journal_instructions()

    filepath = get_journal_file_path()
    # e_main(filepath)  # Open the editor for detailed log entry

    # save_mission_details(filepath, mission_details)  # Save the basic mission details
    access_template(filepath, mission_details)
    # encrypt_file(filepath)  # Encrypt the file after writing ### TODO: uncomment

def get_journal_file_path():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{MISSION_DIR}/mission_log_{timestamp}.txt"
    return filename

def save_mission_details(filepath, details):
    try:
        with open(filepath, 'a') as file:
            for key, value in details.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")
        logging.info(f"Mission details saved in {filepath}")
        
    except Exception as e:
        logging.error(f"Error saving mission details: {e}")
        display_error_message("Failed to save mission details.")

def save_and_ask(journal_entry):
    try:
        sanitized_entries = [entry if entry is not None else '' for entry in journal_entry]
        entry = '\n'.join(sanitized_entries)
        save_journal_to_file(entry)
        logging.info("Mission log entry successfully saved.")
    except Exception as e:
        display_error_message(f"An error occurred while saving the mission log: {e}")
        logging.error(f"An error occurred while saving the mission log: {e}", exc_info=True)

def save_journal_to_file(entry):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{MISSION_DIR}/mission_log_{timestamp}.txt"
    with open(filename, "w") as file:
        file.write(entry)
    encrypt_file(filename)  # Encrypt the file after saving
    display_journal_saved_message(filename)
    logging.info(f"Mission log saved as {filename}")

def ask_return_to_menu():
    return_to_menu = questionary.confirm("Would you like to return to the main menu?").ask()
    if return_to_menu:
        from ..menu import main_menu
        main_menu()
    else:
        new_entry = questionary.confirm("Would you like to enter a new mission log?").ask()
        if new_entry:
            write_journal()
        else:
            ask_return_to_menu()
