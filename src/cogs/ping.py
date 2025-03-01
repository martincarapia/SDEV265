import discord
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Check the bot's latency")
    async def ping(self, ctx):
        latency_ms = round(self.bot.latency * 1000)  # Convert latency to ms
        embed = discord.Embed(
            title="Pong!",
            description=f"Latency is {latency_ms}ms.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PingCog(bot))