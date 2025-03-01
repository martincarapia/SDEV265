import os

def get_db_path():
    """
    Returns the absolute path to the casino.db file, ensuring it's always found.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    db_path = os.path.join(base_dir, "../../Database/casino.db")  # Construct the full path
    return db_path
