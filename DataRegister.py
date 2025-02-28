import sqlite3
from db_utils import get_db_path  # Import our utility function

class DataRegister:
    """Handles registration of players, games, and money in the casino bot."""

    def __init__(self):
        """Initialize the database connection."""
        self.db_name = get_db_path()
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print("Database connection established.")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def register_player(self, discord_id, username, coin_amount=0):
        """
        Registers a new player in the Players table.
        :param discord_id: The Discord ID of the player.
        :param username: The username of the player.
        :param coin_amount: Initial coin amount (default is 0).
        """
        try:
            self.cursor.execute(
                "INSERT INTO Players (discord_id, username, coin_amount) VALUES (?, ?, ?)",
                (discord_id, username, coin_amount)
            )
            self.conn.commit()
            print(f"Player '{username}' registered successfully with {coin_amount} coins.")
        except sqlite3.IntegrityError:
            print(f"Error: A player with Discord ID {discord_id} already exists.")
        except sqlite3.Error as e:
            print(f"Error registering player: {e}")

    def register_game(self, name, description, min_bet, max_bet):
        """
        Registers a new game in the Games table.
        
        :param name: The name of the game.
        :param description: A description of the game.
        :param min_bet: Minimum bet amount.
        :param max_bet: Maximum bet amount.
        """
        try:
            self.cursor.execute(
                "INSERT INTO Games (name, description, min_bet, max_bet) VALUES (?, ?, ?, ?)",
                (name, description, min_bet, max_bet)
            )
            self.conn.commit()
            print(f"Game '{name}' registered successfully.")
        except sqlite3.Error as e:
            print(f"Error registering game: {e}")

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

# Testing the registration methods (manual user input)
if __name__ == "__main__":
    db = DataRegister()

    # Register a player for testing
    discord_id = input("Enter Discord ID for player: ")
    username = input("Enter Username for player: ")
    coin_amount = input("Enter starting coin amount (default 0): ")
    coin_amount = int(coin_amount) if coin_amount.isdigit() else 0
    db.register_player(discord_id, username, coin_amount)

    # Register a game for testing
    game_name = input("\nEnter game name: ")
    game_description = input("Enter game description: ")
    min_bet = input("Enter minimum bet amount: ")
    max_bet = input("Enter maximum bet amount: ")
    min_bet = int(min_bet) if min_bet.isdigit() else 0
    max_bet = int(max_bet) if max_bet.isdigit() else 0
    db.register_game(game_name, game_description, min_bet, max_bet)

    db.close()
