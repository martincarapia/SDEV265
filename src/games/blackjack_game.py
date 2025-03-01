from typing import List
from games.deck_class import Deck
from games.player_class import Player
import discord

class BlackJack:
    # Game states
    PLAYING = 0
    BUST = 1
    WINNER = 2

    def __init__(self, ctx):
        self.ctx = ctx

    async def display_cards(self, table: List[Player], hide: bool):
        """Display cards for all players, optionally hiding dealer's second card"""
        embed = discord.Embed(title="Blackjack Game", description="Current hands")
        for player in table:
            if player.is_dealer and hide:
                embed.add_field(name=player.get_name(), value=player.display_first_card(), inline=False)
            else:
                embed.add_field(name=player.get_name(), value=player.display_hand(), inline=False)
        await self.ctx.send(embed=embed)

    async def play(self):
        # Initialize table and players
        table: List[Player] = []
        game_over = False

        # Add dealer
        table.append(Player("Dealer", True, self.PLAYING))

        # Add players
        add_player = True
        while add_player:
            await self.ctx.send("Player name:")
            name = await self.bot.wait_for('message')
            table.append(Player(name.content, False, self.PLAYING))
            
            await self.ctx.send("Add another player? (Y/N) Note: game will start if 'Y' or 'N' is not typed:")
            response = await self.bot.wait_for('message')
            add_player = response.content.lower() == 'y'

        # Create and shuffle deck
        deck = Deck(Deck.calc_num_of_decks(table))
        deck.shuffle()

        # Initial deal
        for _ in range(2):
            for player in table:
                player.hit(deck.deal())

        await self.display_cards(table, True)
        await self.ctx.send("Starting play...\n")

        # Check for blackjacks
        for player in table:
            if player.has_blackjack():
                player.game_state = self.WINNER
                await self.ctx.send(f"{player.name} has Blackjack!")

                if player.is_dealer:
                    await self.ctx.send("Dealer has Blackjack! The game is over")
                    game_over = True

        # Game continues...
        dealer_bust = False

        if not game_over:
            # Player turns
            for player in table:
                if player.is_dealer or player.game_state == self.WINNER:
                    continue
                
                is_hit = True
                while is_hit and player.game_state != self.WINNER:
                    await self.ctx.send(f"{player.get_name()} has {player.display_hand()}")

                    if not player.is_bust():
                        await self.ctx.send("Hit or stand?")
                        choice = await self.bot.wait_for('message')
                        if choice.content.lower() == "hit":
                            player.hit(deck.deal())
                            await self.ctx.send(f"{player.get_name()} hits")
                        else:
                            await self.ctx.send(f"{player.get_name()} stands")
                            is_hit = False

                        if player.calculate_hand_value() == 21:
                            await self.ctx.send(f"{player.get_name()} hits 21!")
                            player.game_state = self.WINNER
                    else:
                        await self.ctx.send("Bust! AHAHAHA Loser!")
                        is_hit = False
                        player.game_state = self.BUST

            # Dealer's turn
            dealer = table[0]
            await self.ctx.send(f"Dealer reveals hand with {dealer.display_hand()}")
            
            while True:
                dealer_value = dealer.calculate_hand_value()
                if (dealer_value == 17 and dealer.has_ace()) or dealer_value < 17:
                    dealer.hit(deck.deal())
                    await self.ctx.send(f"Dealer hits and now has: {dealer.display_hand()}")
                else:
                    break

            await self.ctx.send("Dealer concludes play")

            if dealer.calculate_hand_value() > 21:
                dealer_bust = True
                dealer.game_state = self.BUST
                await self.ctx.send("Dealer busts!")

        # Determine winners
        dealers_hand = table[0].calculate_hand_value()

        for player in table:
            if dealer_bust and player.game_state != self.BUST:
                player.game_state = self.WINNER
            elif not dealer_bust and player.game_state == self.PLAYING and player.calculate_hand_value() > dealers_hand:
                player.game_state = self.WINNER

        # Display final results
        await self.display_cards(table, False)

        for player in table:
            player_value = player.calculate_hand_value()
            if player.game_state == self.WINNER:
                await self.ctx.send(f"{player.get_name()} wins with a hand of {player_value} against the dealer's hand of {dealers_hand}")
            elif not player.is_dealer:
                await self.ctx.send(f"{player.get_name()} loses with a hand of {player_value} against the dealer's hand of {dealers_hand}")

if __name__ == "__main__":
    game = BlackJack()
    game.play()