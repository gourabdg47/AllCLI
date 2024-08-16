#!/bin/python3
import sys
import os
import time
from copy import deepcopy

# Conditional import for curses
# The curses library is used to create text-based user interfaces in the terminal.
# Since curses is not natively available on Windows, we attempt to install and import windows-curses if the platform is Windows.
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

# Help text for key bindings
# This multi-line string provides a list of all key bindings supported by the editor.
# It serves as a reference for users to understand how to interact with the editor.
HELP_TEXT = """
Key Bindings:
    i      - Enter insert mode
    a      - Enter insert mode after the cursor
    A      - Enter insert mode at the end of the line
    o      - Open a new line below the current line
    O      - Open a new line above the current line
    r      - Replace the character at the cursor
    R      - Enter replace mode
    x      - Delete the character at the cursor
    G      - Go to the line number entered before pressing G
    g      - Go to the top of the document
    0      - Move to the beginning of the line
    $      - Move to the end of the line
    d      - Start delete operation (press 'd' again to delete the current line)
    y      - Start yank (copy) operation (press 'y' again to yank the current line)
    p      - Paste the last deleted or yanked text
    u      - Undo the last operation
    Ctrl+R - Redo the last undone operation
    h      - Move cursor left
    l      - Move cursor right
    k      - Move cursor up
    j      - Move cursor down
    Ctrl+S - Save the document
    Ctrl+Q - Quit the editor
"""

