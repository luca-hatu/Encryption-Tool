from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def generate_key():
    return os.urandom(32)

def encrypt(text, key):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(text.encode()) + padder.finalize()
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    encrypted_text = iv + encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_text

def decrypt(encrypted_text, key):
    iv = encrypted_text[:16]
    encrypted_data = encrypted_text[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data.decode()
import binascii

def main():
    while True:
        print("1. Generate Encryption Key")
        print("2. Encrypt Text")
        print("3. Decrypt Text")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            global encryption_key
            encryption_key = generate_key()
            print(f"Encryption Key (hex): {encryption_key.hex()}")

        elif choice == '2':
            plaintext = input("Enter text to encrypt: ")
            if 'encryption_key' not in globals():
                print("Please generate an encryption key first.")
                continue
            encrypted_text = encrypt(plaintext, encryption_key)
            print(f"Encrypted Text (hex): {binascii.hexlify(encrypted_text).decode()}")

        elif choice == '3':
            encrypted_text_hex = input("Enter encrypted text (hex): ")
            key_hex = input("Enter encryption key (hex): ")
            try:
                encrypted_text = binascii.unhexlify(encrypted_text_hex)
                key = binascii.unhexlify(key_hex)
                decrypted_text = decrypt(encrypted_text, key)
                print(f"Decrypted Text: {decrypted_text}")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid option. Please select again.")

if __name__ == "__main__":
    main()
