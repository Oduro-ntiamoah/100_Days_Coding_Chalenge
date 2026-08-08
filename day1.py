'''
Password Generator.
Day 1 of my 100 day coding challenge
I would be building a Python based Password generator that would generate a random password
'''

import random

lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
symbols = '!@#$%^&*()'
numbers = '1234567890'
all_characters = lowercase_letters + uppercase_letters + symbols + numbers

def password_generator():
    try:    
        password_length = int(input("How long do you want your password: "))

        if password_length < 8:
            password_length = int(input("Put in a number greater than 8: "))
            if password_length < 8:
                password_generator()
        else:
            password = ''.join(random.choice(all_characters) for char in range (password_length))
            print(password)
    except ValueError:
        print("Please enter a valid number")
        password_generator()        

password_generator()