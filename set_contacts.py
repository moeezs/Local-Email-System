'''
author : Moeez Shaikh
date : 1/16/2023
Takes in username/password and creates contacts while encrypting then password
'''

# Imports
import os
import maskpass
import bcrypt

def save_contacts(num_contacts):
    '''Saves the contact in their own specific directory an adds a file called "password.txt" that stores the encrypted password
    
    Args :
        num_contacts - int : The number of contacts that need to be made. Loops this number of times to store contact
    '''
    for i in range(num_contacts):
        username = input('Enter your username : ')
        password = maskpass.askpass(prompt = f'Enter the password you will use for {username} : ', mask = '*')

        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        try:
            os.mkdir(f'contacts/{username}')

            with open(f'contacts/{username}/password.txt', 'wb') as f_out:
                f_out.write(hashed_pass)
        except FileExistsError:
            print('Contact Already Exists')


def main():
    # Input
    num_contacts = input('Enter the number of contacts you want to add : ')

    while not num_contacts.isnumeric():
        num_contacts = input('Enter the number of contacts you want to add (in numbers) : ')

    num_contacts = int(num_contacts)

    try:
        os.mkdir('contacts')
    except FileExistsError:
        pass

    # Processing / Output
    save_contacts(num_contacts)

if __name__ == '__main__':
    main()