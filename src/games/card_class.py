class Card:
    def __init__(self, id: int, suit: str):
        self.id = id
        self.suit = suit
        self._assign_name()
        self._assign_value()
    
    def _assign_value(self):
        """Determine card's value"""
        self.value = self.id if self.id < 10 else 10
    
    def _assign_name(self):
        """Determine the card's name"""
        name_mapping = {
            1: "A",
            13: "K",
            12: "Q",
            11: "J"
        }
        self.name = name_mapping.get(self.id, str(self.id))
    
    def get_value(self) -> int:
        """Return the card's value"""
        return self.value
    
    def get_name(self) -> str:
        """Return the card's name"""
        return self.name
    
    def get_name_and_suit(self) -> str:
        """Return the card's name and suit"""
        return f"{self.name} {self.suit}"