from typing import List
from games.card_class import Card

class Player:
    def __init__(self, name: str, is_dealer: bool, game_state: int):
        self.name = name
        self.is_dealer = is_dealer
        self.hand: List[Card] = []
        self.game_state = game_state
    
    def hit(self, new_card: Card):
        """Add a new card to the player's hand"""
        self.hand.append(new_card)
    
    def calculate_hand_value(self) -> int:
        """Calculate the total value of cards in hand, accounting for aces"""
        val = sum(card.get_value() for card in self.hand)
        
        # If there's an ace and counting it as 11 wouldn't bust,
        # add 10 to the total (since aces are counted as 1 by default)
        if self.has_ace() and val + 10 <= 21:
            val += 10
            
        return val
    
    def is_bust(self) -> bool:
        """Check if player's hand value exceeds 21"""
        return self.calculate_hand_value() > 21
    
    def has_ace(self) -> bool:
        """Check if player's hand contains an ace"""
        return any(card.get_value() == 1 for card in self.hand)
    
    def has_blackjack(self) -> bool:
        """Check if player has blackjack (21 with exactly 2 cards)"""
        return self.calculate_hand_value() == 21 and len(self.hand) == 2
    
    def display_hand(self) -> str:
        """Display all cards in hand and total value"""
        cards_str = " ".join(card.get_name_and_suit() for card in self.hand)
        return f"{cards_str} ({self.calculate_hand_value()})"
    
    def display_first_card(self) -> str:
        """Display only the first card in hand"""
        if self.hand:
            return self.hand[0].get_name_and_suit()
    
    def get_name(self) -> str:
        """Return player's name"""
        return self.name