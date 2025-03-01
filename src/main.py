import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the token from the .env file
TOKEN = os.getenv('TOKEN')

class MyClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Dynamically load all cogs from the cogs directory
        for filename in os.listdir('./src/cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')

    async def on_ready(self):
        print(f"Logged in as {self.user}!")

if __name__ == "__main__":
    # Initialize the bot with the necessary intents and run it
    client = MyClient()
    client.run(TOKEN)
