'''
Today is day 3. I will be making a Caesar cipher encrypt/decrypt algorithm
Side note: Caesar cipher is a type of substitution cipher in which each letter in the plaintext is shifted a certain number of places down or up the alphabet.
'''

import sys
import string

ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

def ceaser_shift(text, shift, alphabet=ALPHABET):
    result = []
    alphabet_size = len(alphabet)

    for char in text:
        if char in alphabet:
            old_pos = alphabet.index(char)
            new_pos = (old_pos + shift) % alphabet_size
            result.append(alphabet[new_pos])
        else:
            result.append(char)

    return ''.join(result)

def encrypt(plaintext, shift, alphabet=ALPHABET):
    return ceaser_shift(plaintext, shift, alphabet)

def decrypt(ciphertext, shift, alphabet=ALPHABET):
    return ceaser_shift(ciphertext, -shift, alphabet)

def validate_shift(shift_input):
    try:
        shift = int(shift_input)
        return shift
    except ValueError:
        print("Invalid shift value. Please enter a non-negative integer.")
        sys.exit(1)

def validate_mode(mode):
    if mode.lower() in ['encrypt', 'e', 'decrypt', 'd']:
        return mode.lower()
    else:
        print(f'Invalid mode: {mode}. Please choose "encrypt" or "decrypt".')
        sys.exit(1)

def parse_arguments():
    if len(sys.argv) == 1:
        return None, None, None
    
    if len(sys.argv) < 4:
        print("Usage: python day3.py <mode> <text> <shift>")
        print("Mode: 'encrypt' or 'decrypt'")
        print("Text: The text to encrypt or decrypt")
        print("Shift: A non-negative integer for the shift value")
        sys.exit(1)

    mode = validate_mode(sys.argv[1])
    text = sys.argv[2]
    shift = validate_shift(sys.argv[3])

    return mode, text, shift

def interactive_mode():
    print("Welcome to the Caesar Cipher Tool!")

    while True:
        mode = input("Enter mode (encrypt/decrypt): ").lower()
        if mode in ['encrypt', 'e', 'decrypt', 'd']:
            break
        print("Invalid mode. Please enter 'encrypt' or 'decrypt'.")
        
    text = input("Enter the text: ")

    while True:
        try:
            shift = int(input("Enter a shift value (Integer): "))
            break
        except ValueError:
            print("Invalid shift value. Please enter an integer.")


    return mode, text, shift

def main():

    mode, text, shift = parse_arguments()

    if mode is None:
        mode, text, shift = interactive_mode()

    if mode in ['encrypt', 'e']:
        result = encrypt(text, shift)
        print(f"Encrypted text: {result}")
    else:
        result = decrypt(text, shift)
        print(f"Decrypted text: {result}")

if __name__ == "__main__":
    main()

