import discord
from discord.ext import commands
from typing import List
from games.deck_class import Deck
from games.player_class import Player

PLAYING = 0
BUST = 1
WINNER = 2

class BlackjackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="blackjack", help="Start a game of Blackjack")
    async def start_blackjack(self, ctx):
        async def display_cards(table: List[Player], hide: bool):
            """Display cards for all players, optionally hiding dealer's second card"""
            embed = discord.Embed(title="Blackjack Game", description="Current hands")
            for player in table:
                if player.is_dealer and hide:
                    embed.add_field(name=player.get_name(), value=player.display_first_card(), inline=False)
                else:
                    embed.add_field(name=player.get_name(), value=player.display_hand(), inline=False)
            await ctx.send(embed=embed)

        async def send_embed_message(title: str, description: str):
            embed = discord.Embed(title=title, description=description)
            await ctx.send(embed=embed)

        def check_blackjack(player: Player):
            if player.has_blackjack():
                player.game_state = WINNER
                return True
            return False

        # Initialize table and players
        table: List[Player] = []
        game_over = False

        # Add dealer
        table.append(Player("Dealer", True, PLAYING))

        # Add the user who requested the game
        table.append(Player(ctx.author.name, False, PLAYING))

        # Create and shuffle deck
        deck = Deck(Deck.calc_num_of_decks(table))
        deck.shuffle()

        # Initial deal
        for _ in range(2):
            for player in table:
                player.hit(deck.deal())

        await display_cards(table, True)

        # Check for blackjacks
        for player in table:
            if check_blackjack(player):
                await send_embed_message("Blackjack!", f"{player.name} has Blackjack!")
                if player.is_dealer:
                    await send_embed_message("Game Over", "Dealer has Blackjack! The game is over")
                    game_over = True

        # Game continues...
        dealer_bust = False

        if not game_over:
            # Player turns
            for player in table:
                if player.is_dealer or player.game_state == WINNER:
                    continue
                
                is_hit = True
                while is_hit and player.game_state != WINNER:
                    if not player.is_bust():
                        await send_embed_message(f"{player.get_name()}'s Turn", f"{player.get_name()} has {player.display_hand()}\nHit or Stand?")
                        choice = await self.bot.wait_for('message')
                        if choice.content.lower() == "hit":
                            player.hit(deck.deal())
                        else:
                            is_hit = False

                        if player.calculate_hand_value() == 21:
                            player.game_state = WINNER
                    else:
                        await send_embed_message(f"{player.get_name()}'s Turn", f"{player.get_name()} BUSTS with {player.display_hand()}")
                        await send_embed_message("Bust!", "Bust! AHAHAHA Loser!")
                        is_hit = False
                        player.game_state = BUST

            # Dealer's turn
            dealer = table[0]
            await send_embed_message("Dealer's Turn", f"Dealer reveals hand with {dealer.display_hand()}")
            
            while True:
                dealer_value = dealer.calculate_hand_value()
                if (dealer_value == 17 and dealer.has_ace()) or dealer_value < 17:
                    dealer.hit(deck.deal())
                    await send_embed_message("Dealer Hits", f"Dealer hits and now has: {dealer.display_hand()}")
                else:
                    break

            if dealer.calculate_hand_value() > 21:
                dealer_bust = True
                dealer.game_state = BUST
                await send_embed_message("Dealer Busts", "Dealer busts!")

        # Determine winners
        dealers_hand = table[0].calculate_hand_value()

        for player in table:
            if dealer_bust and player.game_state != BUST:
                player.game_state = WINNER
            elif not dealer_bust and player.game_state == PLAYING and player.calculate_hand_value() > dealers_hand:
                player.game_state = WINNER

        # Display final results
        await display_cards(table, False)

        for player in table:
            player_value = player.calculate_hand_value()
            if player.game_state == WINNER:
                embed = discord.Embed(title="Winner!", description=f"{player.get_name()} wins with a hand of {player_value} against the dealer's hand of {dealers_hand}")
                embed.set_footer(text="Created by Ally Marks")
                await ctx.send(embed=embed)
            elif not player.is_dealer:
                embed = discord.Embed(title="Loser", description=f"{player.get_name()} loses with a hand of {player_value} against the dealer's hand of {dealers_hand}")
                embed.set_footer(text="Created by Ally Marks")
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BlackjackCog(bot))