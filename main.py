import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from module.aiModule import pipelines
from typing import Optional

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        # Sync the command tree with Discord
        pass
    
    async def on_ready(self):
        print('------')
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
      

intents = discord.Intents.default()
intents.message_content = True

bot = Client(command_prefix='$', intents=intents)

@bot.event
async def on_guild_join(guild: discord.Guild):
    # Copy tất cả global commands vào guild mới
    bot.tree.copy_global_to(guild=guild)

    # Sync slash commands cho guild đó
    await bot.tree.sync(guild=guild)

    print(f"Đã auto-register slash commands cho guild mới: {guild.name}")
            
@bot.command()
async def ping(ctx: commands.Context):
    """Responds with 'Pong!' when the command is invoked."""
    latency = bot.latency
    await ctx.channel.send(f"Pong! **`{latency:.2f}ms`**")
    
@bot.command(name='chat', aliases=['c'])
async def chat(ctx: commands.Context, *, question: str):
    """Handles chat messages and generates responses based on the context."""
    try:
        response = pipelines.chat(question)
        await ctx.channel.send(response['answer'])
    except Exception as e:
        await ctx.channel.send(f"Error: {e}")
        
@bot.command(name='train', aliases=['t'])
async def train(ctx: commands.Context, fileURL: Optional[str] = None):
    """Uploads a DOCX or PDF file and writes its content to the vector database."""
    try:
        if fileURL is None:
            try:
                attachment = ctx.message.attachments[0]
                fileURL = attachment.url.split('?ex')[0]
            except IndexError:
                await ctx.channel.send("Please attach a DOCX or PDF file.")
                return
        response = pipelines.write_docs(fileURL)
        await ctx.channel.send(response['answer'])
    except Exception as e:
        await ctx.channel.send(f"Error: {e}")
        
@bot.command(name ='read', aliases=['r'])
async def ReadURL(ctx: commands.Context):
    """Reads a URL"""
    try:
        attachment = ctx.message.attachments[0]
        fileURL = attachment.url.split('?ex')[0]
        await ctx.channel.send(fileURL)
        print(f"Attachment URL: {fileURL}")
    except Exception as e:
        await ctx.channel.send(f"Error: {e}")
        
# Registering slash commands
#.command(name="prefix", description="text", guild=discord.Object(id=735164080742072441))
@bot.tree.command(name="hello", description="Chào người dùng!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Xin chào, {interaction.user.mention}! 👋")
    
@bot.tree.command(name="ping", description="Check the bot's latency.")
async def ping(interaction: discord.Interaction):
    """Responds with 'Pong!' and the bot's latency."""
    latency = bot.latency
    await interaction.response.send_message(f"Pong! **`{latency:.2f}ms`**")
    
@bot.tree.command(name="chat", description="Chat with the bot.")
async def chat(interaction: discord.Interaction, question: str):
    """Handles chat messages and generates responses based on the context."""
    try:
        await interaction.response.defer()
        response = pipelines.chat(question)
        await interaction.followup.send(response['answer'])
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")
        
bot.run(BOT_TOKEN)