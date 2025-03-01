import random
import discord
from discord.ext import commands

class SlotsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slots", help="Play the slots game")
    async def play_slots(self, ctx, wager: int = None, luck: int = 30):
        if wager is None:
            embed = discord.Embed(
                title="Error",
                description="Please provide a wager amount. Usage: `!slots <wager> [luck]`",
                color=discord.Color.red()
            )
            embed.set_footer(text="Created by Elijah Mckinney")
            await ctx.send(embed=embed)
            return

        if luck < 0 or luck > 100:
            embed = discord.Embed(
                title="Error",
                description="Luck value must be between 0 and 100.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Created by Elijah Mckinney")
            await ctx.send(embed=embed)
            return

        emojis = ["🍍", "🍉", "🍒", "🍋", "🍊", "🍇"]
        result = [random.choice(emojis) for _ in range(3)]
        coin_multiplier = random.randint(1, 5)

        # Adjust the probability of winning based on the luck value
        win_probability = 0.1 + (luck / 100) * 0.4  # Base 10% + up to 40% from luck
        if random.random() < win_probability:
            result = [random.choice(emojis)] * 3

        if result[0] == result[1] == result[2]:
            earnings = wager * coin_multiplier
            embed = discord.Embed(title="You Win!", color=discord.Color.green())
            embed.add_field(name="Result", value=' '.join(result), inline=False)
            embed.add_field(name="Earnings", value=f"You earned {earnings} coins", inline=False)
        else:
            embed = discord.Embed(title="You Lose!", color=discord.Color.red())
            embed.add_field(name="Result", value=' '.join(result), inline=False)
            embed.add_field(name="Loss", value=f"You lost {wager} coins", inline=False)

        embed.set_footer(text="Created by Elijah Mckinney")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SlotsCog(bot))