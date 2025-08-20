This project is an advanced AI-powered voice assistant built in Python, designed to execute a wide range of system, web, and communication tasks through voice commands. The assistant uses SpeechRecognition for capturing user commands, pyttsx3 for speech synthesis, and integrates with APIs like PyWhatKit and Wikipedia for dynamic actions.

code is in helomo.py file oyu can directly run the file in your mac.

Key Features:

System Control: Shutdown, restart, sleep, open/close applications, and force quit programs via macOS automation scripts.

Bluetooth Management: Turn Bluetooth on/off, list paired devices, and connect to specific devices using blueutil.

Web Operations: Open websites, search Google, and play YouTube videos through voice prompts.

WhatsApp Messaging: Instantly send messages to predefined contacts with voice-only interaction.

Task Management: Add, remove, and list tasks in an integrated voice-controlled to-do list.

Wikipedia Search: Fetch and read aloud topic summaries directly from Wikipedia.

Browser Tab Control: Close specific website tabs in Google Chrome through voice commands.

Continuous Listening Mode: Always-on interaction loop until the user says “exit.”

Technology Stack:

Language: Python

Libraries: speech_recognition, pyttsx3, pywhatkit, wikipedia, subprocess, re, os

Platform: macOS (integrated with osascript and blueutil)

Use Case:
This project can serve as a personal productivity assistant, home automation controller, or a customizable base for creating specialized AI voice assistants.
