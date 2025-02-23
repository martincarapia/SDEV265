import sqlite3
from db_utils import get_db_path

class DataAccess:
    """Handles interactions with the casino database."""

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

    def update_leaderboard(self, player_id, total_winnings):
        """
        Update the leaderboard with the player's total winnings.
        If the player is not in the leaderboard, add them.
        
        :param player_id: ID of the player.
        :param total_winnings: Total winnings of the player.
        """
        try:
            # Check if the player already exists in the leaderboard
            self.cursor.execute("SELECT * FROM Leaderboard WHERE player_id = ?", (player_id,))
            existing_player = self.cursor.fetchone()
            
            if existing_player:
                # If player exists, update their total winnings
                self.cursor.execute(
                    "UPDATE Leaderboard SET total_winnings = ? WHERE player_id = ?",
                    (total_winnings, player_id)
                )
            else:
                # If player does not exist, insert them into the leaderboard
                self.cursor.execute(
                    "INSERT INTO Leaderboard (player_id, total_winnings, rank) VALUES (?, ?, ?)",
                    (player_id, total_winnings, 0)  # Rank will be updated later
                )
            self.conn.commit()
            print(f"Leaderboard updated for player {player_id}.")
        except sqlite3.Error as e:
            print(f"Error updating leaderboard: {e}")

    def update_ranks(self):
        """
        Update the ranks of all players based on their total winnings.
        """
        try:
            # Get all players in descending order of total winnings
            self.cursor.execute(
                "SELECT player_id FROM Leaderboard ORDER BY total_winnings DESC"
            )
            players = self.cursor.fetchall()

            # Update ranks based on the order
            for rank, player in enumerate(players, start=1):
                self.cursor.execute(
                    "UPDATE Leaderboard SET rank = ? WHERE player_id = ?",
                    (rank, player[0])
                )
            self.conn.commit()
            print("Ranks updated for all players.")
        except sqlite3.Error as e:
            print(f"Error updating ranks: {e}")

    def add_transaction(self, player_id, transaction_type, amount):
        """
        Add a transaction record for a player.
        
        :param player_id: ID of the player.
        :param transaction_type: Type of transaction (e.g., 'deposit', 'withdrawal').
        :param amount: Amount of the transaction.
        """
        try:
            self.cursor.execute(
                "INSERT INTO Transactions (player_id, transaction_type, amount, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                (player_id, transaction_type, amount)
            )
            self.conn.commit()
            print(f"Transaction added for player {player_id}.")
        except sqlite3.Error as e:
            print(f"Error adding transaction: {e}")

    def add_game_history(self, game_id, player_id, game_mode, wager, result, winnings, win):
        """
        Add a record to the GameHistory table.
        
        :param game_id: ID of the game played.
        :param player_id: ID of the player.
        :param game_mode: The mode of the game played.
        :param wager: The amount wagered.
        :param result: The result of the game (win/loss).
        :param winnings: The amount won or lost.
        :param win: 1 for a win, 0 for a loss.
        """
        try:
            self.cursor.execute(
                "INSERT INTO GameHistory (game_id, player_id, game_mode, wager, result, winnings, win, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (game_id, player_id, game_mode, wager, result, winnings, win)
            )
            self.conn.commit()
            print(f"Game history added for player {player_id} in game {game_id}.")
        except sqlite3.Error as e:
            print(f"Error adding game history: {e}")

    def reset_database(self):
        """
        Truncate all tables and refill with sample data for testing.
        This method will only execute if the user confirms with 'yes'.
        """
        user_input = input("Are you sure you want to reset the database and refill with sample data? (yes/no): ").lower()
        
        if user_input == 'yes':
            try:
                # Truncate all tables
                self.cursor.execute("DELETE FROM GameHistory")
                self.cursor.execute("DELETE FROM Leaderboard")
                self.cursor.execute("DELETE FROM Transactions")
                self.cursor.execute("DELETE FROM Players")
                self.cursor.execute("DELETE FROM Games")
                self.conn.commit()

                # Add sample data for testing
                self.cursor.execute(
                    "INSERT INTO Players (discord_id, username, coin_amount) VALUES (?, ?, ?)",
                    ('12345', 'TonyRazzleDazzle', 1000)
                )
                self.cursor.execute(
                    "INSERT INTO Games (name, description, min_bet, max_bet) VALUES (?, ?, ?, ?)",
                    ('Blackjack', 'What\'s 9 + 10?', 10, 1000)
                )
                self.cursor.execute(
                    "INSERT INTO Leaderboard (player_id, total_winnings, rank) VALUES (?, ?, ?)",
                    (1, 500, 1)
                )
                self.cursor.execute(
                    "INSERT INTO Transactions (player_id, transaction_type, amount) VALUES (?, ?, ?)",
                    (1, 'Begged for it', 500)
                )
                self.cursor.execute(
                    "INSERT INTO GameHistory (game_id, player_id, game_mode, wager, result, winnings, win) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (1, 1, 'Classic', 100, 'win', 200, 1)
                )
                self.conn.commit()
                print("Database reset and sample data added.")
            except sqlite3.Error as e:
                print(f"Error resetting database: {e}")
        else:
            print("Database reset skipped.")

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

# Test the functions (manual input for testing)
if __name__ == "__main__":
    db = DataAccess()

    # Test update_leaderboard manually
    player_id = input("Enter player ID for leaderboard update: ")
    total_winnings = float(input("Enter total winnings for the player: "))
    db.update_leaderboard(player_id, total_winnings)

    # Test update_ranks manually
    db.update_ranks()

    # Test add_transaction manually
    player_id = input("Enter player ID for transaction: ")
    transaction_type = input("Enter transaction type (deposit/withdrawal): ")
    amount = float(input("Enter amount for the transaction: "))
    db.add_transaction(player_id, transaction_type, amount)

    # Test add_game_history manually
    game_id = input("Enter game ID for history: ")
    player_id = input("Enter player ID for game history: ")
    game_mode = input("Enter game mode: ")
    wager = float(input("Enter wager amount: "))
    result = input("Enter result (win/loss): ")
    winnings = float(input("Enter winnings amount: "))
    win = 1 if result.lower() == "win" else 0
    db.add_game_history(game_id, player_id, game_mode, wager, result, winnings, win)

    # Reset database if needed
    db.reset_database()

    db.close()