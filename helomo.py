import subprocess
import speech_recognition as sr
import os
import pywhatkit as kit
import pyttsx3
import datetime
import wikipedia
import os

# Predefined contacts (just an example, you can expand this or load it dynamically)
contacts = {
    "nice":"919426334625",
    
    "great":"917874038680",
    "saver":"919624245411",
}

def speak(text):

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


import re

def list_bluetooth_devices():
    # List available Bluetooth devices
    result = subprocess.run(['blueutil', '--paired'], capture_output=True, text=True)
    devices = result.stdout.splitlines()
    
    # Use regex to find the device names following the "name:" pattern
    device_names = []
    device_addresses = []
    for device in devices:
        # Use regex to find the part of the line that contains the name and address
        match_name = re.search(r'name:\s*"([^"]+)"', device)
        match_address = re.search(r'address:\s*([\w\-:]+)', device)
        if match_name and match_address:
            device_name = match_name.group(1)
            device_address = match_address.group(1)
            device_names.append(device_name)
            device_addresses.append(device_address)
    
    return device_names, device_addresses

def connect_bluetooth_device(device_index, device_names, device_addresses):
    # Find the device at the given index and connect
    if 0 <= device_index < len(device_names):
        device_name = device_names[device_index]
        device_address = device_addresses[device_index]
        print(f"Connecting to {device_name} with address {device_address}...")
        # Run the `blueutil` command to connect to the device
        subprocess.run(['blueutil', '--connect', device_address])
        speak(f"Connected to {device_name}.")
    else:
        print(f"Device index {device_index + 1} is invalid. Please provide a valid index.")


# Function to turn Bluetooth on or off using blueutil
def toggle_bluetooth(state):
    if state == "on":
        # Turn Bluetooth on
        subprocess.run(['blueutil', '--power', '1'])
    elif state == "off":
        # Turn Bluetooth off
        subprocess.run(['blueutil', '--power', '0'])


def extract_phone_number(full_number):
    """Extract the country code and local number from the provided phone number."""
    if len(full_number) >= 11:  # Ensure the number is valid
        country_code = full_number[:-11]  # The digits before the last 11 digits
        local_number = full_number[-11:]  # The last 11 digits
        return f"+{country_code}{local_number}"  # Concatenate country code with local number
    else:
        return None  



def send_whatsapp_message():
    """Send a WhatsApp message."""
    speak("Who should I send the message to?")
    recipient_name = listen_for_command()
    
    # Look up the recipient's phone number from the contacts dictionary
    recipient_number = contacts.get(recipient_name)
    
    if recipient_number:
        speak(f"What is the message you want to send to {recipient_name}?")
        message = listen_for_command()
        
        
        
        # Extract the country code and local number
        phone_number = extract_phone_number(recipient_number)
        
        if phone_number:
            # Send the message using the full phone number
            kit.sendwhatmsg_instantly(phone_number, message)
            speak("Message sent.")
        else:
            speak("Invalid phone number format. Please make sure it contains at least the last 11 digits for the local number.")
    else:
        speak(f"Sorry, I couldn't find {recipient_name} in the contact list.")

def search_web():
    """Search the web using Google."""
    speak("What do you want to search for?")
    query = listen_for_command()
    if query:  
        kit.search(query)
        speak(f"Searching for {query} on Google.")

def play_youtube():
    """Play a YouTube video."""
    speak("What should I play on YouTube?")
    video = listen_for_command()
    if video:
        kit.playonyt(video)
        speak(f"Playing {video} on YouTube.")

import datetime



   

