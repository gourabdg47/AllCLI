import questionary
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
import os
import logging
from datetime import datetime
from cryptography.fernet import Fernet  # For encryption
from ..ui import display_journal_instructions, display_panel, display_journal_saved_message, display_error_message, clear_screen
from ..editor_engine.main_e import e_main

bindings = KeyBindings()

JOURNAL_DIR = "journals"
PROMPT_FLAG = False

# Encryption key for securing logs
ENCRYPTION_KEY = b'your-encryption-key'  # You should generate a key and keep it secure

def journal():
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
        files = [f for f in os.listdir(JOURNAL_DIR) if os.path.isfile(os.path.join(JOURNAL_DIR, f))]
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
            edit_journal_entry(selected_file)

    except Exception as e:
        logging.error(f"Error listing mission logs: {e}")
        display_error_message(f"Failed to list mission logs!")

def edit_journal_entry(filename):
    try:
        file_path = os.path.join(JOURNAL_DIR, filename)
        e_main(file_path)  # Call custom editor engine to edit the log

    except Exception as e:
        logging.error(f"Error editing mission log '{filename}': {e}")
        display_error_message("Failed to edit mission log.")

def write_journal():
    display_panel("Mission Log", title="Log Your Mission", style="bold green")

    # Prompt for mission details
    mission_details = {
        "Mission Name": questionary.text("Enter Mission Name:").ask(),
        "Location": questionary.text("Enter Mission Location:").ask(),
        "Objective": questionary.text("Enter Mission Objective:").ask(),
        "Participants": questionary.text("Enter Participants:").ask()
    }

    display_journal_instructions()

    filepath = get_journal_file_path()
    e_main(filepath)  # Open the editor for detailed log entry

    save_mission_details(filepath, mission_details)  # Save the basic mission details

def get_journal_file_path():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{JOURNAL_DIR}/mission_log_{timestamp}.txt"
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

def encrypt_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            data = file.read()

        fernet = Fernet(ENCRYPTION_KEY)
        encrypted = fernet.encrypt(data)

        with open(filepath, 'wb') as file:
            file.write(encrypted)

        logging.info(f"File '{filepath}' encrypted successfully.")
    except Exception as e:
        logging.error(f"Error encrypting file '{filepath}': {e}")
        display_error_message(f"Failed to encrypt file '{filepath}'.")

def decrypt_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            data = file.read()

        fernet = Fernet(ENCRYPTION_KEY)
        decrypted = fernet.decrypt(data)

        with open(filepath, 'wb') as file:
            file.write(decrypted)

        logging.info(f"File '{filepath}' decrypted successfully.")
    except Exception as e:
        logging.error(f"Error decrypting file '{filepath}': {e}")
        display_error_message(f"Failed to decrypt file '{filepath}'.")

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
    filename = f"{JOURNAL_DIR}/mission_log_{timestamp}.txt"
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