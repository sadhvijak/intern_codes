from cryptography.fernet import Fernet
import json

# Load the encryption key
with open('secret.key', 'rb') as key_file:
    key = key_file.read()
        
    cipher_suite = Fernet(key)

    # Load the encrypted configuration data
    with open('config.json', 'r') as config_file:
        encrypted_data = json.load(config_file)

    # Decrypt the sensitive information
    data = {key: cipher_suite.decrypt(value.encode()).decode() for key, value in encrypted_data.items()}
print(data["API_KEY"])
