import re

def check_password(password, criteria):
    if len(password) < 8:
        print(f"'{password}' -> Invalid password. Less than 8 Characters.")
        return

    errors = []

    # Define allowed special characters
    special_chars = "!@#"

    # Check for each criterion
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

    # Print validation result
    if errors:
        print(f"'{password}' -> Invalid password. " + ", ".join(errors))
    else:
        print(f"'{password}' -> Valid password.")

# Get user input for criteria
print("Select criteria to check (comma-separated):")
print("1. Uppercase letters (A-Z)")
print("2. Lowercase letters (a-z)")
print("3. Numbers (0-9)")
print("4. Special characters (!, @, #)")
criteria_input = input("Enter your choices (e.g., 1,3,4): ").strip()
criteria = criteria_input.split(",")

# List of passwords to check
password_list = [
    "jayanth12345",
    "abc",
    "123456789",
    "abcdefg$",
    "abcdefgABHD!@313",
    "abcdefgABHD$$!@313",
]

# Validate passwords
for password in password_list:
    check_password(password, criteria)
