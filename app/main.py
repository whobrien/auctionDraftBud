import sys
import os
from PyQt5.QtWidgets import QApplication
from draft_logic import Draft, Owner, load_players_from_csv
from gui import DraftApp

def main():
    # Set up owners
    owners = [
        Owner("Seth", 1),
        Owner("Lance", 2),
        Owner("fpd", 3),
        Owner("BK", 4),
        Owner("Nathan", 5),
        Owner("Jimmy", 6),
        Owner("Will", 7, is_my_team=True),
        Owner("Kreg", 8),
        Owner("JohnE", 9),
        Owner("Dodds", 10),
        Owner("Etler", 11),
        Owner("Joe", 12)
    ]  # Add more owners as needed

    # Get the path to the players.csv file in the resources folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    players_file = os.path.join(current_dir, 'resources', 'players.csv')

    # Load players from CSV
    players = load_players_from_csv(players_file)

    # Initialize the Draft
    draft = Draft(owners, players)

    # Start the GUI application
    app = QApplication(sys.argv)
    window = DraftApp(draft)  # Pass the draft object to the GUI
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()