def main(stdscr):
    # Initialize curses
    # This block sets up the curses environment and initializes various settings for the terminal interface.
    screen = curses.initscr()  # Initialize the standard screen object
    screen.nodelay(1)           # Set getch() to non-blocking mode
    curses.noecho()             # Disable automatic echoing of keys
    curses.raw()                # Put terminal in raw mode to disable line buffering
    
    # Initialize variables
    mode = 'n'                  # Mode of the editor (n = normal, i = insert, etc.)
    buffer = []                 # Main text buffer, stores the content of the file
    yank_buffer = []            # Buffer to store text for yank (copy) and paste operations
    undo_buffer = []            # Buffer to store undo history
    filename = 'noname.txt'     # Default filename if no file is provided
    undo_index = -1             # Tracks the current position in the undo history
    search_string = ''          # Variable reserved for search functionality (not used in current code)
    result = []                 # Reserved for storing search results (not used in current code)
    search_index = 0            # Reserved for tracking search result navigation (not used in current code)
    rows, cols = screen.getmaxyx()  # Get the size of the terminal window
    rows -= 1                   # Adjust row count to leave space for the status bar
    view_x, view_y, cursor_row, cursor_col = [0] * 4  # Viewport and cursor position
    input_buffer = ''           # Buffer to store user input for commands like G (go to line)

    # Handle command-line arguments
    # If a filename is provided as an argument, the file is loaded into the buffer.
    # If '--help' is passed, the help text is displayed and the program exits.
    if len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            print(HELP_TEXT)
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

    # Save the initial state of the buffer for undo functionality
    undo_index += 1
    undo_buffer.insert(undo_index, [deepcopy(buffer), [cursor_row, cursor_col]])

    # Main event loop
    # This loop continuously handles user input and updates the screen accordingly.
    while True:
        # Update screen and viewport
        screen.move(0, 0)
        if cursor_row < view_y:
            view_y = cursor_row
        if cursor_row >= view_y + rows:
            view_y = cursor_row - rows + 1
        if cursor_col < view_x:
            view_x = cursor_col
        if cursor_col >= view_x + cols:
            view_x = cursor_col - cols + 1
        
        # Render text buffer on the screen
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
        
        # Display the status bar
        # The status bar shows the current mode, filename, line number, and cursor position.
        status = mode + ' "' + filename + '"' + ' line ' + str(cursor_row + 1)
        try:
            status += ' of ' + str(len(buffer)) + ' --' + str(int(((cursor_row + 1) * 100 / len(buffer)))) + '%--'
        except:
            pass
        status += ' col ' + str(cursor_col)
        screen.addstr(status)
        screen.clrtoeol()
        curses.curs_set(0)
        screen.move(cursor_row - view_y, cursor_col - view_x)
        curses.curs_set(1)
        screen.refresh()

        # Get user input
        # The editor waits for user input to process commands or text entry.
        key = -1
        while key == -1:
            key = screen.getch()

        # Handle terminal resize
        if key == curses.KEY_RESIZE:
            rows, cols = screen.getmaxyx()
            rows -= 1
            screen.refresh()
            view_y = 0

        # Process commands in normal mode
        if chr(key).isdigit() and chr(key) != '0' and mode not in 'irRoO':
            input_buffer += chr(key)
        elif mode == 'n':
            if key == ord('i'):
                mode = 'i'  # Enter insert mode
            elif key == ord('a'):
                cursor_col += 1
                mode = 'i'  # Enter insert mode after cursor
            elif key == ord('A'):
                cursor_col = len(buffer[cursor_row])
                mode = 'i'  # Enter insert mode at the end of the line
            elif key == ord('o'):
                buffer.insert(cursor_row + 1, [])
                cursor_row += 1
                mode = 'o'  # Open a new line below the current line
            elif key == ord('O'):
                buffer.insert(cursor_row, [])
                mode = 'O'  # Open a new line above the current line
            elif key == ord('r'):
                mode = 'r'  # Replace the character at the cursor
            elif key == ord('R'):
                mode = 'R'  # Enter replace mode
            elif key == ord('x') and len(buffer[cursor_row]):
                del buffer[cursor_row][cursor_col]  # Delete the character at the cursor
            elif key == ord('G'):
                cursor_row = int(input_buffer) - 1 if len(input_buffer) and int(input_buffer) - 1 < len(buffer) else len(buffer) - 1
            elif key == ord('g'):
                mode = 'g'  # Go to the top of the document
            elif key == ord('0'):
                if input_buffer == '':
                    cursor_col = 0  # Move to the beginning of the line
                else:
                    input_buffer += chr(key)
            elif key == ord('$'):
                if len(input_buffer):
                    cursor_row = cursor_row + int(input_buffer) - 1 if (cursor_row + int(input_buffer) - 1) < len(buffer) else cursor_row
                cursor_col = len(buffer[cursor_row]) - 1  # Move to the end of the line
            elif key == ord('d'):
                mode = 'd'  # Start delete operation
            elif key == ord('y'):
                mode = 'y'  # Start yank (copy) operation
            elif key == ord('p'):
                # Paste the last deleted or yanked text
                for line in yank_buffer:
                    if len(buffer) > 1:
                        cursor_row += 1
                    buffer.insert(cursor_row, deepcopy(line))
                undo_index += 1
                undo_buffer.insert(undo_index, [deepcopy(buffer), [cursor_row, cursor_col]])
            elif key == ord('u'):
                # Undo the last operation
                if undo_index >= 1:
                    undo_index -= 1
                    buffer = deepcopy(undo_buffer[undo_index][0])
                    cursor_row, cursor_col = undo_buffer[undo_index][1]
            elif key == (ord('r') & 0x1f):
                # Redo the last undone operation
                if undo_index < len(undo_buffer) - 1:
                    undo_index += 1
                    buffer = deepcopy(undo_buffer[undo_index][0])
                    cursor_row, cursor_col = undo_buffer[undo_index][1]
            elif key == ord('h'):
                cursor_col -= 1 if cursor_col else 0  # Move cursor left
            elif key == ord('l'):
                cursor_col += 1 if cursor_col < len(buffer[cursor_row]) - 1 else 0  # Move cursor right
            elif key == ord('k'):
                cursor_row -= 1 if cursor_row else 0  # Move cursor up
            elif key == ord('j'):
                cursor_row += 1 if cursor_row < len(buffer) - 1 else 0  # Move cursor down
            current_row = buffer[cursor_row] if cursor_row < len(buffer) else None
            len_current_row = len(current_row) if current_row is not None else 0
            if cursor_col > len_current_row - 1:
                cursor_col = len_current_row - 1 if len_current_row else len_current_row
            if key == ord('A'):
                cursor_col = len_current_row
            if key != ord('0') and mode not in 'dy':
                input_buffer = ''
        
        # Process commands in insert, open, and replace modes
        elif mode in 'ioO':
            if key == 27:
                mode = 'n'  # Exit to normal mode
                cursor_col -= 1 if cursor_col else 0
            elif key != ((key) & 0x1f) and key < 128:
                buffer[cursor_row].insert(cursor_col, key)  # Insert character
                cursor_col += 1
            elif key == ord('\n'):
                # Insert a newline
                line_content = buffer[cursor_row][cursor_col:]
                buffer[cursor_row] = buffer[cursor_row][:cursor_col]
                cursor_row += 1
                cursor_col = 0
                buffer.insert(cursor_row, [] + line_content)
            elif key == curses.KEY_BACKSPACE:
                if cursor_col:
                    cursor_col -= 1
                    del buffer[cursor_row][cursor_col]  # Delete character
                elif cursor_row:
                    line_content = buffer[cursor_row][cursor_col:]
                    del buffer[cursor_row]
                    cursor_row -= 1
                    cursor_col = len(buffer[cursor_row])
                    buffer[cursor_row] += line_content
        
        # Replace character at the cursor (single character replace mode)
        elif mode == 'r':
            try:
                buffer[cursor_row][cursor_col] = key
            except:
                pass
            mode = 'n'  # Exit to normal mode
        
        # Replace mode (continuous replace mode)
        elif mode == 'R':
            if key == 27:
                mode = 'n'  # Exit to normal mode
                cursor_col -= 1 if cursor_col else 0
            elif key != ((key) & 0x1f) and key < 128:
                buffer[cursor_row][cursor_col] = key  # Replace character
                cursor_col += 1
            elif key == curses.KEY_BACKSPACE:
                cursor_col -= 1 if cursor_col else 0
        
        # Go to the top of the document
        elif mode == 'g':
            cursor_row = 0
            cursor_col = 0
            mode = 'n'
        
        # Delete operation
        elif mode == 'd':
            if key == ord('d'):
                yank_buffer = []
                num_lines = int(input_buffer) if len(input_buffer) else 1
                for i in range(num_lines):
                    if len(buffer) == 1 and buffer[0] == []:
                        break
                    yank_buffer.append(buffer[cursor_row])  # Yank (copy) the line
                    if len(buffer) > 1:
                        del buffer[cursor_row]  # Delete the line
                    elif len(buffer) == 1:
                        buffer[cursor_row] = []
                    if cursor_row and cursor_row == len(buffer):
                        cursor_row -= 1
                        cursor_col = 0
            mode = 'n'
            input_buffer = ''
            screen.move(rows, 0)
        
        # Yank (copy) operation
        elif mode == 'y':
            if key == ord('y'):
                yank_buffer = []
                num_lines = int(input_buffer) if len(input_buffer) else 1
                for i in range(num_lines):
                    if cursor_row + i >= len(buffer):
                        break
                    yank_buffer.append(buffer[cursor_row + i])  # Yank (copy) the line(s)
            mode = 'n'
            input_buffer = ''
            screen.move(rows, 0)
        
        # Save the buffer state for undo functionality
        if (key != 27 and mode in 'irRdoOyd'):
            undo_index += 1
            undo_buffer.insert(undo_index, [deepcopy(buffer), [cursor_row, cursor_col]])
        
        # Quit the editor
        if key == (ord('q') & 0x1f):
            sys.exit()
        
        # Save the document
        if key == (ord('s') & 0x1f):
            content = ''
            for line in buffer:
                content += ''.join([chr(c) for c in line]) + '\n'
            with open(filename, 'w') as file:
                file.write(content)  # Write buffer content to file
            screen.move(rows, 0)
            screen.addstr('Saved')
            screen.clrtoeol()
            screen.refresh()
            time.sleep(1)

# Set ESCDELAY for better responsiveness of escape sequences
# This ensures that the delay in recognizing escape sequences is minimal.
os.environ.setdefault('ESCDELAY', '25')

# Run the curses wrapper
# The wrapper ensures that the terminal is properly initialized and cleaned up.
curses.wrapper(main)
