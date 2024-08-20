from rich import print
from rich.panel import Panel
from rich.console import Console

import time
import keyboard

console = Console()


def display_help():
    help_text = """
        [bold cyan]Key Bindings:[/bold cyan] 
            [bold]i[/bold]      - Enter [bold]insert[/bold] mode
            [bold]a[/bold]      - Enter [bold]insert[/bold] mode after the cursor
            [bold]A[/bold]      - Enter [bold]insert[/bold] mode at the end of the line
            [bold]o[/bold]      - Open a new line below the current line
            [bold]O[/bold]      - Open a new line above the current line
            [bold]r[/bold]      - Replace the character at the cursor
            [bold]R[/bold]      - Enter [bold]replace[/bold] mode
            [bold]x[/bold]      - Delete the character at the cursor
            [bold]G[/bold]      - Go to the line number entered before pressing G
            [bold]g[/bold]      - Go to the top of the document
            [bold]0[/bold]      - Move to the beginning of the line
            [bold]$[/bold]      - Move to the end of the line
            [bold]d[/bold]      - Start delete operation (press 'd' again to delete the current line)
            [bold]y[/bold]      - Start yank (copy) operation (press 'y' again to yank the current line)
            [bold]p[/bold]      - Paste the last deleted or yanked text
            [bold]u[/bold]      - Undo the last operation
            [bold]Ctrl+R[/bold] - Redo the last undone operation
            [bold]h[/bold]      - Move cursor left
            [bold]l[/bold]      - Move cursor right
            [bold]k[/bold]      - Move cursor up
            [bold]j[/bold]      - Move cursor down
            [bold]Ctrl+S[/bold] - Save the document
            [bold]Ctrl+Q[/bold] - Quit the editor
        """
        
    console.print(Panel(help_text, title="[bold magenta]Help[/bold magenta]"))
    
def kb_main():
    display_help()
    
    # Wait for the user to press the Esc key to exit
    print("\n[bold yellow]Press [bold magenta]Esc[/bold magenta] to exit...[/bold yellow]")
    keyboard.wait('esc')
    print("\n[bold green]Exiting...[/bold green]")