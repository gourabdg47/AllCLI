import os
import questionary
import logging
from datetime import datetime
from jinja2 import Template
from prompt_toolkit.key_binding import KeyBindings

from ...ui import (
    display_journal_instructions,
    display_panel,
    display_journal_saved_message,
    display_error_message,
    clear_screen,
)
from ...editor_engine.main_e import e_main
from ...encryption import encrypt_file, decrypt_file
from configs import config

# Global Constants
MISSION_DIR = config.MISSION_DIR
MISSION_LOG_TEMPLATE_PATH = config.MISSION_LOG_TEMPLATE_PATH

# Initialize KeyBindings
bindings = KeyBindings()

def get_user_list_input(prompt_text):
    """Prompt the user for a list of items."""
    items = []
    while True:
        item = questionary.text(f"{prompt_text} (leave blank to finish):").ask()
        if not item:
            break;
        items.append(item)
    return items

def render_mission_log_template(output_filepath, mission_data):
    """Render and save the mission log using the Jinja2 template."""
    with open(MISSION_LOG_TEMPLATE_PATH, "r") as template_file:
        mission_template = template_file.read()

    template = Template(mission_template)
    rendered_mission_log = template.render(mission_data)

    with open(output_filepath, "w") as file:
        file.write(rendered_mission_log)

def collect_mission_data():
    """Collect mission details from the user."""
    current_date = datetime.now().strftime("%B %d, %Y")
    current_time = datetime.now().strftime("%I:%M %p")

    mission_data = {
        "mission_name": questionary.text("Enter Mission Name:").ask(),
        "date": current_date,
        "time": current_time,
        "objective": questionary.text("Enter Mission Objective:").ask(),
        "tasks": get_user_list_input("Enter a task"),
        "challenges": get_user_list_input("Enter a challenge"),
        "outcome": questionary.text("Enter Outcome:").ask(),
        "next_steps": questionary.text("Enter Next Steps:").ask()
    }
    
    return mission_data

def mission():
    """Main menu to write, edit, search, or delete mission logs."""
    clear_screen()
    options = [
        "1: Write Mission Log", 
        "2: Read / Edit Mission Log", 
        "3: Search Mission Logs", 
        "4: Delete Mission Log"
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
        write_mission_log()
    elif choice == options[1]:
        edit_existing_mission_log()
    elif choice == options[2]:
        search_mission_logs() # TODO: Not working
    elif choice == options[3]:
        delete_mission_log()

def edit_existing_mission_log():
    """Allow the user to select and edit an existing mission log."""
    clear_screen()
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
            decrypt_file(os.path.join(MISSION_DIR, selected_file))
            edit_mission_log(selected_file)

    except Exception as e:
        logging.error(f"Error listing mission logs: {e}")
        display_error_message("Failed to list mission logs!")

def edit_mission_log(filename):
    """Use the custom editor engine to edit a mission log."""
    try:
        file_path = os.path.join(MISSION_DIR, filename)
        e_main(file_path)
        display_panel("Enter new password", title="Encrypt", style="bold green")
        encrypt_file(file_path)
    except Exception as e:
        logging.error(f"Error editing mission log '{filename}': {e}")
        display_error_message("Failed to edit mission log.")

def search_mission_logs():
    """Search for mission logs containing a specific keyword."""
    clear_screen()
    keyword = questionary.text("Enter a keyword to search for:").ask()

    try:
        files = [f for f in os.listdir(MISSION_DIR) if os.path.isfile(os.path.join(MISSION_DIR, f))]
        matching_files = []

        for file in files:
            decrypt_file(os.path.join(MISSION_DIR, file))
            with open(os.path.join(MISSION_DIR, file), "r") as f:
                content = f.read()
                if keyword.lower() in content.lower():
                    matching_files.append(file)
        
        if not matching_files:
            display_error_message("No matching mission logs found.")
        else:
            display_panel("\n".join(matching_files), title="Search Results", style="bold green")

    except Exception as e:
        logging.error(f"Error searching mission logs: {e}")
        display_error_message("Failed to search mission logs.")

def delete_mission_log():
    """Delete a selected mission log."""
    clear_screen()
    try:
        files = [f for f in os.listdir(MISSION_DIR) if os.path.isfile(os.path.join(MISSION_DIR, f))]
        if not files:
            display_error_message("No mission logs found.")
            return

        selected_file = questionary.select(
            "Select a mission log to delete:",
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
            os.remove(os.path.join(MISSION_DIR, selected_file))
            display_panel(f"Mission log '{selected_file}' deleted.", title="Delete Confirmation", style="bold red")

    except Exception as e:
        logging.error(f"Error deleting mission log: {e}")
        display_error_message("Failed to delete mission log.")

def write_mission_log():
    """Create a new mission log entry."""
    display_panel("Mission Log", title="Log Your Mission", style="bold green")

    mission_details = collect_mission_data()

    filepath = generate_mission_log_filepath()
    render_mission_log_template(filepath, mission_details)
    encrypt_file(filepath)

def generate_mission_log_filepath():
    """Generate a unique file path for the new mission log."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{MISSION_DIR}/mission_log_{timestamp}.txt"
    return filename
