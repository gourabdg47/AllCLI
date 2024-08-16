import questionary
from .ui import display_welcome_message, display_panel, display_exit_message
from .custom_modules.journal import journal

def main_menu():
    display_welcome_message()

    options = [
        "1: Write Journal",
        "2: Configure Settings",
        "3: Start Process",
        "4: Donate to the dev",
        "5: Exit"
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
        journal()
    elif choice == options[1]:
        configure_settings()
    elif choice == options[2]:
        start_process()
    elif choice == options[3]:
        donate()
    elif choice == options[4]:
        exit_app()

def configure_settings():
    display_panel("Settings: Configure your preferences", title="Settings", style="bold yellow")
    # Implement settings logic

def start_process():
    display_panel("Process: The process has started", title="Process", style="bold blue")
    # Implement process logic

def donate():
    display_panel("Donate $$$ for this app development!", title="Donate", style="bold red")
    # Implement donation logic

def exit_app():
    display_exit_message()
    exit()
