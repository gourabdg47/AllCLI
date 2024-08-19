from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import time
import os

console = Console()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome_message():
    """Display the welcome message."""
    # clear_screen()
    console.print(Panel(Text("Welcome to the Modern CLI", justify="center", style="bold magenta")))

def display_panel(message, title=None, style="bold green"):
    """Display a panel with a custom message."""
    clear_screen()
    console.print(Panel(message, title=title, style=style))

def display_exit_message():
    """Display exit message."""
    clear_screen()
    console.print(Panel("Exiting the application. Goodbye!", title="Exit", style="bold red"))
    time.sleep(0.7)
    clear_screen()

def display_journal_instructions():
    """Display instructions for writing a journal entry."""
    clear_screen()
    # console.print("[bold yellow]Type your journal entry below. Press Ctrl + S to save automatically.[/bold yellow]")
    # console.print("[bold red]Press Ctrl + C to cancel and return to the main menu.[/bold red]")
    
    console.print("[bold yellow]Press ENTER to choose default.[/bold yellow]")
    console.print("[bold red]Type 'exit-' to go back to main menu[/bold red]")

def display_journal_saved_message(filename):
    """Display a message when the journal entry is saved."""
    clear_screen()
    console.print(f"Journal saved as [bold green]{filename}[/bold green]")
    console.print(f"[bold yellow]Press ENTER to return to main menu.[/bold yellow]")

def display_error_message(error):
    """Display an error message."""
    console.print(Panel(f"ERROR: {error}", style="bold red"))
