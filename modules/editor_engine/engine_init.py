import sys
import os
import time
from copy import deepcopy
from rich import print as r_print
from rich.panel import Panel


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



class TerminalTextEditor:
    def __init__(self, filepath=None):
        self.filepath = filepath if filepath else 'noname.txt'
        self.mode = 'normal'
        self.buffer = []
        self.yank_buffer = []
        self.undo_buffer = []
        self.undo_index = -1
        self.rows = 0
        self.cols = 0
        self.view_x, self.view_y, self.cursor_row, self.cursor_col = [0] * 4
        self.input_buffer = ''

        if self.filepath:
            try:
                with open(self.filepath) as file:
                    content = file.read().split('\n')
                    content = content[:-1] if len(content) > 1 else content
                    for line in content:
                        self.buffer.append([ord(c) for c in line])
            except:
                self.buffer.append([])
        else:
            self.buffer.append([])

        self.undo_index += 1
        self.undo_buffer.insert(self.undo_index, [deepcopy(self.buffer), [self.cursor_row, self.cursor_col]])

    def run(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        screen = curses.initscr()
        screen.nodelay(1)
        curses.noecho()
        curses.raw()

        self.rows, self.cols = screen.getmaxyx()
        self.rows -= 1

        while True:
            screen.move(0, 0)
            if self.cursor_row < self.view_y:
                self.view_y = self.cursor_row
            if self.cursor_row >= self.view_y + self.rows:
                self.view_y = self.cursor_row - self.rows + 1
            if self.cursor_col < self.view_x:
                self.view_x = self.cursor_col
            if self.cursor_col >= self.view_x + self.cols:
                self.view_x = self.cursor_col - self.cols + 1
            
            for row in range(self.rows):
                buffer_row = row + self.view_y
                for col in range(self.cols):
                    buffer_col = col + self.view_x
                    try:
                        screen.addch(row, col, self.buffer[buffer_row][buffer_col])
                    except:
                        pass 
                screen.clrtoeol()
                try:
                    screen.addstr('\n') if buffer_row < len(self.buffer) else screen.addstr('~\n')
                except:
                    pass
            
            status = f"Mode: {self.mode} | File: '{self.filepath}' | Line: {self.cursor_row + 1}/{len(self.buffer)} ({int((self.cursor_row + 1) * 100 / len(self.buffer))}%) | Col: {self.cursor_col}"
            screen.addstr(status)
            screen.clrtoeol()
            curses.curs_set(0)
            screen.move(self.cursor_row - self.view_y, self.cursor_col - self.view_x)
            curses.curs_set(1)
            screen.refresh()

            key = -1
            while key == -1:
                key = screen.getch()

            if key == curses.KEY_RESIZE:
                self.rows, self.cols = screen.getmaxyx()
                self.rows -= 1
                screen.refresh()
                self.view_y = 0

            if chr(key).isdigit() and chr(key) != '0' and self.mode not in ['insert', 'replace', 'open']:
                self.input_buffer += chr(key)

            elif self.mode == 'normal':
                if key == ord('i'):
                    self.mode = 'insert'
                elif key == ord('a'):
                    self.cursor_col += 1
                    self.mode = 'insert'
                elif key == ord('A'):
                    self.cursor_col = len(self.buffer[self.cursor_row])
                    self.mode = 'insert'
                elif key == ord('o'):
                    self.buffer.insert(self.cursor_row + 1, [])
                    self.cursor_row += 1
                    self.mode = 'open'
                elif key == ord('O'):
                    self.buffer.insert(self.cursor_row, [])
                    self.mode = 'open'
                elif key == ord('r'):
                    self.mode = 'replace_char'
                elif key == ord('R'):
                    self.mode = 'replace'
                elif key == ord('x') and len(self.buffer[self.cursor_row]):
                    del self.buffer[self.cursor_row][self.cursor_col]
                elif key == ord('G'):
                    self.cursor_row = int(self.input_buffer) - 1 if len(self.input_buffer) and int(self.input_buffer) - 1 < len(self.buffer) else len(self.buffer) - 1
                elif key == ord('g'):
                    self.cursor_row = 0
                    self.cursor_col = 0
                elif key == ord('0'):
                    if self.input_buffer == '':
                        self.cursor_col = 0
                    else:
                        self.input_buffer += chr(key)
                elif key == ord('$'):
                    if len(self.input_buffer):
                        self.cursor_row = self.cursor_row + int(self.input_buffer) - 1 if (self.cursor_row + int(self.input_buffer) - 1) < len(self.buffer) else self.cursor_row
                    self.cursor_col = len(self.buffer[self.cursor_row]) - 1
                elif key == ord('d'):
                    self.mode = 'delete'
                elif key == ord('y'):
                    self.mode = 'yank'
                elif key == ord('p'):
                    for line in self.yank_buffer:
                        if len(self.buffer) > 1:
                            self.cursor_row += 1
                        self.buffer.insert(self.cursor_row, deepcopy(line))
                    self.undo_index += 1
                    self.undo_buffer.insert(self.undo_index, [deepcopy(self.buffer), [self.cursor_row, self.cursor_col]])
                elif key == ord('u'):
                    if self.undo_index >= 1:
                        self.undo_index -= 1
                        self.buffer = deepcopy(self.undo_buffer[self.undo_index][0])
                        self.cursor_row, self.cursor_col = self.undo_buffer[self.undo_index][1]
                elif key == (ord('r') & 0x1f):
                    if self.undo_index < len(self.undo_buffer) - 1:
                        self.undo_index += 1
                        self.buffer = deepcopy(self.undo_buffer[self.undo_index][0])
                        self.cursor_row, self.cursor_col = self.undo_buffer[self.undo_index][1]
                elif key == ord('h'):
                    self.cursor_col -= 1 if self.cursor_col else 0
                elif key == ord('l'):
                    self.cursor_col += 1 if self.cursor_col < len(self.buffer[self.cursor_row]) - 1 else 0
                elif key == ord('k'):
                    self.cursor_row -= 1 if self.cursor_row else 0
                elif key == ord('j'):
                    self.cursor_row += 1 if self.cursor_row < len(self.buffer) - 1 else 0
                current_row = self.buffer[self.cursor_row] if self.cursor_row < len(self.buffer) else None
                len_current_row = len(current_row) if current_row is not None else 0
                if self.cursor_col > len_current_row - 1:
                    self.cursor_col = len_current_row - 1 if len_current_row else len_current_row
                if key == ord('A'):
                    self.cursor_col = len_current_row
                if key != ord('0') and self.mode not in ['delete', 'yank']:
                    self.input_buffer = ''
            
            elif self.mode in ['insert', 'open']:
                if key == 27:  # ESC key
                    self.mode = 'normal'
                    self.cursor_col -= 1 if self.cursor_col else 0

                elif key in [curses.KEY_ENTER, 10, 13]:  # Handle the 'Enter' key
                    line_content = self.buffer[self.cursor_row][self.cursor_col:]
                    self.buffer[self.cursor_row] = self.buffer[self.cursor_row][:self.cursor_col]
                    self.cursor_row += 1
                    self.cursor_col = 0
                    self.buffer.insert(self.cursor_row, [] + line_content)

                elif key in [curses.KEY_BACKSPACE, 8]:  # Handle the 'Backspace' key
                    if self.cursor_col > 0:  # If not at the beginning of the line
                        self.cursor_col -= 1
                        del self.buffer[self.cursor_row][self.cursor_col]
                    elif self.cursor_row > 0:  # If at the beginning of the line, join with the previous line
                        # Save the remaining content of the current line
                        line_content = self.buffer[self.cursor_row]
                        # Delete the current line
                        del self.buffer[self.cursor_row]
                        # Move to the end of the previous line
                        self.cursor_row -= 1
                        self.cursor_col = len(self.buffer[self.cursor_row])
                        # Append the saved content to the previous line
                        self.buffer[self.cursor_row].extend(line_content)


                elif key == curses.KEY_DC:  # Handle the 'Delete' key
                    if self.cursor_col < len(self.buffer[self.cursor_row]):
                        del self.buffer[self.cursor_row][self.cursor_col]
                    elif self.cursor_row < len(self.buffer) - 1:
                        line_content = self.buffer[self.cursor_row + 1]
                        del self.buffer[self.cursor_row + 1]
                        self.buffer[self.cursor_row] += line_content

                elif key != ((key) & 0x1f) and key < 128:
                    self.buffer[self.cursor_row].insert(self.cursor_col, key)
                    self.cursor_col += 1


            elif self.mode == 'replace_char':
                try:
                    self.buffer[self.cursor_row][self.cursor_col] = key
                except:
                    pass
                self.mode = 'normal'

            elif self.mode == 'replace':
                if key == 27:  # ESC key
                    self.mode = 'normal'
                    self.cursor_col -= 1 if self.cursor_col else 0
                elif key != ((key) & 0x1f) and key < 128:
                    self.buffer[self.cursor_row][self.cursor_col] = key
                    self.cursor_col += 1
                elif key == curses.KEY_BACKSPACE:
                    self.cursor_col -= 1 if self.cursor_col else 0

            elif self.mode == 'delete':
                if key == ord('d'):
                    self.yank_buffer = []
                    num_lines = int(self.input_buffer) if len(self.input_buffer) else 1
                    for i in range(num_lines):
                        if len(self.buffer) == 1 and self.buffer[0] == []:
                            break
                        self.yank_buffer.append(self.buffer[self.cursor_row])
                        if len(self.buffer) > 1:
                            del self.buffer[self.cursor_row]
                        elif len(self.buffer) == 1:
                            self.buffer[self.cursor_row] = []
                        if self.cursor_row and self.cursor_row == len(self.buffer):
                            self.cursor_row -= 1
                            self.cursor_col = 0
                            
                self.mode = 'normal'
                self.input_buffer = ''
                screen.move(self.rows, 0)

            elif self.mode == 'yank':
                if key == ord('y'):
                    self.yank_buffer = []
                    num_lines = int(self.input_buffer) if len(self.input_buffer) else 1
                    for i in range(num_lines):
                        if self.cursor_row + i >= len(self.buffer):
                            break
                        self.yank_buffer.append(self.buffer[self.cursor_row + i])
                self.mode = 'normal'
                self.input_buffer = ''
                screen.move(self.rows, 0)

            if key != 27 and self.mode in ['insert', 'replace', 'open', 'delete', 'yank']:
                self.undo_index += 1
                self.undo_buffer.insert(self.undo_index, [deepcopy(self.buffer), [self.cursor_row, self.cursor_col]])

            if key == (ord('q') & 0x1f) or key == (ord('c') & 0x1f):  # Ctrl+Q
                # from ..custom_modules.journals import journal
                # journal()
                break

            if key == (ord('s') & 0x1f):  # Ctrl+S
                self.save_file()
                screen.move(self.rows, 0)
                screen.addstr('Saved')
                screen.clrtoeol()
                screen.refresh()
                time.sleep(1)

    def save_file(self):
        content = ''
        for line in self.buffer:
            content += ''.join([chr(c) for c in line]) + '\n'
        with open(self.filepath, 'w') as file:
            file.write(content)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Simple terminal-based text editor")
    parser.add_argument('filepath', nargs='?', help="File to edit", default=None)
    args = parser.parse_args()

    editor = TerminalTextEditor(filepath=args.filepath)
    editor.run()