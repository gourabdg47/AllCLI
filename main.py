from modules.menu import main_menu
from modules.folder_init import initialize_folders, setup_logging

''' TODO: Features to add: 
* Notes takings, tagging journals and notes, Time Tracking
* Budget and Expense Tracking (Personal Finance Tracker, Business Expense Management)
* File and Document Management (Document Storage, Search and Tagging)
* Notifications and Reminder (Task Reminders, Daily Summary)
* Goal Setting and Tracking (Goal Management, Milestone Tracking) [show progress bar in home, etc]
* Health and Wellness (Exercise Log, Meditation Timer, etc)
* Integration with External Services 
    - API Integration: Allow users to integrate with other tools or services they use regularly 
    (e.g., Slack for work communication, Trello for project management).
    - Email Integration: Enable users to link their email accounts to manage work or personal 
    emails directly from the app.
* Data Backup and Sync (Cloud Sync, Backup Options)
* ssh & ftp support


* Customizable Dashboard
* Theme Options (UI Customization)
* User Support and Documentation (Help and Tutorials, Feedback and Support)
* Security Features
* Collaboration Tools (Shared Tasks and Projects, Communication Tools)

'''

if __name__ == "__main__":
    initialize_folders()
    setup_logging()
    while True:
        main_menu()
