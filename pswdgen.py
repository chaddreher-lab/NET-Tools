import random
import string

def generate_password(length=12):
    """Generate a random password."""
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    print("Generated Password:", password)

# Ask the user for the desired password length
try:
    length = int(input("Enter the desired password length: "))
    if length <= 0:
        print("Password length must be a positive number.")
    else:
        generate_password(length)
except ValueError:
    print("Invalid input. Please enter a valid number.")