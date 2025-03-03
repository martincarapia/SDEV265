import discord
from discord.ext import commands
import random

class CrapsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tokens = 1
        self.bet_tokens = 0
        self.point = None

    def roll_dice(self):
        """Roll two dice and return the sum."""
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        return dice1 + dice2

    async def play_round(self, ctx):
        """Play a round of craps."""
        # Roll the dice for the come-out roll
        come_out_roll = self.roll_dice()
        await ctx.send(embed=discord.Embed(
            title="Come-Out Roll",
            description=f"You rolled a {come_out_roll} on the come-out roll.",
            color=discord.Color.blue()
        ))

        if come_out_roll in [7, 11]:
            await ctx.send(embed=discord.Embed(
                title="Result",
                description="You win! You rolled a natural.",
                color=discord.Color.green()
            ))
            self.tokens += self.bet_tokens
        elif come_out_roll in [2, 3, 12]:
            await ctx.send(embed=discord.Embed(
                title="Result",
                description="You lose. You rolled a crap.",
                color=discord.Color.red()
            ))
            self.tokens -= self.bet_tokens
        else:
            self.point = come_out_roll
            await ctx.send(embed=discord.Embed(
                title="Point Established",
                description=f"You established a point of {self.point}.",
                color=discord.Color.blue()
            ))

            # Roll the dice until the point is rolled again or a 7 is rolled
            while True:
                roll = self.roll_dice()
                await ctx.send(embed=discord.Embed(
                    title="Roll",
                    description=f"You rolled a {roll}.",
                    color=discord.Color.blue()
                ))

                if roll == self.point:
                    await ctx.send(embed=discord.Embed(
                        title="Result",
                        description="You win! You rolled the point again.",
                        color=discord.Color.green()
                    ))
                    self.tokens += self.bet_tokens
                    break
                elif roll == 7:
                    await ctx.send(embed=discord.Embed(
                        title="Result",
                        description="You lose. You rolled a 7.",
                        color=discord.Color.red()
                    ))
                    self.tokens -= self.bet_tokens
                    break

    async def play_game(self, ctx):
        """Play the craps game."""
        await self.play_round(ctx)
        await ctx.send(embed=discord.Embed(
            title="Tokens",
            description=f"You now have {self.tokens} tokens.",
            color=discord.Color.blue()
        ))

    @commands.command(name="craps", help="Start a game of Craps")
    async def start_craps(self, ctx, wager: int = None):
        if wager is None:
            embed = discord.Embed(
                title="Error",
                description="Please provide a wager amount. Usage: `!craps <wager>`",
                color=discord.Color.red()
            )
            embed.set_footer(text="Created by Emily Schwent")
            await ctx.send(embed=embed)
            return

        if wager <= 0:
            await ctx.send(embed=discord.Embed(
                title="Invalid Bet",
                description="Please enter a positive number for the wager.",
                color=discord.Color.red()
            ))
            return

        self.bet_tokens = wager
        await ctx.send(embed=discord.Embed(
            title="Craps Game",
            description=f"Starting the Craps game with a wager of {wager} tokens...",
            color=discord.Color.blue()
        ).set_footer(text="Created by Emily Schwent"))
        await self.play_game(ctx)

async def setup(bot):
    await bot.add_cog(CrapsCog(bot))