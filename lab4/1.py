import os
import hashlib
import getpass

# A simple in-memory user database (username: (salt, hashed_password))
users_db = {}

def register():
    username = input("Enter a username for registration: ")
    if username in users_db:
        print("Username already exists. Please choose another username.")
        return
    
    password = getpass.getpass("Enter your password: ")
    
    # Generate a 16-byte salt using a secure random generator
    salt = os.urandom(16)
    
    # Hash the password with SHA-256 using PBKDF2 for key stretching
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',           # The hash digest algorithm for HMAC
        password.encode(),  # Convert the password to bytes
        salt,               # Provide the salt
        100000              # It is recommended to use at least 100,000 iterations of SHA-256
    )
    
    # Store the salt and hashed password in the users_db
    users_db[username] = (salt, hashed_password)
    print("Registration successful!")

def login():
    username = input("Enter your username: ")
    if username not in users_db:
        print("Username does not exist!")
        return

    password = getpass.getpass("Enter your password: ")
    salt, stored_hash = users_db[username]
    
    # Hash the provided password with the same salt and iterations
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        100000
    )
    
    # Compare the newly computed hash with the stored hash
    if hashed_password == stored_hash:
        print("Login successful!")
    else:
        print("Invalid password!")

def main():
    while True:
        print("\n--- Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
