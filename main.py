import settings
import discord
from discord import app_commands
from discord.ext import commands
from cogs.agents import Agents
from discord import Webhook
import aiohttp

logger = settings.logging.getLogger('bot')
cogs_logger = settings.logging.getLogger('cogs')
tree_logger = settings.logging.getLogger('tree')

class Client(commands.Bot): 
    async def setup_hook(self):
        # sync to a specific guild
        # [delete this comment] test_guild = discord.Object(id=...)  # change ... to your test guild_id
        # [and this] self.tree.copy_global_to(guild=test_guild)
        
        # logging info
        logger.info(f'User : {self.user} (ID : {self.user.id})')
        
        # load commands
        await load_commands()
        
        # sync to all servers and add to logger
        synced = await self.tree.sync()
        tree_logger.info(f'Sycned : {len(synced)} Commands to Global')
        
async def load_commands():
    for cogs in settings.COGS_DIR.glob("*.py"):
        if cogs.name != "__init__.py":
            await client.load_extension(f'cogs.{cogs.name[:-3]}')
            # log the commands in the logger
            cogs_logger.info(f'Loaded ({cogs.name})')
        
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

@client.tree.command(name = "reload_commands", description = "reload the commands list")
async def reload_commands(interaction : discord.Interaction):
    reloaded_cogs = 0
    for cogs in settings.COGS_DIR.glob("*.py"):
        if cogs.name != "__init__.py":
            await client.reload_extension(f'cogs.{cogs.name[:-3]}')
            reloaded_cogs += 1
    await interaction.response.send_message(f'Reloaded : {reloaded_cogs} cogs. Auto delete after 4 Seconds', delete_after=4)

client.run(settings.DISCORD_API_SECRET, root_logger = True)