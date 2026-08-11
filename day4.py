'''
Password strength checker (length, char classes, common-password list)
Caesar cipher encrypt/decrypt algorithm
Day 3 of my 100 day coding challenge
I would be building a Python based Caesar cipher that would encrypt and decrypt text.
'''

import string
import sys
from urllib.request import urlopen

upper_case_letters = string.ascii_uppercase
lower_case_letters = string.ascii_lowercase
numbers = string.digits
punctuation = string.punctuation
common_passwords_1 = [
    "123456", "password", "123456789", "12345678", "12345", "111111", "1234567", "sunshine", "qwerty",
    "iloveyou", "princess", "admin", "welcome", "666666", "abc123", "football", "123123", "monkey", 
    "654321", "Admin", "charlie", "aa123456", "donald", "password1", "qwerty123", "letmein", "1234",
    "123", "1q2w3e4r", "123456a", "123qwe", "zxcvbnm", "asdfghjkl", "qazwsx", "1qaz2wsx", "qwertyuiop",
    "password123"
]
common_passwords_2 = str(urlopen('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt').read(), 'utf-8')
common_passwords = common_passwords_1 + common_passwords_2.split('\n')

password = input("Enter a password to check its strength: ")

if password.lower() in common_passwords:
    print("Warning: This password is commonly used and easily guessable. Consider choosing a stronger password.")
    sys.exit(1)

def check_password_strength():
    length = len(password)
    has_upper = any(char in upper_case_letters for char in password)
    has_lower = any(char in lower_case_letters for char in password)
    has_number = any(char in numbers for char in password)
    has_punctuation = any(char in punctuation for char in password)
    is_common = password.lower() in common_passwords

    strength_criteria = {
        "length": length >= 8,
        "upper_case": has_upper,
        "lower_case": has_lower,
        "number": has_number,
        "punctuation": has_punctuation,
        "common_password": not is_common
    }

    return strength_criteria, password

def display_strength_results(strength_criteria, password):
    print("\nPassword Strength Results:")
    print("="*70)
    print(f"Length >= 8: {'Yes' if strength_criteria['length'] else 'No'}")
    print(f"Contains Uppercase Letter: {'Yes' if strength_criteria['upper_case'] else 'No'}")
    print(f"Contains Lowercase Letter: {'Yes' if strength_criteria['lower_case'] else 'No'}")
    print(f"Contains Number: {'Yes' if strength_criteria['number'] else 'No'}")
    print(f"Contains Punctuation: {'Yes' if strength_criteria['punctuation'] else 'No'}")
    print(f"Not a Common Password: {'Yes' if strength_criteria['common_password'] else 'No'}")
    if password in common_passwords:
        print("Warning: This password is commonly used and easily guessable. Consider choosing a stronger password.")
    password_strength = sum(strength_criteria.values())
    if password_strength == 6:
        print("Overall Strength: Strong")
    elif password_strength >= 4:
        print("Overall Strength: Moderate")
    elif password_strength >= 2:
        print("Overall Strength: Weak")
    elif password_strength < 2:
        print("Overall Strength: Very Weak")
    else:
        print("Overall Strength: Unknown")
    print(f"Password strength score: {password_strength}/6")

strength_criteria, password = check_password_strength()
display_strength_results(strength_criteria, password)