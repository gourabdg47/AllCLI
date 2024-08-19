import curses

def editor_engine(stdscr, edit_win):
    # Initial position for the cursor in the editing window
    cursor_y, cursor_x = 1, 1
    edit_win.move(cursor_y, cursor_x)

    while True:
        key = edit_win.getch()

        if key == curses.KEY_UP:
            cursor_y = max(1, cursor_y - 1)
        elif key == curses.KEY_DOWN:
            cursor_y = min(edit_win.getmaxyx()[0] - 2, cursor_y + 1)
        elif key == curses.KEY_LEFT:
            cursor_x = max(1, cursor_x - 1)
        elif key == curses.KEY_RIGHT:
            cursor_x = min(edit_win.getmaxyx()[1] - 2, cursor_x + 1)
        elif key in (curses.KEY_BACKSPACE, 127):
            if cursor_x > 1:
                cursor_x -= 1
                edit_win.delch(cursor_y, cursor_x)
        elif key == 10:  # Enter key
            cursor_y = min(edit_win.getmaxyx()[0] - 2, cursor_y + 1)
            cursor_x = 1
        elif key == 27:  # Escape key to exit
            break
        else:
            edit_win.addch(cursor_y, cursor_x, key)
            cursor_x += 1

        edit_win.move(cursor_y, cursor_x)
        edit_win.refresh()

def create_title_borders(stdscr, title='Sample'):
    # Get the terminal height and width
    height, width = stdscr.getmaxyx()

    # Define padding (reduce height and width by these amounts)
    padding_y = 6
    padding_x = 10

    # Calculate window size based on screen size with padding
    win_height = height - padding_y
    win_width = width - padding_x

    # Define the position of the window (y, x) relative to the terminal
    start_y = (height - win_height) // 2
    start_x = (width - win_width) // 2

    # Add title above the window, centered
    stdscr.addstr(start_y - 3, start_x + (win_width - len(title)) // 2, title, curses.A_BOLD)

    # Create the larger box
    big_box_height = win_height - 2
    big_box_width = win_width - 2
    big_box_start_y = start_y
    big_box_start_x = start_x
    big_box = curses.newwin(big_box_height, big_box_width, big_box_start_y, big_box_start_x)
    big_box.box()

    # Add instructions to the larger box
    instructions = [
        "Instructions:",
        "Use arrow keys to move the cursor",
        "Type to edit text",
        "Press Backspace to delete",
        "Press Enter for new line",
        "Press ESC to exit"
    ]
    for i, line in enumerate(instructions, start=1):
        big_box.addstr(i, 2, line)

    # Create the smaller (editable) box inside the larger box
    small_box_height = big_box_height - len(instructions) - 4
    small_box_width = big_box_width - 4
    small_box_start_y = big_box_start_y + len(instructions) + 2  # Position below instructions
    small_box_start_x = big_box_start_x + 2
    small_box = curses.newwin(small_box_height, small_box_width, small_box_start_y, small_box_start_x)
    small_box.box()

    # Refresh all windows
    stdscr.refresh()
    big_box.refresh()
    small_box.refresh()

    # Enter the text editor engine for the inner box
    editor_engine(stdscr, small_box)

def main(stdscr):
    # Clear screen
    stdscr.clear()
    create_title_borders(stdscr)

# Initialize curses and call the main function
curses.wrapper(main)
