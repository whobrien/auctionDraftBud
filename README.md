# Fantasy Football Auction Draft App

## Overview

The Fantasy Football Auction Draft App is a Python-based application designed to streamline and manage the process of a fantasy football auction draft. The app provides an intuitive graphical user interface (GUI) that allows users to nominate players, track bids, and manage their fantasy football teams throughout the draft.

## Key Features

- **Intuitive GUI**: The application uses PyQt5 to provide a clean and interactive interface, allowing users to navigate through different tabs to manage the draft process.

- **Draft Management**:
  - **Player Nomination**: Users can nominate players from a dropdown list, setting them up for bidding.
  - **Player Drafting**: Users can draft players by selecting a nominating owner, setting a price, and confirming the purchase. Drafted players are automatically removed from the nomination list.
  - **Owner Management**: Owners are removed from the bidding pool once they have drafted the maximum allowed players (16 players).

- **Real-Time Updates**:
  - **Round and Pick Tracking**: The app tracks the current round and pick number, updating the information in real-time as the draft progresses.
  - **Total Budget Tracking**: Displays the total remaining budget of all owners, allowing users to see the financial landscape of the draft at a glance.

- **Team and Owner Overview**:
  - **Owners Tab**: Displays a list of all owners, showing their current roster, remaining budget, and maximum bid.
  - **My Team Tab**: Focuses on the user’s team, showing detailed information about the players drafted by "My Team".

- **Data Persistence**:
  - **Draft Results**: The app saves the draft results to a CSV file, including information such as player name, position, team, nominating owner, buying owner, and purchase price.

## Installation and Setup

1. **Dependencies**: Ensure you have Python installed along with the following libraries:
   - PyQt5
   - CSV (standard Python library)

2. **Running the Application**:
   - Clone the repository and navigate to the project directory.
   - Run `main.py` to start the application: `python main.py`

3. **Customizing**:
   - You can modify the list of owners and players by editing the relevant sections in the `main.py` file and the `players.csv` file in the `resources` folder.

## Usage

- **Starting the Draft**: Launch the application, and use the Draft tab to nominate and draft players.
- **Monitoring Progress**: Use the Owners and My Team tabs to monitor each team's progress throughout the draft.

## Future Enhancements

- **Advanced Error Handling**: Improved user notifications for invalid inputs.
- **Enhanced Data Visualization**: Graphical representations of budgets and draft trends.
- **Support for Different Draft Formats**: Integration of other draft formats and rules.
