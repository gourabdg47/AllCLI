from modules.menu import main_menu
from modules.folder_init import initialize_folders, setup_logging

if __name__ == "__main__":
    initialize_folders()
    setup_logging()
    while True:
        main_menu()
