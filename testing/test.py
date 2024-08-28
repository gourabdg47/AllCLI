import curses
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def draw_info_window(info_win):
    # Create a Rich Console for the welcome message
    console = Console(record=True)

    # Create a rich text panel as the information message
    welcome_text = Text("Welcome to Vim-like Interface!", style="bold green")
    instructions_text = Text("\nYou can type commands at the bottom.\nType :q to quit.", style="dim")
    additional_info = Text("\nThis is where different information will be displayed.", style="italic")

    # Combine the messages into a panel
    info_panel = Panel(welcome_text + instructions_text + additional_info, title="Information", border_style="blue")

    # Render the panel into a string that can be printed with curses
    console.print(info_panel)
    welcome_output = console.export_text()

    # Display the rich text in the info window
    info_win.clear()
    for idx, line in enumerate(welcome_output.splitlines()):
        info_win.addstr(idx, 0, line[:info_win.getmaxyx()[1]])
    info_win.refresh()

    # Display the menu
    menu_options = [
        "1: Personal",
        "2: Work",  # Mission logs, etc.
        "3: Settings",   # Configs, Templates, Preferences
        "4: Support Development",  # Donation option
        "5: Exit"
    ]
    for idx, option in enumerate(menu_options):
        info_win.addstr(idx + len(welcome_output.splitlines()) + 1, 0, option)
    info_win.refresh()

def handle_menu_selection(info_win, option):
    info_win.clear()
    if option == '1':
        info_win.addstr(0, 0, "Personal Information Selected")
    elif option == '2':
        info_win.addstr(0, 0, "Work Information Selected")
    elif option == '3':
        info_win.addstr(0, 0, "Settings Selected")
    elif option == '4':
        info_win.addstr(0, 0, "Support Development Selected")
    elif option == '5':
        info_win.addstr(0, 0, "Exiting...")
    else:
        info_win.addstr(0, 0, "Invalid Option")
    info_win.refresh()

def main(stdscr):
    # Get screen dimensions
    height, width = stdscr.getmaxyx()

    # Create two windows: one for information and one for the command panel
    info_height = height - 3  # Reserve 3 lines for the command panel
    info_win = curses.newwin(info_height, width, 0, 0)
    cmd_win = curses.newwin(3, width, info_height, 0)

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    # Draw the initial content in the info window
    draw_info_window(info_win)

    # Create a status bar for the command window
    statusbar_str = "COMMAND MODE -- :q to quit | Press 'i' to enter input mode | Choose option (1-5)"
    cmd_win.attron(curses.color_pair(1))
    cmd_win.addstr(1, 0, statusbar_str)
    cmd_win.addstr(1, len(statusbar_str), " " * (width - len(statusbar_str) - 1))
    cmd_win.attroff(curses.color_pair(1))
    cmd_win.refresh()

    # Enter command mode
    command_mode = True
    input_str = ""

    while True:
        # Move cursor to command window input position
        cmd_win.move(1, len(":") + 1)

        # Get user input
        if command_mode:
            key = cmd_win.getch()

            # Handle user input
            if key == ord(':'):  # Command mode
                cmd_win.clear()
                cmd_win.addstr(1, 0, ":")
                cmd_win.refresh()
                command_mode = False
                input_str = ""
            elif key == ord('i'):  # Insert mode
                command_mode = False
                input_str = ""
                cmd_win.clear()
            elif key in (ord('1'), ord('2'), ord('3'), ord('4'), ord('5')):
                # Handle menu selection
                handle_menu_selection(info_win, chr(key))
                if key == ord('5'):
                    break
                command_mode = True
                cmd_win.clear()
                cmd_win.attron(curses.color_pair(1))
                cmd_win.addstr(1, 0, statusbar_str)
                cmd_win.addstr(1, len(statusbar_str), " " * (width - len(statusbar_str) - 1))
                cmd_win.attroff(curses.color_pair(1))
                cmd_win.refresh()
            elif key == ord('q'):
                break

        # Handle input
        if not command_mode:
            key = cmd_win.getch()
            if key == ord('\n'):
                # Enter pressed, process the command
                command_mode = True
                cmd_win.clear()
                cmd_win.attron(curses.color_pair(1))
                cmd_win.addstr(1, 0, statusbar_str)
                cmd_win.addstr(1, len(statusbar_str), " " * (width - len(statusbar_str) - 1))
                cmd_win.attroff(curses.color_pair(1))
                cmd_win.refresh()
            elif key == 27:  # ESC key
                command_mode = True
                cmd_win.clear()
                cmd_win.attron(curses.color_pair(1))
                cmd_win.addstr(1, 0, statusbar_str)
                cmd_win.addstr(1, len(statusbar_str), " " * (width - len(statusbar_str) - 1))
                cmd_win.attroff(curses.color_pair(1))
                cmd_win.refresh()
            else:
                input_str += chr(key)
                cmd_win.addstr(1, len(":") + len(input_str), chr(key))
                cmd_win.refresh()

curses.wrapper(main)
