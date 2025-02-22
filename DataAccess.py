import sqlite3

class DataAccess:
    def __init__(self, db_name="casino.db"):
        """Initialize the database connection."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish connection to the database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print("Database connection established.")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def get_all_players(self):
        """Fetch all players from the Players table."""
        try:
            self.cursor.execute("SELECT * FROM Players")
            players = self.cursor.fetchall()
            return players
        except sqlite3.Error as e:
            print(f"Error fetching players: {e}")
            return []

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

# Test the connection and retrieval
if __name__ == "__main__":
    db = DataAccess()
    players = db.get_all_players()
    print("Players:", players)
    db.close()
