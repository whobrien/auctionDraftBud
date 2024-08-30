import os
import csv

class Owner:
    def __init__(self, name, nomination_number, is_my_team=False):
        self.name = name
        self.nomination_number = nomination_number
        self.budget = 200
        self.players = []
        self.is_my_team = is_my_team  # Flag to identify "My Team"

    @property
    def max_bid(self):
        return self.budget - (16 - len(self.players) - 1)

    def buy_player(self, player, position, team, price):
        if len(self.players) >= 16:
            raise ValueError(f"{self.name} already has 16 players.")
        if price > self.max_bid:
            raise ValueError(f"{self.name} cannot afford this player with a bid of ${price}. Max bid: ${self.max_bid}")
        self.players.append(player)
        self.budget -= price  # Subtract the price from the owner's budget
        player.buying_owner = self.name
        player.position = position
        player.team = team
        player.price = price

    def __str__(self):
        return f"Owner: {self.name}, Budget: ${self.budget}, Max Bid: ${self.max_bid}, Players: {[player.name for player in self.players]}, {[player.position for player in self.players]}, {[player.team for player in self.players]}"

    def display(self):
        if self.is_my_team:
            return f"*** MY TEAM ***\n{self.__str__()}\n"
        else:
            return self.__str__()

class Player:
    def __init__(self, name, position, team, tier, tad):
        self.name = name
        self.position = position
        self.team = team
        self.tier = tier
        self.tad = tad
        self.nominating_owner = None
        self.buying_owner = None
        self.price = 0

    def __str__(self):
        return f"Player: {self.name}, Position: {self.position}, Team: {self.team}, Tier: {self.tier}, Tad: {self.tad}, Nominating Owner: {self.nominating_owner}, Buying Owner: {self.buying_owner}, Price: ${self.price}"

class Draft:
    def __init__(self, owners, players, draft_file='draft_results.csv'):
        self.owners = owners
        self.players = players
        self.current_owner_index = 0
        self.round = 1
        self.pick = 1
        self.draft_file = draft_file

        # Initialize the CSV file with headers
        with open(self.draft_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Position", "Team", "Pick", "Nominating Owner", "Buying Owner", "Price"])

    def next_owner(self):
        while len(self.owners[self.current_owner_index].players) >= 16:
            self.current_owner_index = (self.current_owner_index + 1) % len(self.owners)
        return self.owners[self.current_owner_index]

    def nominate_player(self, owner_name, player_name):
        owner = self.get_owner_by_name(owner_name)
        player = self.get_player_by_name(player_name)
        player.nominating_owner = owner.name
        # Print statements for debugging
        #print(player.nominating_owner)
        return player

    def draft_player(self, player_name, owner_name, price):

        # Print statements for debugging
        #print(f"draft_player called with: player_name={player_name}, owner_name={owner_name}, price={price}")

        owner = self.get_owner_by_name(owner_name)
        player = self.get_player_by_name(player_name)
        if owner.is_my_team:
            # Special handling or logging for "My Team"
            print(f"{owner.name} (My Team) is drafting {player.name} for ${price}")
        owner.buy_player(player, player.position, player.team, price) #Deduct the player's price from the owner's budget
        print(f"{owner.name} has drafted {player.name} for ${price}. Budget remaining: ${owner.budget}. Max bid: ${owner.max_bid}")

        # Calculate the current round based on the pick
        self.calculate_round()

        # Update the pick number after drafting a player
        player.pick = self.pick
        self.pick += 1

        # Write the draft result to the CSV file
        self.update_draft_file(player)
        
        # Move to the next owner for nomination
        self.current_owner_index = (self.current_owner_index + 1) % len(self.owners)
    
    def calculate_round(self):

        #Calculate the current round based on the current pick and number of owners.
        #print(f"Current pick: {self.pick}")
        #print(f"Number of owners: {len(self.owners)}")
        self.round = self.pick // len(self.owners) + 1
    
    def total_remaining_budget(self):
        return sum(owner.budget for owner in self.owners)

    def update_draft_file(self, player):
        with open(self.draft_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player.name, player.position, player.team, self.pick - 1, player.nominating_owner, player.buying_owner, player.price])

    def get_owner_by_name(self, name):
        for owner in self.owners:
            if owner.name == name:
                return owner
        raise ValueError(f"Owner {name} not found.")

    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player
        raise ValueError(f"Player {name} not found.")

    def run_draft(self):
        while self.round <= 16:
            for owner in sorted(self.owners, key=lambda o: o.nomination_number):
                if len(owner.players) < 16:
                    print(f"{owner.name}, it's your turn to nominate a player.")
                    # Here you would handle the actual nomination and bidding process
            self.round += 1

def load_players_from_csv(filename):
    players = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            players.append(Player(row['Name'], row['Position'], row['Team'], row['Tier'], row['TAD']))
    return players

# Example usage
if __name__ == "__main__":
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

    draft = Draft(owners, players)
    draft.run_draft()