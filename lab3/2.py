import re

def check_password(password, criteria):
    if len(password) < 8:
        return "invalid", "Less than 8 Characters"

    errors = []
    special_chars = "!@#"

    if "1" in criteria and not any(char.isupper() for char in password):
        errors.append("Missing Uppercase letters")

    if "2" in criteria and not any(char.islower() for char in password):
        errors.append("Missing Lowercase letters")

    if "3" in criteria and not any(char.isdigit() for char in password):
        errors.append("Missing Numbers")

    if "4" in criteria:
        if not any(char in special_chars for char in password):
            errors.append("Missing Special characters")
        if any(char not in special_chars and not char.isalnum() for char in password):
            errors.append("Contains invalid special characters")

    return ("valid", None) if not errors else ("invalid", ", ".join(errors))

# Get user input for criteria
print("Select criteria to check (comma-separated):")
print("1. Uppercase letters (A-Z)")
print("2. Lowercase letters (a-z)")
print("3. Numbers (0-9)")
print("4. Special characters (!, @, #)")
criteria_input = input("Enter your choices (e.g., 1,3,4): ").strip()
criteria = criteria_input.split(",")

valid_count = 0
invalid_count = 0

# Read passwords from file
try:
    with open("input.txt", "r") as file:
        passwords = file.readlines()

    for password in passwords:
        password = password.strip()
        if not password:
            continue  # Skip empty lines

        status, reason = check_password(password, criteria)
        if status == "valid":
            valid_count += 1
        else:
            invalid_count += 1

    # Display final results
    print("\nTotal Passwords Checked:", valid_count + invalid_count)
    print("Valid Passwords:", valid_count)
    print("Invalid Passwords:", invalid_count)

except FileNotFoundError:
    print("Error: 'input.txt' file not found. Please create the file with passwords.")

