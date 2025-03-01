from typing import List
import random
from games.card_class import Card

class Deck:
    def __init__(self, num_decks: int = None):
        self.the_deck: List[Card] = []
        
        if num_decks is not None:
            print(f"Starting game with {num_decks} deck(s)")
            for _ in range(num_decks):
                self._create_one_deck()
        else:
            self._create_one_deck()
    
    @staticmethod
    def calc_num_of_decks(table: List['Player']) -> int:
        """Calculate number of decks needed based on number of players"""
        if len(table) < 4:
            return 1
        elif len(table) == 4:
            return 2
        else:
            return 6
    
    def _create_one_deck(self):
        """Create one standard 52-card deck"""
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        for suit in suits:
            for value in range(1, 14):
                self.the_deck.append(Card(value, suit))
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.the_deck)
    
    def deal(self) -> Card:
        """Deal a card from the top of the deck"""
        return self.the_deck.pop(0)
    
    def replenish(self, returned_card: Card):
        """Add a card back to the deck"""
        self.the_deck.append(returned_card)
    
    def get_deck_size(self) -> int:
        """Return the number of cards in the deck"""
        return len(self.the_deck)
    
    def display_deck(self):
        """Display all cards in the deck"""
        for card in self.the_deck:
            print(card.get_name_and_suit())