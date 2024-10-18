"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                            CStats Timestamp Management                           ║
║                                                                                  ║
║ This script manages saving and retrieving timestamps in either the Windows       ║
║ registry or a JSON file, depending on the operating system. It is used in the    ║
║ CStats application to record the last time an API pull or other event occurred.  ║
║                                                                                  ║
║ Features:                                                                        ║
║ - On Windows (win32), timestamps are saved to and retrieved from the Windows     ║
║   registry.                                                                      ║
║ - On non-Windows platforms (e.g., Linux, macOS), timestamps are saved to and     ║
║   retrieved from a JSON file.                                                    ║
║ - Provides error handling for both reading and writing operations.               ║
║                                                                                  ║
║ Functions:                                                                       ║
║ - save_timestamp: Saves the current timestamp in the appropriate location based  ║
║   on the OS.                                                                     ║
║ - read_timestamp: Reads and returns the saved timestamp from the appropriate     ║
║   location.                                                                      ║
║                                                                                  ║
║ Example usage:                                                                   ║
║     save_timestamp()  # Save the current timestamp                               ║
║     read_timestamp()  # Read the saved timestamp                                 ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""


import sys
import os
import json
from datetime import datetime


def save_timestamp():
    """
    Saves the current timestamp to the Windows registry (if on Windows) or a JSON file (if on another OS).
    """
    timestamp = datetime.now().isoformat()  # Get the current timestamp
    
    if sys.platform == "win32":
        import winreg
        try:
            # Open or create the registry key and save the timestamp
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\CStatsas')
            winreg.SetValueEx(key, 'Timestamp', 0, winreg.REG_SZ, timestamp)
            winreg.CloseKey(key)
            print("Timestamp saved in registry.")
        except Exception as e:
            print(f"Error saving timestamp: {e}")
    
    else:
        # Save timestamp to a JSON file for non-Windows systems
        try:
            data = {'Timestamp': timestamp}
            with open('timestamp.json', 'w') as json_file:
                json.dump(data, json_file)
            print("Timestamp saved to JSON file.")
        except Exception as e:
            print(f"Error saving timestamp: {e}")


def read_timestamp():
    """
    Reads the saved timestamp from the Windows registry (if on Windows) or a JSON file (if on another OS).
    Returns the timestamp if found, otherwise None.
    """
    if sys.platform == "win32":
        import winreg
        try:
            # Open the registry key and read the timestamp
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\CStatsas', 0, winreg.KEY_READ)
            timestamp, _ = winreg.QueryValueEx(key, 'Timestamp')
            winreg.CloseKey(key)
            print(f"Timestamp read from registry: {timestamp}")
            return timestamp
        except FileNotFoundError:
            print("Timestamp not found in registry.")
        except Exception as e:
            print(f"Error reading timestamp: {e}")
    
    else:
        # Read timestamp from a JSON file for non-Windows systems
        try:
            if os.path.exists('timestamp.json'):
                with open('timestamp.json', 'r') as json_file:
                    data = json.load(json_file)
                timestamp = data.get('Timestamp')
                print(f"Timestamp read from JSON file: {timestamp}")
                return timestamp
            else:
                print("Timestamp file not found.")
        except Exception as e:
            print(f"Error reading timestamp: {e}")

    return None


# Example usage
if __name__ == "__main__":
    save_timestamp()  # Save the current timestamp
    read_timestamp()  # Read and print the saved timestamp

