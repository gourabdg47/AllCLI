import questionary

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

import logging
from datetime import datetime

from ..ui import display_journal_instructions, display_panel, display_journal_saved_message, display_error_message

bindings = KeyBindings()
PROMPT_FLAG = False

def write_journal():
    display_panel("Journal Entry", title="Write Your Journal", style="bold green")

    session = PromptSession()
    journal_entry = []
    line_number = 1
    global PROMPT_FLAG
    PROMPT_FLAG = False

    display_journal_instructions()

    @bindings.add('c-s')
    def save_journal(event):
        global PROMPT_FLAG
        save_and_ask(journal_entry)
        # display_panel("Press ENTER to return to main menu.", style="bold green")
        PROMPT_FLAG = True

    while not PROMPT_FLAG:
        try:
            prompt_text = f"{line_number}: "
            line = session.prompt(prompt_text, key_bindings=bindings)

            if line and line.lower() == "save-me":
                logging.info("User requested to save journal entry.")
                save_and_ask(journal_entry)
                ask_return_to_menu()
                break

            if line:
                journal_entry.append(line)
                logging.debug(f"Appended line {line_number} to journal entry: {line}")
                line_number += 1

        except KeyboardInterrupt:
            display_panel("Exiting journal entry mode.", style="bold red")
            logging.warning("User exited journal entry mode with KeyboardInterrupt.")
            ask_return_to_menu()
            break

        except Exception as e:
            display_error_message(e)
            logging.error(f"An error occurred: {e}", exc_info=True)
            ask_return_to_menu()
            break

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
        from .menu import main_menu
        main_menu()
    else:
        new_entry = questionary.confirm("Would you like to enter a new journal entry?").ask()
        if new_entry:
            write_journal()
        else:
            ask_return_to_menu()
