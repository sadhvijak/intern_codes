from cryptography.fernet import Fernet
import json
 
# Generate a key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)
 
# Sensitive information for SharePoint
data = {
    "API_KEY": "",
 
}
 
 
# Encrypt sensitive information
encrypted_sharepoint_data = {key: cipher_suite.encrypt(value.encode()).decode() for key, value in data.items()}
 
# Save encrypted data to a config file
with open('config.json', 'w') as config_file:
    json.dump(encrypted_sharepoint_data, config_file)
 
# Save the encryption key separately (store securely, not in version control)
with open('secret.key', 'wb') as key_file:
    key_file.write(key)
 
print("Encryption complete for SharePoint and GPT. Data saved to 'config.json'.")