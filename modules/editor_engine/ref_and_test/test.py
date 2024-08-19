import curses

def editor_engine(stdscr):
    pass

def create_title_borders(stdscr, title = 'Sample'):
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
    title = title
    stdscr.addstr(start_y - 2, start_x + (win_width - len(title)) // 2, title, curses.A_BOLD)

    # Create the larger box
    big_box_height = win_height - 6
    big_box_width = win_width - 6
    big_box_start_y = start_y
    big_box_start_x = start_x
    big_box = curses.newwin(big_box_height, big_box_width, big_box_start_y, big_box_start_x)

    # Add content and border to the larger box
    big_box.addstr(1, 2, "This is the larger box", curses.A_BOLD)
    big_box.box()

    # Create the smaller box inside the larger box
    small_box_height = big_box_height // 2
    small_box_width = big_box_width // 2
    small_box_start_y = big_box_start_y + 3  # Adjust this to position the smaller box inside the larger one
    small_box_start_x = big_box_start_x + 3  # Adjust this to position the smaller box inside the larger one
    small_box = curses.newwin(small_box_height, small_box_width, small_box_start_y, small_box_start_x)

    # Add content and border to the smaller box
    small_box.addstr(1, 2, "This is the smaller box", curses.A_BOLD)
    small_box.box()

    # Refresh all windows
    stdscr.refresh()
    big_box.refresh()
    small_box.refresh()

    # Wait for user input before exiting
    stdscr.getch()

def main(stdscr):
    # Clear screen
    stdscr.clear()
    create_title_borders(stdscr)

   

# Initialize curses and call the main function
curses.wrapper(main)