tasks = {} 
def manage_todo_list():
    """Manage tasks in a to-do list."""
    # Task dictionary to hold task ID and task description

    while True:
        speak("Say 'insert', 'remove', or 'list down'.")
        action = listen_for_command()

        if "insert" in action:
            speak("What is the task you want to add?")
            task = listen_for_command()
            task_id = len(tasks) + 1  # Assign task ID based on current length of tasks
            tasks[task_id] = task  # Store task in dictionary with ID as the key
            speak(f"Task {task_id} added: {task}")

        elif "remove" in action or "done" in action:
            speak("What is the name of the task you want to remove?")
            task_name = listen_for_command()
            task_removed = None  # Variable to store the removed task if found

            # Search for the task by name and remove it
            for task_id, task in list(tasks.items()):
                if task_name.lower() in task.lower():  # Case-insensitive search
                    task_removed = tasks.pop(task_id)
                    speak(f"Task '{task_removed}' removed.")
                    
                    break

            if not task_removed:
                speak(f"Task with name '{task_name}' not found.")
                

        elif "list down" in action:
            if tasks:
                speak("Here are your tasks:")
                print("Your Tasks List:")  # Display tasks on screen
                for task_id, task in tasks.items():
                    speak(f"Task {task_id}: {task}")
          
            else:
                speak("Your to-do list is empty.")
          

        else:
            speak("Invalid action. Please Say 'insert', 'remove', or 'list down'.")
        
        speak("Would you like to manage more tasks? Say 'again' to continue")
        continue_action = listen_for_command()
        if "again" in continue_action:
            manage_todo_list()
        else:
            speak("okay!")
            break
            

def get_wikipedia_summary():
    """Get a Wikipedia summary."""
    speak("What topic should I search for on Wikipedia?")
    topic = listen_for_command()
    if topic:
        try:
            summary = wikipedia.summary(topic, sentences=5)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError:
            speak("Your query is too ambiguous. Please try again.")
        except wikipedia.exceptions.PageError:
            speak("I couldn't find anything on that topic.")




def jarvis_command(command):
    try:
        print(f"Processing command: {command}")  # Debugging output
        
        # System operations
        if "shutdown" in command:
            print("Shutting down the system...")
            subprocess.run(["osascript", "-e", 'tell application "System Events" to shut down'])
        elif "restart" in command:
            print("Restarting the system...")
            subprocess.run(["osascript", "-e", 'tell application "System Events" to restart'])
        elif "sleep" in command:
            print("Putting the system to sleep...")
            subprocess.run(["osascript", "-e", 'tell application "System Events" to sleep'])
        
        elif "force quit" in command:
            app_name = command.replace("force quit", "").strip()
            if app_name:
                print(f"Force quitting the application: {app_name}...")
                subprocess.run(["osascript", "-e", f'tell application "{app_name}" to quit'])
            else:
                print("Please specify the application to force quit.")

        elif "send message" in command:
            send_whatsapp_message()
        elif "search" in command:
            search_web()
        elif "to do" in command:
            manage_todo_list()
       
        elif "play" in command:
            play_youtube()
       
        elif "wikipedia" in command:
            get_wikipedia_summary()

        if "bluetooth on" in command:
            speak("Turning Bluetooth on...")
            toggle_bluetooth("on")
        elif "bluetooth off" in command:
            speak("Turning Bluetooth off...")
            toggle_bluetooth("off")
        elif "list devices" in command:
            print("Listing Bluetooth devices...")
            device_names, device_addresses = list_bluetooth_devices()
            if device_names:
                for idx, device in enumerate(device_names):
                    speak(f"{idx + 1}. {device}")
                return device_names, device_addresses  # Return devices list
            else:
                print("No paired Bluetooth devices found.")
                return [], []  # Return empty lists if no devices found
        elif "connect" in command:
            # Check if a number follows the "connect" command
            match = re.search(r'connect (first|second|third|fourth|fifth|[0-9]+)', command)
            if match:
                # Get the number or ordinal (first, second, etc.)
                device_index = match.group(1)
                device_names, device_addresses = list_bluetooth_devices()
                
                # Map ordinal to list index (1 -> 0, 2 -> 1, etc.)
                if device_index == 'first':
                    device_index = 0
                elif device_index == 'second':
                    device_index = 1
                elif device_index == 'third':
                    device_index = 2
                elif device_index == 'fourth':
                    device_index = 3
                elif device_index == 'fifth':
                    device_index = 4
                else:
                    try:
                        # Convert number string to an integer
                        device_index = int(device_index) - 1
                    except ValueError:
                        print("Invalid number for device index.")
                        return

                # Ensure the index is within bounds
                if 0 <= device_index < len(device_names):
                    connect_bluetooth_device(device_index, device_names, device_addresses)
                else:
                    print("Invalid device number.")
            else:
                print("Please specify a valid device number to connect.")
            # Web operations
        elif "web" in command:
            website_name = command.replace("web", "").strip()
            website_name = website_name.lower().replace(" ", "")
            domain_extensions = [".com", ".org", ".net", ".edu", ".gov"]
            domain_extension = ".com"
            for ext in domain_extensions:
                if website_name.endswith(ext):
                    domain_extension = ""
                    break
            if not any(website_name.endswith(ext) for ext in domain_extensions):
                website_name = website_name + domain_extension
            if not website_name.startswith("http"):
                website_name = "https://" + website_name
            print(f"Opening website: {website_name}")
            subprocess.run(["open", "-a", "Google Chrome", website_name])

        # Application operations
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            open_application(app_name)

        elif "close" in command:
            app_name = command.replace("close", "").strip()
            close_application(app_name)

      
        
        # Close specific website tabs
        elif "off" in command:
            website_name = command.replace("off", "").strip()
            close_website(website_name)
        
        else:
            print("Command not recognized!")
            # For debugging, let's log the raw command to see what it's interpreting.
            print(f"Unrecognized command: {command}")

    except Exception as e:
        print(f"Error executing the command: {e}")


