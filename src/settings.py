import json
settings = {}
file_path = './settings.json'
try:
    # Open the JSON file for reading
    with open(file_path, 'r') as json_file:
        # Load the JSON data into the dictionary
        settings = json.load(json_file)
    print("JSON data loaded successfully.")
    HEIGHT =  settings['HEIGHT']
    WIDTH = settings['WIDTH']
    FPS = settings['FPS']
    TOP_BOUND = settings['TOP_BOUND']*HEIGHT
    BOTTOM_BOUND = settings['BOTTOM_BOUND'] *HEIGHT
    SMASH_ACTIVE = settings['SMASH_ACTIVE']
    CPU_PADDLE_START = [
        settings['CPU_PADDLE_START'][0]*WIDTH,
        settings['CPU_PADDLE_START'][1]*HEIGHT
    ]
    USER_PADDLE_START = [
        settings['USER_PADDLE_START'][0]*WIDTH,
        settings['USER_PADDLE_START'][1]*HEIGHT
    ]
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except json.JSONDecodeError:
    print(f"Error decoding JSON in '{file_path}'. Please check the file format.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

