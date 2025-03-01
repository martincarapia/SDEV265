import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command(name="help", help="Shows this help message")
    async def help_command(self, ctx):
        prefix = "!"
        embed = discord.Embed(title="Help", description=f"List of available commands (Prefix: {prefix}):", color=discord.Color.blue())
        
        for command in self.bot.commands:
            embed.add_field(name=f"{prefix}{command.name}", value=f"{command.help}", inline=False)
        
        embed.set_footer(text="Created by Martin Carapia")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))