def close_application(app_name):
    try:
        # Check if the application exists in either /System/Applications or /Applications
        app_name = app_name.strip()  # Remove leading/trailing spaces
        app_path = f"/System/Applications/{app_name}.app"
        
        # Check if the application exists in the System Applications folder
        if os.path.exists(app_path):
            print(f"Closing {app_name}...")
            subprocess.run(["osascript", "-e", f'tell application "{app_name}" to quit'])
        else:
            # Otherwise, check the /Applications directory
            app_path = f"/Applications/{app_name}.app"
            if os.path.exists(app_path):
                print(f"Closing {app_name}...")
                subprocess.run(["osascript", "-e", f'tell application "{app_name}" to quit'])
            else:
                print(f"Application {app_name} not found.")

    except Exception as e:
        print(f"Error closing the application: {e}")

def open_application(app_name):
    try:
        app_name = app_name.strip()  # Remove leading/trailing spaces
        # Check if the application exists in either /System/Applications or /Applications
        app_path = f"/System/Applications/{app_name}.app"
        
        if os.path.exists(app_path):
            print(f"Opening {app_name}...")
            subprocess.run(["open", app_path])
        else:
            # Otherwise, check the /Applications directory
            app_path = f"/Applications/{app_name}.app"
            if os.path.exists(app_path):
                print(f"Opening {app_name}...")
                subprocess.run(["open", app_path])
            else:
                print(f"Application {app_name} not found.")

    except Exception as e:
        print(f"Error opening the application: {e}")


def close_website(website_name):
    try:
        # Normalize the website name (e.g., "youtube" -> "youtube.com")
        website_name = website_name.replace(" ", "").lower()

        # AppleScript to get all tabs in Google Chrome
        script = f'''
        tell application "Google Chrome"
            set window_list to every window
            repeat with w in window_list
                set tab_list to every tab of w
                repeat with t in tab_list
                    set tab_url to URL of t
                    if tab_url contains "{website_name}" then
                        close t
                        return "Closing website: {website_name}..."
                    end if
                end repeat
            end repeat
        end tell
        '''
        
        # Execute the AppleScript
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        
        # Output the result (or an error message)
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("Error: Couldn't close the specified website.")
    
    except Exception as e:
        print(f"Error while closing the website: {e}")




def listen_for_command():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening for commands...")

        # Adjust for ambient noise once before listening
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                # Listen for up to 20 seconds or until speech is detected
                audio = recognizer.listen(source, phrase_time_limit=20)
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that. Please try again.")
            except sr.RequestError as e:
                print(f"Error with the speech recognition service: {e}. Please check your internet connection.")
                return ""
            except sr.WaitTimeoutError:
                print("Listening timed out. No command received.")
                return ""


def main():
    print("Starting Jarvis chatbot. Say 'exit' to quit.")

    while True:
        command = listen_for_command()
        if "exit" in command:
            print("Exiting Jarvis chatbot. Goodbye!")
            break
        if command:
            jarvis_command(command)

if __name__ == "__main__":
    main()
