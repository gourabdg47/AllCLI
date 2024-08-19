#!/bin/python3
import sys
import os
import time
from copy import deepcopy

# Attempt to import the `curses` library, which is used to create text-based user interfaces in the terminal.
# If the platform is Windows and `curses` is not available, the script tries to install and import `windows-curses`.
try:
    import curses
except ImportError:
    if sys.platform.startswith('win'):
        try:
            os.system('pip install windows-curses')
            import curses
        except Exception as e:
            print("Failed to install windows-curses:", e)
            sys.exit(1)

# Importing `rich` for enhanced terminal output, including formatted text and panels for help messages.
from rich import print
from rich.panel import Panel

# Function to display beautifully formatted help text using `rich`.
# This function is invoked when the user requests help or provides the `--help` command-line argument.
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
    print(Panel(help_text, title="[bold magenta]Help[/bold magenta]"))

# Main function which is wrapped by `curses.wrapper` to handle terminal initialization and cleanup.
# This function contains the core logic of the text editor, 
# handling input, rendering, and managing the editor's state.
def main(stdscr):
    # Initialize the screen and set various terminal modes.
    # `nodelay` makes `getch()` non-blocking, `noecho` prevents keypresses from being echoed to the screen,
    # and `raw` disables line buffering and special handling of certain keys.
    screen = curses.initscr()
    screen.nodelay(1)
    curses.noecho()
    curses.raw()

    # Initialize editor state variables.
    # `mode` tracks the current mode (e.g., 'normal', 'insert').
    # `buffer` stores the text content, `yank_buffer` stores copied text, and `undo_buffer` tracks undo history.
    mode = 'normal'
    buffer = []
    yank_buffer = []
    undo_buffer = []
    filename = 'noname.txt'  # Default filename if none is provided
    undo_index = -1
    rows, cols = screen.getmaxyx()  # Get terminal size
    rows -= 1  # Reserve the last row for the status bar
    view_x, view_y, cursor_row, cursor_col = [0] * 4  # Initialize viewport and cursor positions
    input_buffer = ''  # Buffer to store input for commands like 'G' (go to line)

    # Handle command-line arguments.
    # If a filename is provided, the file's content is loaded into `buffer`.
    # If '--help' is passed, the help text is displayed and the program exits.
    if len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            display_help()
            sys.exit(0)
        filename = sys.argv[1]
        try:
            with open(filename) as file:
                content = file.read().split('\n')
                content = content[:-1] if len(content) > 1 else content
                for line in content:
                    buffer.append([ord(c) for c in line])
        except:
            buffer.append([])
    else:
        buffer.append([])

    # Save the initial state of the buffer for undo functionality.
    undo_index += 1
    undo_buffer.insert(undo_index, [deepcopy(buffer), [cursor_row, cursor_col]])

    # Main event loop: continuously handle user input and update the screen.
    while True:
        # Adjust viewport based on cursor position to keep it within view.
        screen.move(0, 0)
        if cursor_row < view_y:
            view_y = cursor_row
        if cursor_row >= view_y + rows:
            view_y = cursor_row - rows + 1
        if cursor_col < view_x:
            view_x = cursor_col
        if cursor_col >= view_x + cols:
            view_x = cursor_col - cols + 1
        
        # Render the text buffer on the screen within the current viewport.
        for row in range(rows):
            buffer_row = row + view_y
            for col in range(cols):
                buffer_col = col + view_x
                try:
                    screen.addch(row, col, buffer[buffer_row][buffer_col])
                except:
                    pass 
            screen.clrtoeol()
            try:
                screen.addstr('\n') if buffer_row < len(buffer) else screen.addstr('~\n')
            except:
                pass
        
        # Display the status bar, showing the current mode, filename, line/column number, and percentage through the file.
        status = f"Mode: {mode} | File: '{filename}' | Line: {cursor_row + 1}/{len(buffer)} ({int((cursor_row + 1) * 100 / len(buffer))}%) | Col: {cursor_col}"
        screen.addstr(status)
        screen.clrtoeol()
        curses.curs_set(0)
        screen.move(cursor_row - view_y, cursor_col - view_x)
        curses.curs_set(1)
        screen.refresh()

        # Get user input; `getch` is non-blocking, so it waits for input.
        key = -1
        while key == -1:
            key = screen.getch()

        # Handle terminal resizing by adjusting rows and columns based on the new terminal size.
        if key == curses.KEY_RESIZE:
            rows, cols = screen.getmaxyx()
            rows -= 1
            screen.refresh()
            view_y = 0

        # Process numeric input for commands like 'G'.
        if chr(key).isdigit() and chr(key) != '0' and mode not in ['insert', 'replace', 'open']:
            input_buffer += chr(key)

        # Process commands in normal mode, handling keypresses to change modes or manipulate text.
        elif mode == 'normal':
            if key == ord('i'):
                mode = 'insert'
            elif key == ord('a'):
                cursor_col += 1
                mode = 'insert'
            elif key == ord('A'):
                cursor_col = len(buffer[cursor_row])
                mode = 'insert'
            elif key == ord('o'):
                buffer.insert(cursor_row + 1, [])
                cursor_row += 1
                mode = 'open'
            elif key == ord('O'):
                buffer.insert(cursor_row, [])
                mode = 'open'
            elif key == ord('r'):
                mode = 'replace_char'
            elif key == ord('R'):
                mode = 'replace'
            elif key == ord('x') and len(buffer[cursor_row]):
                del buffer[cursor_row][cursor_col]
            elif key == ord('G'):
                cursor_row = int(input_buffer) - 1 if len(input_buffer) and int(input_buffer) - 1 < len(buffer) else len(buffer) - 1
            elif key == ord('g'):
                cursor_row = 0
                cursor_col = 0
            elif key == ord('0'):
                if input_buffer == '':
                    cursor_col = 0
                else:
                    input_buffer += chr(key)
            elif key == ord('$'):
                if len(input_buffer):
                    cursor_row = cursor_row + int(input_buffer) - 1 if (cursor_row + int(input_buffer) - 1) < len(buffer) else cursor_row
                cursor_col = len(buffer[cursor_row]) - 1
            elif key == ord('d'):
                mode = 'delete'
            elif key == ord('y'):
                mode = 'yank'
            elif key == ord('p'):
                for line in yank_buffer:
                    if len(buffer) > 1:
                        cursor_row += 1
                    buffer.insert(cursor_row, deepcopy(line))
                undo_index += 1
                undo_buffer.insert(undo_index, [deepcopy(buffer), [cursor_row, cursor_col]])
            elif key == ord('u'):
                if undo_index >= 1:
                    undo_index -= 1
                    buffer = deepcopy(undo_buffer[undo_index][0])
                    cursor_row, cursor_col = undo_buffer[undo_index][1]
            elif key == (ord('r') & 0x1f):
                if undo_index < len(undo_buffer) - 1:
                    undo_index += 1
                    buffer = deepcopy(undo_buffer[undo_index][0])
                    cursor_row, cursor_col = undo_buffer[undo_index][1]
            elif key == ord('h'):
                cursor_col -= 1 if cursor_col else 0
            elif key == ord('l'):
                cursor_col += 1 if cursor_col < len(buffer[cursor_row]) - 1 else 0
            elif key == ord('k'):
                cursor_row -= 1 if cursor_row else 0
            elif key == ord('j'):
                cursor_row += 1 if cursor_row < len(buffer) - 1 else 0
            current_row = buffer[cursor_row] if cursor_row < len(buffer) else None
            len_current_row = len(current_row) if current_row is not None else 0
            if cursor_col > len_current_row - 1:
                cursor_col = len_current_row - 1 if len_current_row else len_current_row
            if key == ord('A'):
                cursor_col = len_current_row
            if key != ord('0') and mode not in ['delete', 'yank']:
                input_buffer = ''

        # Process commands in insert and open modes, where the user is entering text.
        elif mode in ['insert', 'open']:
            if key == 27:
                mode = 'normal'
                cursor_col -= 1 if cursor_col else 0
            elif key != ((key) & 0x1f) and key < 128:
                buffer[cursor_row].insert(cursor_col, key)
                cursor_col += 1
            elif key == ord('\n'):
                line_content = buffer[cursor_row][cursor_col:]
                buffer[cursor_row] = buffer[cursor_row][:cursor_col]
                cursor_row += 1
                cursor_col = 0
                buffer.insert(cursor_row, [] + line_content)
            elif key == curses.KEY_BACKSPACE:
                if cursor_col:
                    cursor_col -= 1
                    del buffer[cursor_row][cursor_col]
                elif cursor_row:
                    line_content = buffer[cursor_row][cursor_col:]
                    del buffer[cursor_row]
                    cursor_row -= 1
                    cursor_col = len(buffer[cursor_row])
                    buffer[cursor_row] += line_content

        # Replace a single character at the cursor position in `replace_char` mode.
        elif mode == 'replace_char':
            try:
                buffer[cursor_row][cursor_col] = key
            except:
                pass
            mode = 'normal'

        # Process continuous replacement of characters in `replace` mode.
        elif mode == 'replace':
            if key == 27:
                mode = 'normal'
                cursor_col -= 1 if cursor_col else 0
            elif key != ((key) & 0x1f) and key < 128:
                buffer[cursor_row][cursor_col] = key
                cursor_col += 1
            elif key == curses.KEY_BACKSPACE:
                cursor_col -= 1 if cursor_col else 0

        # Process deletion of lines in `delete` mode.
        elif mode == 'delete':
            if key == ord('d'):
                yank_buffer = []
                num_lines = int(input_buffer) if len(input_buffer) else 1
                for i in range(num_lines):
                    if len(buffer) == 1 and buffer[0] == []:
                        break
                    yank_buffer.append(buffer[cursor_row])
                    if len(buffer) > 1:
                        del buffer[cursor_row]
                    elif len(buffer) == 1:
                        buffer[cursor_row] = []
                    if cursor_row and cursor_row == len(buffer):
                        cursor_row -= 1
                        cursor_col = 0
            mode = 'normal'
            input_buffer = ''
            screen.move(rows, 0)

        # Process yanking (copying) of lines in `yank` mode.
        elif mode == 'yank':
            if key == ord('y'):
                yank_buffer = []
                num_lines = int(input_buffer) if len(input_buffer) else 1
                for i in range(num_lines):
                    if cursor_row + i >= len(buffer):
                        break
                    yank_buffer.append(buffer[cursor_row + i])
            mode = 'normal'
            input_buffer = ''
            screen.move(rows, 0)

        # Save the buffer state to the undo history whenever text is changed.
        if (key != 27 and mode in ['insert', 'replace', 'open', 'delete', 'yank']):
            undo_index += 1
            undo_buffer.insert(undo_index, [deepcopy(buffer), [cursor_row, cursor_col]])

        # Quit the editor if the user presses `Ctrl+Q`.
        if key == (ord('q') & 0x1f):
            sys.exit()

        # Save the document if the user presses `Ctrl+S`.
        if key == (ord('s') & 0x1f):
            content = ''
            for line in buffer:
                content += ''.join([chr(c) for c in line]) + '\n'
            with open(filename, 'w') as file:
                file.write(content)
            screen.move(rows, 0)
            screen.addstr('Saved')
            screen.clrtoeol()
            screen.refresh()
            time.sleep(1)

# Set ESCDELAY environment variable for better responsiveness of escape sequences.
# This minimizes the delay in recognizing escape sequences.
os.environ.setdefault('ESCDELAY', '25')

# Run the `main` function using the `curses.wrapper`, 
# which ensures the terminal is properly initialized and cleaned up.
curses.wrapper(main)
