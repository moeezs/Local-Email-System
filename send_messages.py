'''
author : Moeez Shaikh
date : 1/16/2023
Makes the user sign in and allows it send messages to the other saved contacts
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
        list_contacts(contacts, username)


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


def list_contacts(contacts, username):
    '''Lists all the contacts that are in the database that you can send a message to
    
    Args :
        contacts - list[str] : this is the list of all the saved usernames (contacts) that are in the contacts folder
        username - str : the username that is inputted by the user
    '''

    sort_alpha(contacts)

    max_num_contacts = 0

    print('Choose the contact you want to send a message to : ')

    for i, contact in enumerate(contacts):
        print(f'{i + 1} - {contact}')
        max_num_contacts = max_num_contacts + 1
    
    chosen_contact = input('Enter the corresponding number : ')

    while chosen_contact.isnumeric() == False or int(chosen_contact) > max_num_contacts or int(chosen_contact) < 1:
        chosen_contact = input('Enter the corresponding number (in numbers) : ')

    chosen_contact = int(chosen_contact)


    send_message(contacts, chosen_contact, username)


def sort_alpha(contacts):
    '''This takes in the list contacts and sorts them alphabetically
    
    Args :
        contacts - list[str] : this is the list of all the saved usernames (contacts) that are in the contacts folder
    '''

    for i in range(len(contacts)):
        for j in range(len(contacts) - 1):
            if contacts[j] > contacts[j + 1]:
                contacts[j], contacts[j + 1] = contacts[j + 1], contacts[j]


def send_message(contacts, contact_num, username):
    '''Takes in the message and sends it to the chosen contact
    
    Args :
        contacts - list[str] : this is the list of all the saved usernames (contacts) that are in the contacts folder
        contact_num - int : this is the contact that was chosen by the sender to send a message to (receiver)
        username - str : the username that is inputted by the user
    '''

    message = input("Enter the message you want to send : ")
    reciever = contacts[contact_num - 1]

    try:
        os.mkdir(f'contacts/{reciever}/messages')
    except FileExistsError:
        pass
  
    with open(f'contacts/{reciever}/messages/message_{username}.txt', 'w') as f_out:
        f_out.write(f'{username} : {message}')

    print(f'Successfully sent the message "{message}" to {reciever} through {username}')


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