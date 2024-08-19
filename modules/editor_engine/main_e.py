#!/bin/python3

from modules.editor_engine.engine_init import TerminalTextEditor

def e_main(filepath):
    editor = TerminalTextEditor(filepath=filepath)
    editor.run()
    

    