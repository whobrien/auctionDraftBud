import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QTabWidget, QTextEdit, QGroupBox, QCheckBox
from draft_logic import Draft, Owner, Player, load_players_from_csv

class DraftApp(QWidget):
    def __init__(self, draft):
        super().__init__()
        self.draft = draft  # Store the draft object
        self.initUI()

    def initUI(self):
        # Create the main layout
        layout = QVBoxLayout()

        # Create tab widget
        self.tabs = QTabWidget()
        self.draft_tab = QWidget()
        self.owners_tab = QWidget()
        self.my_team_tab = QWidget()

        # Add tabs to the widget
        self.tabs.addTab(self.draft_tab, "Draft")
        self.tabs.addTab(self.owners_tab, "Owners")
        self.tabs.addTab(self.my_team_tab, "My Team")

        # Initialize tabs
        self.initDraftTab()
        self.initOwnersTab()
        self.initMyTeamTab()

        # Add tabs to the layout
        layout.addWidget(self.tabs)

        # Set the layout for the main window
        self.setLayout(layout)
        self.setWindowTitle('Fantasy Football Draft')
        self.setGeometry(300, 300, 800, 600)

    def initDraftTab(self):
        layout = QVBoxLayout()

        # Draft Information
        self.round_label = QLabel(f"Round: {self.draft.round}, Pick: {self.draft.pick}, Total Budget Remaining: ${self.draft.total_remaining_budget()}")
        current_owner = self.draft.next_owner()
        self.nomination_info = QLabel(f"Nomination: {current_owner.name} - Nomination Number {current_owner.nomination_number}")
        layout.addWidget(self.round_label)
        layout.addWidget(self.nomination_info)

        # Position filter
        self.position_filter = QComboBox()
        self.position_filter.addItem("All Positions")
        positions = sorted(set(player.position for player in self.draft.players))
        self.position_filter.addItems(positions)
        self.position_filter.currentIndexChanged.connect(self.filter_players)
        layout.addWidget(self.position_filter)

        # # Position Filter
        # self.position_group_box = self.create_checkbox_group("Position", sorted(set(player.position for player in self.draft.players)))
        # layout.addWidget(self.position_group_box)

        # Tier filter
        self.tier_filter = QComboBox()
        self.tier_filter.addItem("All Tiers")
        tiers = sorted(set(int(player.tier) for player in self.draft.players))
        self.tier_filter.addItems(map(str, tiers)) # Convert back to strings for display
        self.tier_filter.currentIndexChanged.connect(self.filter_players)
        layout.addWidget(self.tier_filter)

        # Target/Avoid/Dart-Throw filter
        self.tad_filter = QComboBox()
        self.tad_filter.addItem("All TADs")
        tads = sorted(set(str(player.tad) for player in self.draft.players))
        self.tad_filter.addItems(tads)
        self.tad_filter.currentIndexChanged.connect(self.filter_players)
        layout.addWidget(self.tad_filter)

        # # Player dropdown
        # self.player_dropdown = QLineEdit()  # Replaced dropdown with a line edit for manual entry
        # layout.addWidget(self.player_dropdown)

        # Player dropdown
        self.player_dropdown = QComboBox()
        self.update_player_dropdown()
        layout.addWidget(self.player_dropdown)

        # Manual player entry
        self.manual_player_entry = QLineEdit()
        self.manual_player_entry.setPlaceholderText("Enter player name if not in dropdown")
        layout.addWidget(self.manual_player_entry)

        # Manual player position entry
        self.manual_player_entry = QLineEdit()
        self.manual_player_entry.setPlaceholderText("Enter player position")
        layout.addWidget(self.manual_player_entry)

        # Player nomination dropdown
        #self.player_dropdown = QComboBox()
        #for player in self.draft.players:
        #    self.player_dropdown.addItem(player.name)
        #layout.addWidget(self.player_dropdown)

        # Button to nominate player
        self.nominate_button = QPushButton("Nominate Player")
        self.nominate_button.clicked.connect(self.nominatePlayer)
        layout.addWidget(self.nominate_button)

        # Buying Owner and Price
        self.buyer_dropdown = QComboBox()
        for owner in self.draft.owners:
            self.buyer_dropdown.addItem(owner.name)
        layout.addWidget(self.buyer_dropdown)

        self.price_input = QLineEdit("1")
        self.price_input.setPlaceholderText("Enter Price")
        layout.addWidget(self.price_input)

        # Button to finalize the purchase
        self.draft_button = QPushButton("Draft Player")
        self.draft_button.clicked.connect(self.draftPlayer)
        layout.addWidget(self.draft_button)
        
        # Back button to go back one pick
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.goBackOnePick)
        layout.addWidget(self.back_button)

        self.draft_tab.setLayout(layout)

    def create_checkbox_group(self, title, options):
        group_box = QGroupBox(title)
        layout = QVBoxLayout()
        self.checkboxes = {}
        for option in options:
            checkbox = QCheckBox(option)
            layout.addWidget(checkbox)
            self.checkboxes[option] = checkbox
        group_box.setLayout(layout)
        return group_box

    def update_player_dropdown(self):
        # Clear current dropdown items
        self.player_dropdown.clear()

        # Get selected position, tier and, Tad filters
        selected_position = self.position_filter.currentText()
        #selected_positions = [pos for pos, checkbox in self.position_checkboxes.items() if checkbox.isChecked()]
        selected_tier = self.tier_filter.currentText()
        selected_tad = self.tad_filter.currentText()

        # Filter players based on selected position, tier, tad
        filtered_players = [
            player.name for player in self.draft.players
            if (selected_position == "All Positions" or player.position == selected_position) and 
                (selected_tier == "All Tiers" or str(player.tier) == selected_tier) and
                    (selected_tad == "All TADs" or str(player.tad) == selected_tad)
        ]

        # Sort the filtered players alphabetically
        #filtered_players.sort()

        # Add filtered players to the dropdown
        self.player_dropdown.clear()
        self.player_dropdown.addItems(filtered_players)

    def filter_players(self):
        # Update the player dropdown based on the selected filters
        self.update_player_dropdown()

    def goBackOnePick(self):
        # Check if we're at the first pick
        if self.draft.pick <= 1:
            print("Cannot go back, this is the first pick.")
            return

        # Reduce the pick number
        self.draft.pick -= 1

        # Recalculate the round
        self.draft.calculate_round()

        # Load the last pick's details from the CSV file
        with open(self.draft.draft_file, mode='r') as file:
            lines = file.readlines()

        # Remove the last line (the most recent draft) from the CSV
        if len(lines) > 1:
            with open(self.draft.draft_file, mode='w', newline='') as file:
                file.writelines(lines[:-1])

            # Get the last drafted player's name
            last_pick_data = lines[-1].strip().split(',')
            last_player_name = last_pick_data[0]
            last_owner_name = last_pick_data[5]
            last_price = int(last_pick_data[6])
            last_nominating_owner_name = last_pick_data[4]
            #print(f"Last Nominating Owner: {last_nominating_owner_name}")

            # Reverse the draft: Remove player from the owner and refund the budget
            last_owner = self.draft.get_owner_by_name(last_owner_name)
            last_player = self.draft.get_player_by_name(last_player_name)

            last_owner.players.remove(last_player)
            last_owner.budget += last_price

            # Reset player attributes
            last_player.buying_owner = None
            last_player.nominating_owner = None # Clear the nominating owner
            last_player.price = 0

            # Add the player back to the nomination dropdown
            self.player_dropdown.addItem(last_player_name)

            # Add the owner back to the buyer dropdown if necessary
            if last_owner not in [self.buyer_dropdown.itemText(i) for i in range(self.buyer_dropdown.count())]:
                self.buyer_dropdown.addItem(last_owner.name)

            print(f"Reversed pick for player: {last_player_name}, owner: {last_owner_name}, price: ${last_price}")

            # Adjust the Current Owner Index
            self.draft.current_owner_index -= 1
            if self.draft.current_owner_index < 0:
                self.draft.current_owner_index = len(self.draft.owners) - 1 # Wrap around to the last owner

            # Update the nomination info in the GUI
            #pervious_owner = self.draft.get_owner_by_name(last_nominating_owner_name)
            #self.nomination_info.setText(f"Nomination: {pervious_owner.name} - Nomination Number {pervious_owner.nomination_number}")

        # Update the round, pick, and total remaining budget information
        total_budget = self.draft.total_remaining_budget()
        self.round_label.setText(f"Round: {self.draft.round}, Pick: {self.draft.pick}, Total Budget Remaining: ${total_budget}")

        # Update the nomination information
        next_owner = self.draft.next_owner()
        self.nomination_info.setText(f"Nomination: {next_owner.name} - Nomination Number {next_owner.nomination_number}")

        # Update the owners and team tabs
        self.updateOwnersTab()
        self.updateMyTeamTab()

    def initOwnersTab(self):
        layout = QVBoxLayout()

        # Placeholder for owners and their players
        self.owners_display = QTextEdit()
        self.owners_display.setReadOnly(True)
        layout.addWidget(self.owners_display)

        self.updateOwnersTab()

        self.owners_tab.setLayout(layout)

    def initMyTeamTab(self):
        layout = QVBoxLayout()

        # Placeholder for My Team and players
        self.my_team_display = QTextEdit()
        self.my_team_display.setReadOnly(True)
        layout.addWidget(self.my_team_display)

        self.updateMyTeamTab()

        self.my_team_tab.setLayout(layout)

    def nominatePlayer(self):
        # Logic to nominate a player
        player_name = self.player_dropdown.currentText()
        if player_name == "Select Player":
            return
        
        # Get the player name from the dropdown or manual entry
        player_name = self.player_dropdown.currentText()
        manual_name = self.manual_player_entry.text().strip()
        manual_position = self.manual_player_entry.text().strip()

        if manual_name:
            player_name = manual_name  # Use the manually entered name

            # Add the new player to the draft
            new_player = Player(name=manual_name, position=manual_position, team="Unknown", tier=0, tad="")
            self.draft.players.append(new_player)
            
            # Also add to the dropdown for future use
            self.player_dropdown.addItem(manual_name)
        
        if not player_name or player_name == "Select Player":
            print("No player selected")
            return

        # Update the nomination info
        current_owner = self.draft.next_owner()

        # Update the player's nominating owner using the Draft class's nominate_player method
        nominated_player = self.draft.nominate_player(current_owner.name, player_name)

        self.nomination_info.setText(f"{current_owner.name} has nominated {player_name}.")

        # Print debug information to ensure that the nominating owner is set correctly
        print(f"Player {nominated_player.name} nominated by {nominated_player.nominating_owner}")

    def draftPlayer(self):
        # Logic to draft a player
        player_name = self.player_dropdown.currentText()
        manual_name = self.manual_player_entry.text().strip()
        manual_position = self.manual_player_entry.text().strip()
        owner_name = self.buyer_dropdown.currentText()
        price = self.price_input.text()

        # Print statements for debugging
        #print(f"Drafting player: {player_name}")
        #print(f"Buyer owner: {owner_name}")
        #print(f"Price: {price}")

        # Check for valid inputs
        if not player_name or player_name == "Select Player":
            print("No player selected")
            return

        if manual_name:
            player_name = manual_name # Use the manually entered name

        if not owner_name or owner_name == "Select Owner":
            print("No owner selected")
            return

        if not price or not price.isdigit():
            print("Invalid price entered")
            return
        
        # Get the player object
        player = self.draft.get_player_by_name(player_name)

        # Convert price to an integer
        price = int(price)

        # Handle the case where the player was manually entered
        if manual_name:
            # find or creat the player in the draft
            player = next((p for p in self.draft.players if p.name == player_name), None)
            if not player:
                player = Player(name=player_name, position=manual_position, team="Unknown", tier=0, tad="")
                self.draft.players.append(player)
        else:
            #get the player object from the dropdown menu
            player = self.draft.get_player_by_name(player_name)
            # Remove the drafted player from the dropdown menu if they were in it
            index = self.player_dropdown.findText(player_name)
            if index != -1:
                self.player_dropdown.removeItem(index)

        # Check if the player has a nominating owner
        if not player.nominating_owner:
            print(f"Player {player_name} cannot be drafted because they have no nominating owner.")
            return

        # Draft the player using the Draft class
        try:
            self.draft.draft_player(player_name, owner_name, price)
        except AttributeError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error drafting player: {e}")
            return

        # Check if the owner has reached 16 players
        owner = self.draft.get_owner_by_name(owner_name)
        print(f"Owner {owner.name} has {len(owner.players)} players.")
        if len(owner.players) >= 16:
            # Remove the owner from the buyer dropdown
            owner_index = self.buyer_dropdown.findText(owner_name)
            if owner_index != -1:
                self.buyer_dropdown.removeItem(owner_index)
            print(f"Owner {owner_name} has reached 16 players and has been removed from the dropdown.")

        # Update the round, pick, and total remaining budget information
        total_budget = self.draft.total_remaining_budget()
        self.round_label.setText(f"Round: {self.draft.round}, Pick: {self.draft.pick}, Total Budget Remaining: ${total_budget}")

        # Update the round and nomination information
        self.round_label.setText(f"Round: {self.draft.round}, Pick: {self.draft.pick}, Remaining Budget: ${total_budget}")
        next_owner = self.draft.next_owner()
        self.nomination_info.setText(f"Nomination: {next_owner.name} - Nomination Number {next_owner.nomination_number}")

        # Update GUI after drafting the player
        self.updateOwnersTab()
        self.updateMyTeamTab()

        # Clear the price and name input for the next entry
        self.price_input.setText("1")
        self.manual_player_entry.clear()

    def updateOwnersTab(self):
        # Update the owners tab with current information
        owners_text = "Owners and their players:\n"
        for owner in self.draft.owners:
            owners_text += owner.display() + "\n"
        self.owners_display.setText(owners_text)

    def updateMyTeamTab(self):
        # Update My Team tab with current information
        my_team = next(owner for owner in self.draft.owners if owner.is_my_team)
        my_team_text = my_team.display()
        self.my_team_display.setText(my_team_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Load the draft data (this assumes you've set up the owners and players)
    owners = [
        Owner("My Team", 1, is_my_team=True),
        Owner("Owner 2", 2),
        Owner("Owner 3", 3),
        Owner("Owner 4", 4),
        Owner("Owner 5", 5),
        Owner("Owner 6", 6),
        Owner("Owner 7", 7),
        Owner("Owner 8", 8),
        Owner("Owner 9", 9),
        Owner("Owner 10", 10),
        Owner("Owner 11", 11),
        Owner("Owner 12", 12)
    ]  # Add more owners as needed

    current_dir = os.path.dirname(os.path.abspath(__file__))
    players_file = os.path.join(current_dir, 'resources', 'players.csv')

    # Load players from CSV
    players = load_players_from_csv(players_file)

    draft = Draft(owners, players)
    window = DraftApp(draft)
    window.show()
    sys.exit(app.exec_())