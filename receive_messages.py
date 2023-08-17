'''
author : Moeez Shaikh
date : 1/16/2023
Makes the user sign in and allows it view all the messages they have received
'''

# Imports
import os
import maskpass
import bcrypt

def sign_in(contacts):
    '''Signs the user in and lets them send messages if they have the correct username and password
    
    Args :
        contacts - list[str] : this is the list of all the saved usernames (contacts) that are in the contacts folder

    Returns : 
        False : this is only returned if the inputted username is not one of the contacts in the saved database
    '''
    username = input('Enter your username : ')
    if username_check(username, contacts) == False:
        print(f'Wrong username. {username} is not in our contact list.')
        return False

    with open(f'contacts/{username}/password.txt', 'rb') as f_in:
        read_pass = f_in.read()

    password = maskpass.askpass(prompt = 'Enter your password : ', mask = '*')
    
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), read_pass)

    if hashed_pass != read_pass:
        print('Wrong Password. Restart and log in again.')
    elif hashed_pass == read_pass:
        print(f'Welcome {username}')
        check_messages(contacts, username)
  

def username_check(username, contacts):
  '''Checks if the username that the user provided is in the contacts folder
    
    Args :
        username - str : the username that is inputted by the user
        contacts - list[str] : this is the list of all the saved usernames (contacts) that are in the contacts folder
    
    Returns :
        True - if the username entered is a username that is saved as a contact
        False - if the username entered does not match the username in the contacts
    '''

  for i, contact in enumerate(contacts):
      if contact == username:
          return True
    
  return False


def check_messages(contacts, username):
    '''For every contact message, it adds the message to the messages list
    
    Args : 
        contacts - list[str] : all the contacts that are saved in the folder
        username - str : the username that is inputted by the user and is signed in
    '''

    messages = []
    for contact in contacts:
        try:
            with open(f'contacts/{username}/messages/message_{contact}.txt') as f_in:
                message = f_in.read()
                messages.append(message)
        except FileNotFoundError:
            pass

    display_messages(messages)


def display_messages(messages):
    '''This takes in the lists of messages and displays them to the logged in user
    
    Args :
        messages - list[str] : this is the list of all the messages available in the logged in user's directory
    '''

    if len(messages):
        print('Your Messages')
    else:
        print('You have no messages')

    sort_alpha(messages)

    for message in messages:
        print(message)


def sort_alpha(messages):
    '''This takes in the list contacts and sorts them alphabetically
    
    Args :
        contacts - list[str] : this is the list of all the saved usernames (contacts) that are in the contacts folder
    '''
    for i in range(len(messages)):
        for j in range(len(messages) - 1):
            if messages[j] > messages[j + 1]:
                messages[j], messages[j + 1] = messages[j + 1], messages[j]


def main():
    # Input / Processing / Output
    try:
        contacts = os.listdir('contacts')
        if len(contacts):
            sign_in(contacts)
        else:
            print('No Contacts')
    except FileNotFoundError:
        print('No Contacts')

if __name__ == '__main__':
    main()