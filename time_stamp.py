import winreg
from datetime import datetime

# Function to save timestamp
def save_timestamp():
    timestamp = datetime.now().isoformat()
    try:
        # Open the registry key
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\CStatsas')
        # Set the value
        winreg.SetValueEx(key, 'Timestamp', 0, winreg.REG_SZ, timestamp)
        # Close the key
        winreg.CloseKey(key)
        print("Timestamp saved in registry.")
    except Exception as e:
        print(f"Error saving timestamp: {e}")

# Function to read timestamp
def read_timestamp():
    try:
        # Open the registry key
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\CStatsas', 0, winreg.KEY_READ)
        # Read the value
        timestamp, _ = winreg.QueryValueEx(key, 'Timestamp')
        # Close the key
        winreg.CloseKey(key)
        print(f"Timestamp read from registry: {timestamp}")
        return timestamp
    except FileNotFoundError:
        print("Timestamp not found in registry.")
    except Exception as e:
        print(f"Error reading timestamp: {e}")
    
    #save_timestamp()
    return None

# Example usage
if __name__ == "__main__":
    save_timestamp()
    read_timestamp()
