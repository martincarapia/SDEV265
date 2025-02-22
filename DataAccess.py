import sqlite3  #Import SQLite library to handle database operations

class DataAccess:
    """Handles database connection and operations for the casino bot."""

    def __init__(self, db_name="casino.db"):
        """
        Initializes the database connection.

        :param db_name: The name of the SQLite database file.
        """
        self.db_name = db_name  #Store database name
        self.conn = None  #Placeholder for the database connection
        self.cursor = None  #Placeholder for the database cursor
        self.connect()  #Establish connection when the object is created

    def connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name)  #Connect to database
            self.cursor = self.conn.cursor()  #Create a cursor for executing queries
            print("Database connection established.")  #Log success message
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")  #Log any connection errors

    def get_all_players(self):
        """
        Retrieves all player records from the 'Players' table.

        :return: A list of tuples containing player data.
        """
        try:
            self.cursor.execute("SELECT * FROM Players")  #Execute SQL query to get all players
            players = self.cursor.fetchall()  #Fetch all results from query
            return players  #Return player data
        except sqlite3.Error as e:
            print(f"Error fetching players: {e}")  #Log any errors
            return []  #Return an empty list in case of an error

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()  #Close the connection to free up resources
            print("Database connection closed.")  #Log success message

#Testing the database connection when this script is run directly
if __name__ == "__main__":
    """
    This block ensures that the following code only runs when this script is executed directly,
    and NOT when it is imported into another module.
    """
    db = DataAccess()  #Create an instance of the DataAccess class
    players = db.get_all_players()  #Retrieve all players
    print("Players:", players)  #Print player data to verify connection
    db.close()  #Close database connection
