import questionary

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

import os
import logging
from datetime import datetime

from ...ui import display_journal_instructions, display_panel, display_journal_saved_message, display_error_message, clear_screen
from ...editor_engine.main_e import e_main

bindings = KeyBindings()



JOURNAL_DIR = "journals"
PROMPT_FLAG = False


def journal_menu():
    
    clear_screen()
    options = [
        "1: Write Journal",
        "2: My Journals",
        "3: Main menu"
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
    elif choice == options[2]:
        return_home()
        
def write_journal():
    # display_panel("Journal Entry", title="Write Your Journal", style="bold green")

    session = PromptSession()
    journal_entry = []
    line_number = 1
    global PROMPT_FLAG
    PROMPT_FLAG = False

    display_journal_instructions()

    # @bindings.add('c-s')
    # def save_journal(event):
    #     global PROMPT_FLAG
    #     save_and_ask(journal_entry)
    #     # display_panel("Press ENTER to return to main menu.", style="bold green")
    #     PROMPT_FLAG = True

    # while not PROMPT_FLAG:
    #     try:
    #         prompt_text = f"{line_number}: "
    #         line = session.prompt(prompt_text, key_bindings=bindings)

    #         if line and line.lower() == "save-me":
    #             logging.info("User requested to save journal entry.")
    #             save_and_ask(journal_entry)
    #             ask_return_to_menu()
    #             break

    #         if line:
    #             journal_entry.append(line)
    #             logging.debug(f"Appended line {line_number} to journal entry: {line}")
    #             line_number += 1

    #     except KeyboardInterrupt:
    #         display_panel("Exiting journal entry mode.", style="bold red")
    #         logging.warning("User exited journal entry mode with KeyboardInterrupt.")
    #         ask_return_to_menu()
    #         break

    #     except Exception as e:
    #         display_error_message(e)
    #         logging.error(f"An error occurred: {e}", exc_info=True)
    #         ask_return_to_menu()
    #         break
    
    # Calling custom editor engoine 
    filepath = get_journal_file_path()
    e_main(filepath)
    
def read_edit_journal():
    # List all journal entries in the specified folder
    try:
        files = [f for f in os.listdir(JOURNAL_DIR) if os.path.isfile(os.path.join(JOURNAL_DIR, f))]
        if not files:
            display_error_message("No journal entries found.")
            return

        selected_file = questionary.select(
            "Select a journal entry to edit:",
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
        logging.error(f"Error listing journal entries: {e}")
        display_error_message(f"Failed to list journal entries!")
        
def edit_journal_entry(filename):
    try:
        file_path = os.path.join(JOURNAL_DIR, filename)
        e_main(file_path)
        
        # with open(file_path, 'r') as file:
        #     content = file.read()

        # new_content = questionary.text(f"Editing {filename}:", default=content).ask()

        # if new_content != content:  # Check if there were any changes
        #     with open(file_path, 'w') as file:
        #         file.write(new_content)
        #     display_journal_saved_message(f"Journal entry '{filename}' saved successfully.")
        # else:
        #     display_journal_saved_message("No changes were made.")

    except Exception as e:
        logging.error(f"Error editing journal entry '{filename}': {e}")
        display_error_message("Failed to edit journal entry.")



def get_journal_file_path():
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # get journal name from user
    user_journal_name = questionary.text(f"Enter Journal Name [DEFAULT: journal_{timestamp}.txt]: ").ask()
    if user_journal_name:
        if user_journal_name == 'exit-':
            # exit()
            from ...menu import main_menu
            main_menu()
        filename = f"journals/{user_journal_name}.txt"
    else:
        filename = f"journals/journal_{timestamp}.txt"
    
    return filename

def save_and_ask(journal_entry):
    try:
        sanitized_entries = [entry if entry is not None else '' for entry in journal_entry]
        entry = '\n'.join(sanitized_entries)
        save_journal_to_file(entry)

        logging.info("Journal entry successfully saved.")
    except Exception as e:
        display_error_message(f"An error occurred while saving the journal: {e}")
        logging.error(f"An error occurred while saving the journal: {e}", exc_info=True)

def save_journal_to_file(entry):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"journals/journal_{timestamp}.txt"
    with open(filename, "w") as file:
        file.write(entry)

    display_journal_saved_message(filename)
    logging.info(f"Journal saved as {filename}")

def ask_return_to_menu():
    return_to_menu = questionary.confirm("Would you like to return to the main menu?").ask()
    if return_to_menu:
        from ...menu import main_menu
        main_menu()
    else:
        new_entry = questionary.confirm("Would you like to enter a new journal entry?").ask()
        if new_entry:
            write_journal()
        else:
            ask_return_to_menu()