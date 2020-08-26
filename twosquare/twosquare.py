#!/usr/bin/env python3

"""An implementation of the two-square cipher.

This program encypts and decrypts messages using the two-square cipher,
aka double Playfair. There are two variations of the cipher, vertical
and horizontal, depending on how the two Playfair tables are arranged.
This implementation uses the first variation, so the two tables are
placed vertically.

The functionality of this program can also be used as a module.

"""

# globals
from typing import List
from typing import NoReturn
from typing import Union

# Use type aliases for type hints on complex types
Row = List[str]
Table = List[Row]

class FooBarError(Exception):
    """Raised when something really bad happens.

    """
    pass

class TypeMismatchError(TypeError):
    """Raised when someone tries to put a square peg in a round hole.

    """

    pass
    
class StakesTooHighError(IndexError):
    """Raised when the stakes are just too dang high!

    """

    pass 

class BadValueError(ValueError):
    """Raised when the value is flagrantly and absolutely invalid.

    """

    pass

def create_table(key: str) -> Union[Table, bool]: # return either Table or False
    """Create a Playfair table.

    Creates a Playfair table using the provided key. This table is a
    5 x 5 matrix that is used by the cipher to encrypt and decrypt
    messages.

    key must be a string in valid format. The validate_key()
    function can be used to verify that a key meets all necessary
    requirements prior to calling this function.
    
    Returns a valid populated table if successful or 
    prints a failure message and returns False if unsuccessful.

    """

    # set table size
    MAX_ROWS: int = 5
    MAX_COLUMNS: int = 5

    try:
        if type(key) is not str or key.isalpha() == False:
            raise ValueError('Invalid key format.')

        # capitalize all letters in the key
        key: str = key.upper()

        # create empty list for storage
        key_as_letters: list = [ ]

        # check for I and J in key and combine into single IJ letter
        for letter in key:         
            if letter == 'I' or letter == 'J':
                letter = 'IJ'
            key_as_letters.append(letter)

        # create full list of letters to track letters not in key
        alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"           
        letters_not_in_key: list = [ ]

        # combine I and J into IJ
        for letter in alphabet:
            if letter == 'J':
                letter = 'IJ'
                letters_not_in_key.remove('I')
            letters_not_in_key.append(letter)

        # remove key letters from list of letters not in key
        for letter in key_as_letters:
            if letter in letters_not_in_key:
                letters_not_in_key.remove(letter)

        # reverse the two lists for sake of efficiency when creating
        # the table below: linear time instead of quadratic for pops
        key_as_letters.reverse()
        letters_not_in_key.reverse()

        # create empty table
        table: list = [ ]

        # create and populate the table
        for row in range(MAX_ROWS):

            # create a new empty row
            this_row: list = [ ]

            # populate the new row with characters
            for column in range(MAX_COLUMNS):

                # use the key letters to populate the table
                if len(key_as_letters) > 0:
                    current_letter = key_as_letters.pop()

                # then fill table with remaining letters of alphabet
                else:
                    current_letter = letters_not_in_key.pop()

                # populate each cell with the current letter
                this_row.append(current_letter)

            # append new row to table
            table.append(this_row)

        return table

    except ValueError as err:
        print(err)
        return False

    except Exception as err:
        print('Unexpected exception type raised during execution.')
        print(type(err))
        print(err)
        raise

    return False

def encrypt(plaintext: str, key1: str, key2: str) -> str:
    return False

def decrypt(ciphertext: str, key1: str, key2: str) -> str:
    return False  

def display_table(table: Table) -> bool:
    """Print a Playfair table to the screen.

    Prints a Playfair table to the console for viewing purposes to
    facilitate development and testing.
    
    """

    try:
        if type(table) is not list:
            raise TypeError('Table must be a list.')

        if len(table) != 5:
            raise ValueError('Illegal number of rows in table.')

        print()

        # print each row of the table
        for row in table:

            if len(row) != 5:
                raise ValueError('Illegal number of columns in table row.')

            # print each cell in current row
            for cell in row:

                if type(cell) is not str or len(cell) > 2:
                    raise(ValueError('Bad table data.'))
                
                print('%6s' % cell, end='')

            # white space to separate rows
            print('\n\n')

    except ValueError as err:
        print(err)
        return False

    except TypeError as err:
        print(err)
        return False

    except Exception as err:
        from inspect import currentframe as cf
        print('Unexpected exception type raised during execution:')
        print(f'In function: {cf().f_code.co_name}') # function name
        print(type(err))
        print(err)
        raise

    else:
        return True

    return False

