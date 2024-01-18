import json

# Get user input
flask_port = input("Enter Flask port: ")
username = input("Enter username: ")
password = input("Enter password: ")

# Create config dictionary
config = {
    "flask_port": flask_port,
    "username": username,
    "password": password
}

# Save config to config.json
with open('config.json', 'w') as json_file:
    json.dump(config, json_file)

print("Config has been saved to config.json! 🌟")

