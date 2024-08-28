from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from time import sleep

import os

console = Console()

# Function to render the panels
def render_panels(panel1, panel2, panel3):
    layout = Layout()
    layout.split_column(
        Panel(panel1, title="Panel 1"),
        Panel(panel2, title="Panel 2"),
        Panel(panel3, title="Panel 3"),
    )
    return layout

# Initial content for the panels
panel1_content = "Initial content for Panel 1"
panel2_content = "Initial content for Panel 2"
panel3_content = "Initial content for Panel 3"

iteration = 0
while True:
    sleep(1)
    iteration += 1

    # Update only Panel 2's content
    panel2_content = f"Updated content for Panel 2 - Iteration {iteration}"

    # Clear the console and render the updated panels
    console.clear()
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(render_panels(panel1_content, panel2_content, panel3_content))