def get_key(ordinal: str = '') -> str:
    """Gets key from user and returns it.

    Prompts user for keyword or key phrase. Does not perform any
    validity checks of user input for proper key formatting
    restrictions, which is left to validate_key() function.

    The arg ordinal is optional string value for print formatting. If
    provided, it should be an ordinal number (e.g. - 'first', 'second').

    Returns the string value entered by the user.

    """

    if len(ordinal) > 0:
        ordinal += " "
        
    while not (key := input("Enter %skeyword or key phrase >> " % ordinal)):

        print("Invalid entry. Please try again.")

    return key

def get_mode() -> Union[str, bool]:
    """Gets program mode from user.

    Prompts user for program mode (encryption or decryption).

    Returns string value 'encrypt' or 'decrypt' based on user selection
    or returns False if user has made an invalid selection.
    """

    mode: str = input("Select mode: 1 for encrypt or 2 for decrypt >> ")

    if mode == '1':
        return 'encrypt'

    elif mode == '2':
        return 'decrypt'

    else:
        return False

def validate_key(key: str) -> bool:
    """Validates a key for a Playfair table.

    Takes a string as input and validates it against the formatting
    specifications of a keyword or key phrase for a Playfair table.

    Returns True if key passes all checks.
    Prints a failure message and returns False if key is invalid.

    """

    try:
        # check that key is a string
        if type(key) is not str:
            raise ValueError('Key must be a string.')

        # make sure key not empty - added this for use at module
        # level as main program already will not allow this
        if len(key) < 1:
            raise ValueError('Key must not be empty.')
                            
        key: str = key.upper()

        # make list to track which letters are in the key
        letters_in_key: list = [ ]

        for character in key:

            # check for white space
            if character.isspace():
                raise ValueError('Key cannot contain white space. ' +
                    'Only letters are allowed.')

            # check for digits
            if character.isdigit():
                raise ValueError('Key cannot contain digits. ' +
                    'Numbers must be spelled out.')

            # check for other forbidden characters
            if not character.isalpha():
                raise ValueError('Key cannot contain punctuation ' +
                    'or special characters.')

            # check for duplicate letters
            if character in letters_in_key:
                raise ValueError('Key must not contain duplicate letters.')

            # if character is a letter add it to the list to track it
            elif character.isalpha():
                letters_in_key.append(character)

        # make sure key does not contain more than twenty five letters
        if len(key) > 25:
            raise ValueError('Key cannot contain more than ' +
                'twenty-five characters.')
        
    except ValueError as err:
        print(err)
        return False

    except Exception as err:
        print('Unexpected exception type raised during execution.')
        print(type(err))
        print(err)
        raise

    else:
        return True
    
def __main__():
    """This is the main program.

    The functionality of this implementation can also be used as a module.
    """

    # display program title and brief description
    name: str = "twosquare"
    description: str = "encrypt and decrypt messages with the two-square cipher"
    print('{:^80}'.format('>> ' + name.upper() + ' <<'))
    print('{:^80}'.format(description.title()))

    # print bottom border that matches the length of the program description
    border_character: str = '-'
    border: str = border_character * len(description)
    print('{:^80}'.format(border))
    print()

    # prompt user for mode - encrypt or decrypt
    # get input until user chooses a valid selection
    while not (mode := get_mode()):
        print('Invalid selection. Please try again!')
      
    # prompt user for first key
    first_key: str = get_key('first')

    # validate key
    while not validate_key(first_key):
        first_key: str = get_key()

    # prompt user for second key
    second_key: str = get_key('second')

    # validate key
    while not validate_key(second_key):
        second_key: str = get_key()

    # create first table with first key
    first_table: Table = create_table(first_key) 

    # create second table with second key
    second_table: Table = create_table(second_key)

    # display the tables to the console for viewing - optional functionality

    print('\nHere are the Playfair tables generated with your keys:')
    
    print('\nTABLE ONE:')
    display_table(first_table)
    
    print('TABLE TWO:')
    display_table(second_table)

    text_prefix: str = 'plain' if mode == 'encrypt' else 'cipher'

    prompt: str = f'Enter {text_prefix}text to {mode}: '
    
    # prompt the user for message to encrypt / decrypt
    message = input(prompt)

    # perform encoding or decoding of message
    
    if mode == 'encrypt':
        message = encrypt(message, first_key, second_key)

    elif mode == 'decrypt':
        message = decrypt(message, first_key, second_key)

    else:
        raise Exception('Error: Invalid Mode.')

    ##### Progress marker #####

    # display success / failure message to confirm operation status

    # display (en/de)coded message    

    # OPTIONAL FUNCTIONALITY TO POSSIBLY IMPLEMENT LATER:

    # command-line usage

    # prompt user to accept or redo keys after table display

    # confirm message before (en/de)coding - e.g. - [P]roceed or [R]edo

    # get message text from file instead of keyboard

    # print out the modified text to the console 

    # prompt user to continue or quit

if __name__ == '__main__':
    __main__()
