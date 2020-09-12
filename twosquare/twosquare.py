#!/usr/bin/env python3

"""An implementation of the two-square cipher.

This program encypts and decrypts messages using the two-square cipher,
aka double Playfair. There are two variations of the cipher, vertical
and horizontal, depending on how the two Playfair tables are arranged.
This implementation uses the first variation, so the two tables are
placed vertically.

The functions in the global scope of this implementation can also be
used as a module.

""" 

# globals
from functools import partial

from typing import Callable
from typing import List
from typing import NoReturn
from typing import Tuple
from typing import Union

if __name__ == 'twosquare.twosquare':
    import_path = 'twosquare.exceptions'
    
else:
    import_path = 'exceptions' 

# user-defined error class names
custom_error_classes = [
    'BadValueError',
    'FooBarError',
    'StakesTooHighError',
    'TypeMismatchError',
    ]

# import the custom error classes from resolved path
for error_class in custom_error_classes:
    exec(f'from {import_path} import {error_class}') 

# Use type aliases for type hints on complex types
Row = List[str]
Table = List[Row]

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

    Dependencies:
        BadValueError

    """

    # set table size
    MAX_ROWS: int = 5
    MAX_COLUMNS: int = 5

    try:
        if type(key) is not str or key.isalpha() == False:
            raise BadValueError('Invalid key format.')

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

    except BadValueError as err:
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
        return table

def decrypt(ciphertext: str, key1: str, key2: str) -> str:
    """Decrypts a message using the Twosquare cipher.

    Dependencies:
        None

    TO BE IMPLEMENTED.

    """
    
    return False  

def display_table(table: Table) -> bool:
    """Print a Playfair table to the screen.

    Prints a Playfair table to the console for viewing purposes.
    
    Returns True if successful or False if an error occurs.

    Dependencies:

    from twosquare:
        BadValueError
        validate_table
    
    """

    try:

        if not validate_table(table):
            raise BadValueError('Table is invalid.')
        
        # print each row of the table
        for row in table:

            print(' ')

            # print each cell in current row
            for cell in row:
             
                print('%6s' % cell, end='')

            print('\n')

    except BadValueError as err:
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

def encode() -> NoReturn:
    """Encrypts or decrypts a message using the Twosquare cipher.

    Helper function for encrypt and decrypt functions.
    
    Will move and place any shared code for both operations here
    to avoid redundancy and to streamline the codebase.

    Dependencies:
        None

    TO BE IMPLEMENTED...

    """
    
    pass

def encrypt(plaintext: str, key1: str, key2: str) -> Union[str, bool]:
    """Encrypts a message using the Twosquare cipher.

    Encrypts a plaintext message using the two keys provided and returns
    the encoded ciphertext as a str if successful or returns False if
    operation is unsuccessful.

    Each key must be a valid keyword or key phrase:
    a non-empty string with no more than twenty-five letters
    no white space,
    no special characters,
    no digits - numbers must be spelled out,
    no duplicate letters (i.e. - the same letter cannot be used twice in
        the same key)

    The validate_key function can be used ahead of time to check the
    validity of each key.

    The value of plaintext must be a non-empty string. Please note the
    following: All white space, special characters, and digits will be
    removed from the plaintext during the encryption process. Basically,
    all non-alpha characters, while allowed, will be ignored and thus
    removed from the message. No data is stored about what was removed
    and therefore, when the ciphertext is later decrypted, the white
    space and punctuation will not be restored.

    Another thing to keep in mind is that 'I' and 'J' characters are
    combined into a single IJ letter by this cipher. While not ideal by
    any means, that is the way the cipher was designed. Hence, there
    can be some loss of information when the process is reversed and the
    ciphertext is decrypted back to a plaintext. In practicality, this
    makes little difference, as the decoded message is still typically
    easy to read and understand.

    If the number of characters in the plaintext is odd after removing
    all white space, special characters, and digits a Z is added to the
    end to make the number of characters even. This is necessary for
    the cipher to function properly, as the text is broken into digraphs
    (two-letter combinations) during the encoding or decoding process.
    This trailing character is, of course, easy enough to remove or
    simply to ignore when reading the decrypted message.

    For these reasons, among others, the Twosquare cipher is not a tool
    with practical use for encrypting and decrypting files and documents
    where a loss of data would be unacceptable, or where high levels of
    data security and integrity are essential. It is best used as a
    relatively simple means of sending English alphabetic messages and
    is perhaps valuable in real terms mainly for its historical
    significance and for educational purposes.

    Dependencies:
    
    from twosquare:
        BadValueError
        create_table
        # encode
        FooBarError
        get_coordinates        
        Row
        Table
        validate_key
        validate_plaintext    

    from typing:
        List

    """

    MAX_COLUMNS: int = 5
    MAX_ROWS: int = 5

    ciphertext: str = ''
    digraphs: list = [ ]
    letters_only: list = [ ]

    try:

        # validate keys
        if not (validate_key(key1) and validate_key(key2)):
            raise BadValueError('Invalid key error. I am the gatekeeper. ' + \
                                'Are you the keymaster?')

        # validate plaintext
        if not validate_plaintext(plaintext):
            raise BadValueError('Invalid plaintext error.')

        # capitalize all letters in plaintext
        capitalized: str = plaintext.upper()
        
        # filter to remove non-alpha characters
        for character in capitalized:
            if character.isalpha():
                letters_only.append(character)

        # if length of odd add 'Z' to end to make it even
        if len(letters_only) % 2 != 0:
            letters_only.append('Z')

        # get two letters at a time 
        for n in range(0, len(letters_only), 2):

            # create a digraph with the two letters
            current_digraph: list = [letters_only[n], letters_only[n+1]]

            # store the current digraph in the list of all digraphs
            digraphs.append(current_digraph)

        # create first table with first key
        first_table: Table = create_table(key1) 

        # create second table with second key
        second_table: Table = create_table(key2)

        # create ciphertext from plaintext using the tables
        for digraph in digraphs:

            # unpack digraph
            letter1, letter2 = digraph

            column1: int = -1
            column2: int = -1
            row1: int = -1
            row2: int = -1

            # get each letter's coordinates in its table (row, column)
            row1, column1 = get_coordinates(first_table, letter1)
            row2, column2 = get_coordinates(second_table, letter2)

            if min(row1, row2, column1, column2) < 0:
                
                raise FooBarError('Table mismatch error. Unable to find one' + \
                                  ' or more letters of the plaintext using' + \
                                  ' the tables generated during program .')

            # check to see which of two cases is true:
            # case 1: letters are in different columns - swap column numbers
            if column1 != column2:
                temp: int = column1
                column1 = column2
                column2 = temp

                # fetch letters from table using new coordinates
                encrypted_letter1 = first_table[row1][column1]
                encrypted_letter2 = second_table[row2][column2]

            # case 2: letters are in same column - leave letters as is
            else: # nope, that's not lazy, that's what the cipher says to do
                encrypted_letter1 = letter1
                encrypted_letter2 = letter2

            # add the two encrypted letters to the ciphertext body
            ciphertext = ciphertext + encrypted_letter1 + encrypted_letter2

    except BadValueError as err:
        print(err)
        return False

    except FooBarError as err:
        print(err)
        print(err.subtext)
        raise

    except Exception as err:
        from inspect import currentframe as cf
        print('Unexpected exception type raised during execution:')
        print(f'In function: {cf().f_code.co_name}') # function name
        print(type(err))
        print(err)
        raise

    else:
        return ciphertext

def get_coordinates(table: Table, letter: str) -> Tuple[int, int]:
    """Gets a letters coordinates from a Playfair table.

    Helper function for encrypt and decrypt functions.

    Letter should be a str containing a single ASCII letter character.
    Table must be prepopulated and have a valid format.
    
    Returns a tuple of two integers: (row_number, column_number) if
    successful or returns a a tuple of two integer values of (-1, -1)
    if unsuccessful.

    Dependencies:
        None
    
    """

    try:

        # create row counter
        row_number: int = 0

        if letter == 'I' or letter == 'J':
            letter = "IJ"

        # check each row of the table for the letter
        for row in table:
            
            # if the letter is found in current row
            if letter in row:
                
                # get the column number for the letter
                column_number: int = row.index(letter)

                # return the position of the letter in the table
                return (row_number, column_number)

            # if not found, increment the row counter for the next row
            row_number += 1

    except Exception as err:
        from inspect import currentframe as cf
        print('Unexpected exception type raised during execution:')
        print(f'In function: {cf().f_code.co_name}') # function name
        print(type(err))
        print(err)
        raise

    else:
        # if letter not found in table, return tuple with negative indices
        # to indicate that a non-fatal error has occured
        return (-1, -1)

def get_key(ordinal: str = '') -> str:
    """Gets key from user and returns it.

    Prompts user for keyword or key phrase. Does not perform any
    validity checks of user input for proper key formatting
    restrictions, which is left to validate_key() function.

    The arg ordinal is optional string value for print formatting. If
    provided, it should be an ordinal number (e.g. - 'first', 'second').

    Returns the string value entered by the user.

    Dependencies:
        None

    """

    try:
        if type(ordinal) is not str:
            raise TypeMismatchError('ordinal must be a string')

        if len(ordinal) > 0:
            ordinal += " "
            
        while not (key := input("Enter %skeyword or key phrase >> " % ordinal)):

            print("Invalid entry. Please try again.")

    except TypeMismatchError as err:
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
        return key

def validate_ciphertext(message: str) -> bool:
    """Validates a ciphertext message for the Twosquare cipher.
  
    To pass validation, a ciphertext message has these requirements:
    
    *Must be a non-empty string containing one or more alphabetic letters
    *English-language letters from the ASCII character set count
    *Punctuation and special characters are not allowed
    *Non-printable ASCII characters are not allowed
    *Unicode characters are not allowed
    *All letters must be capitalized
    *White space is not allowed
    *Digits are not allowed

    Returns True if message passes validation as ciphertext.
    Returns False if message fails validation or if an error occurs.

    Dependencies:

    From String:
        ascii_uppercase

    From Twosquare:
        BadValueError
        TypeMismatchError

    """

    from string import ascii_uppercase

    contains_a_letter: bool = False
    message_type: str = 'ciphertext'

    try:

        # validate type of message is str
        if type(message) is not str:
            raise TypeMismatchError(f'Error: {message_type} must be a ' + \
                                    'string. \nAre you trying to put a ' + \
                                    'square peg in a round hole?')

        # validate len of message is not zero
        if len(message) == 0:
            raise BadValueError(f'Error: {message_type} is empty. ' + \
                                'Into the void we fall...')

        # validate each character in the message
        for character in message:

            if not (character.isascii() and character.isprintable()):
                raise BadValueError(f'Only printable ASCII characters are ' + \
                                    'allowed in {message_type}.')

            if character.isspace():
                raise BadValueError('White space is not allowed in the ' + \
                                    f'{message_type}.')

            if character.isdigit():
                raise BadValueError('Digits are not allowed in the ' + \
                                    f'{message_type}.')
            
            if character in ascii_uppercase:
                contains_a_letter = True
                
            else:
                raise BadValueError('Only capitalized letters from the ' + \
                                    'ASCII character set are allowed.') 

        if contains_a_letter == False:
            raise BadValueError('Error: No alpha charcters in ' + \
                                f'{message_type}. Alas, symbolism is ' + \
                                'sensational,\nand punctuation is ' + \
                                'paramount, but letters are legendary!')        

    except BadValueError as err:
        print(err)
        return False

    except TypeMismatchError as err:
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

def validate_key(key: str) -> bool:
    """Validates a key for a Playfair table.

    Takes a string as input and validates it against the formatting
    specifications of a keyword or key phrase for a Playfair table.

    Returns True if key passes all checks.
    Prints a failure message and returns False if key is invalid.

    Dependencies:

    From twosquare:
        BadValueError
        TypeMismatchError

    """

    try:
        # check that key is a string
        if type(key) is not str:
            raise TypeMismatchError('Key must be a string.')

        # make sure key not empty - added this for use at module
        # level as main program already will not allow this
        if len(key) < 1:
            raise BadValueError('Key must not be empty.')
                            
        key: str = key.upper()

        # make list to track which letters are in the key
        letters_in_key: list = [ ]

        for character in key:

            # check for white space
            if character.isspace():
                raise BadValueError('Key cannot contain white space. ' +
                    'Only letters are allowed.')

            # check for digits
            if character.isdigit():
                raise BadValueError('Key cannot contain digits. ' +
                    'Numbers must be spelled out.')

            # check for other forbidden characters
            if not character.isalpha():
                raise BadValueError('Key cannot contain punctuation ' +
                    'or special characters.')

            # check for duplicate letters
            if character in letters_in_key:
                raise BadValueError('Key must not contain duplicate letters.')

            # if character is a letter add it to the list to track it
            elif character.isalpha():
                letters_in_key.append(character)

        # make sure key does not contain more than twenty five letters
        if len(key) > 25:
            raise BadValueError('Key cannot contain more than ' +
                'twenty-five characters.')
        
    except BadValueError as err:
        print(err)
        return False

    except TypeMismatchError as err:
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

def validate_message(message: str, mode: str = 'plain') -> bool:
    """Validates a message for the Twosquare cipher.

    Validates a plaintext or ciphertext message according to the 
    requirements and expected values of the Twosquare cipher.

    Value for message parameter should be a string containing the
    plaintext or ciphertext to be validated.

    Value for mode parameter should be a string indicating the type of
    message to validate.
    Value should be either 'plain' or 'p' for a plaintext message.
    Value should be either 'cipher' or 'c' for a ciphertext message.

    Calls validate_ciphertext or validate_plaintext based on value of
    mode.
    
    Returns the return value returned by the function called.
    The expected return values are:
    True if the message is valid.
    False if the message is invalid or if an error occurs.

    Dependencies:

    From string:
        printable        

    From twosquare:
        TypeMismatchError
        validate_ciphertext
        validate_plaintext

    """

    try:

        # validate type of message is str
        if type(message) is not str:
            raise TypeMismatchError(f'Error: message type must be a ' + \
                                    'string. \nAre you trying to put a ' + \
                                    'square peg in a round hole?')

        # call the appropriate function for the requested mode
        if mode in ['plain', 'p']:
            return validate_plaintext(message)

        elif mode in ['cipher', 'c']:
            return validate_ciphertext(message)

        else:
            raise BadValueError('Error: Invalid mode.')

    except BadValueError as err:
        print(err)
        return False

    except TypeMismatchError as err:
        print(err)
        return False

    except Exception as err:
        from inspect import currentframe as cf
        print('Unexpected exception type raised during execution:')
        print(f'In function: {cf().f_code.co_name}') # function name
        print(type(err))
        print(err)
        raise  

def validate_plaintext(message: str) -> bool:
    """Validates a plaintext message for the Twosquare cipher.

    Validates a plaintext according to the requirements and expected values
    of the Twosquare cipher.

    Returns True if the message is valid as a plaintext.
    Returns False if the message is invalid or if an error occurs.

    To pass validation, a plaintext message has these requirements:
    *Must be a non-empty string containing one or more alphabetic letters
    *English-language letters from the ASCII character set count
    *Unicode characters do not count and, while allowed, will be ignored
    *Digits are allowed, but will be ignored. Numbers can be spelled out
    *Punctuation and special characters are allowed, but are ignored
    *Non-printable ASCII characters are not allowed
    *White space is allowed, but will be ignored

    Dependencies:

    From string:
        printable        

    From twosquare:
        BadValueError
        TypeMismatchError


    ONE SEEMINGLY LOGICAL GENERAL APPROACH TO VALIDATION:
        From greatest violations of requirements to least violations
        Perhaps review all validation functions and sections against this order
    
    """

    from string import printable

    message_type: str = 'plaintext'
    printable_chars: str = printable

    try:

        # validate type of message is str
        if type(message) is not str:
            raise TypeMismatchError(f'Error: {message_type} must be a ' + \
                                    'string. \nAre you trying to put a ' + \
                                    'square peg in a round hole?')

        # validate len of message is not zero
        if len(message) == 0:
            raise BadValueError(f'Error: {message_type} is empty. ' + \
                                'Into the void we fall...')

        # validate that message not merely white space or numeric
        if message.isspace() or message.isnumeric():
            raise BadValueError(f'Error: {message_type} must contain at ' + \
                                'least some letters.\nTell me a joke or ' + \
                                'something.')

        # validate that message is only printable ASCII characters
        # or perhaps just ignore them instead???
        if not message.isascii():
            raise BadValueError(f'Error: {message_type} can consist of ' + \
                                'ASCII characters only.\n')

        contains_a_letter: bool = False

        # check for non-printable characters
        for character in message:
            if character not in printable_chars:
                raise BadValueError(f'Error: {message_type} cannot contain ' + \
                                    'non-printable characters.')
            
            # make sure message contains at least one letter
            if character.isalpha():
                contains_a_letter = True

        if contains_a_letter == False:
            raise BadValueError('Error: No letters present in the ' + \
                                '{message_type}. Alas, symbolism is ' + \
                                'sensational,\nand punctuation is paramount' + \
                                ', but letters are legendary!')        

    except BadValueError as err:
        print(err)
        return False

    except TypeMismatchError as err:
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
   
def validate_table(table: Table) -> bool:
    """Validates a Playfair table.

    Returns True if the table is valid or returns False otherwise.

    Dependencies:
        None

    """

    letters_in_table = [ ]
    letter_count = 0

    try:
        if type(table) is not list:
            raise TypeMismatchError('Table must be a list.')

        if len(table) != 5:
            raise BadValueError('Illegal number of rows in table.')        

        # check each row of the table
        for row in table:

            if len(row) != 5:
                raise BadValueError('Illegal number of columns in table row.')

            # check each cell in current row
            for cell in row:
                if type(cell) is not str or len(cell) > 2:
                    raise(BadValueError('Bad table data.'))

                if not (cell.isascii() and cell.isprintable()):
                    raise(BadValueError('Table contains illegal characters.'))

                if not (cell.isalpha() and cell.isupper()):
                    raise(BadValueError('Invalid characters in table.'))

                if cell in letters_in_table:
                    raise(BadValueError('Table contains duplicate letters.'))

                letters_in_table.append(cell)   

                letter_count += len(cell)

                if letter_count > 26:
                    raise(ValueError('Table contains more than 26 letters.'))
                
    except BadValueError as err:
        print(err)
        print(err.subtext)
        return False

    except TypeMismatchError as err:
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

def __main__():
    """This is the main program.

    The other functions in the global scope of this implementation can also
    be imported and used as a module.
    
    """

    # inner functions for main program only - not for use as module

    def _coming_soon() -> NoReturn:
        """Prints a message indicating that a program's feature is coming soon.

        Inner helper function for the main twosquare program.

        """

        print('\nThat feature is coming soon...')

        return True

    def _create_key(key_list: List[str], ordinal: List[str], \
         index: int, action: str = 'create') -> NoReturn:

        try:

            # prompt user for a key      
            key: str = get_key(ordinal[index])

            # validate key and get again if not valid
            while not validate_key(key):
                key: str = get_key()

            # replace existing key with new key value
            key_list.pop(index)
            key_list.insert(index, key.lower())

        except Exception as err:
            print(f'An error occurred. Unable to {action} key.')
            print(err)

        else:
            # confirm that key was created successfully
            print(f'\nKey {action}d successfully.')

        return

    def _display_keys() -> NoReturn:
        """Displays the current keys, if any.

        Inner helper function for the main twosquare program.

        """
    
        print('\nHere are your current keys: \n')

        for key_number, key in enumerate(keys, start = 1):

            if len(key) == 0:
                key = '[None]'
            
            print(f'KEY {key_number}: {key}')

        return

    def _display_menu(menu_options: list) -> Union[int, bool]:
        """Print a formatted list of program options.

        Inner helper function for the main twosquare program.

        Returns number of menu_options in list if successful
        or returns False if an exception occurs. Keep this in mind,
        and handle potential Exceptions accordingly.

        """

        try:   

            for number, option in enumerate(menu_options, start = 0):
                print('{:56}'.format('\t    ***            ' + str(number) + ': ' \
                                     + option.upper()) + ' ***\t')
                
            print(' ')

        except Exception as err:
            print('Unable to print program menu. ' +
                  'An unexpected error has occured.')
            print(err)
            print(type(err))
            
            return False

        else:
            return number # total number of items (also highest index)

    def _display_title(title: str, byline: str, border_character: str = '-') \
            -> NoReturn:
        """Displays a pretty formatted title and byline.

        Inner helper function for the main twosquare program.

        TODOs: Ideas for additional features:

        Add keyword arg for text_alignment with default = 'center'

        """
        
        print('{:^80}'.format('>> ' + title.upper() + ' <<'))
        print('{:^80}'.format(byline.title()))

        # print bottom border that matches the length of the byline
        border: str = border_character * len(byline)
        print('{:^80}'.format(border))
        print()

        return

    def _get_response(action: str) -> bool:
        """Gets a yes or no response from the user.

        Inner helper function for the main twosquare program.

        Prompts the user for input.

        The input validation only accepts [upper/lower]case variants of 'Y'
        and 'N'.

        Returns True if user selects 'Y'
        Returns False if user selects 'N'
        
        Example use case: to check whether or not the user wants to perform
        another action in a loop or exit (to main menu / quit program, etc.).

        """
    
        while True:
            
            try:
                response = input(f'\n{action}? (Y/N)? >> ').upper()

                if response == 'Y':
                    return True
                
                elif response == 'N':
                    return False

                else:
                    raise
            
            except:
                print('Invalid selection. Please try again.')

    def _get_selection(options: List[str],
                       header: str = 'Select an option:',
                       list_item_character = '*',
                       prompt: str = 'Enter selection >> ',
                       error_message:  str = 'Invalid selection. ' + \
                           'Please try again.') -> int:
        """Prompts the user to make a selection from a list of options.

        Returns an int corresponding to the index of the options list item
        selected by the user if successful.
        Returns an int value of -1 if an expected error occurs during
        execution.

        Dependencies:

        From twosquare:
        #BadValueError
        TypeMismatchError

        """

        valid_choices: List[str]

        try:

            if type(options) is not list:
                raise TypeMismatchError('Error: options must be a list.')

            for item in options:
                if type(item) is not str:
                    raise TypeMismatchError('Error: all items in options ' + \
                                            'list must be strings.')

            if type(header) is not str:
                raise TypeMismatchError('Error: header must be a string.')

            if type(list_item_character) is not str:
                raise TypeMismatchError('Error: list_item_character ' + \
                                        'must be a string.')

            if type(prompt) is not str:
                raise TypeMismatchError('Error: prompt must be a string.')

            if type(error_message) is not str:
                raise TypeMismatchError('Error: error_message must be ' + \
                                        'a string.')

            # print header
            print(f'n\{header}')

            # print a menu of the options
            for number, item in enumerate(options, start = 1):

                print(f'{list_item_character}{number}: {item}')

                # keep track of valid choices
                valid_choices.append(str(number))            

            # get a valid selection from the user
            while True:
                selection = input(f'\n{prompt}')

                if selection in valid_choices:
                    
                    # return options list index corresponding to user's selection
                    return int(selection) - 1

                else:
                    print(error_message)

        except TypeMismatchError as err:
            print(err)
            return -1

        except Exception as err:
            from inspect import currentframe as cf
            print('Unexpected exception type raised during execution:')
            print(f'In function: {cf().f_code.co_name}') # function name
            print(type(err))
            print(err)
            raise

    def _load_file(filename: str = '') -> Union[str, bool]:
        """Loads a message from a .txt file.

        Loads a plaintext or ciphertext message. Only .txt files are supported.

        Helper function for main Twosquare program.

        Parameter for filename, if included, must be a string representing a  
        valid filename for a file in the current directory, and must include
        the .txt file type extension in the name. If a filename is not
        included, this function will prompt the user for a filename.

        No validation is made for the contents of the file loaded. That is left
        to the validate_message function.

        Returns the message if successful.
        Returns false if an error occurs.

        REFACTOR _LOAD_FILE TODOs:
        -------------------------

        *FIX FOR WHEN FILENAME IS INCLUDED AS PARAMETER VALUE
        *Use menu helper function to reduce excessive indentation
        *Replace abort code with -1 int value like in _save_file function        
        

        """
       
        try:
            if type(filename) is not str:
                raise TypeMismatchError('Filename must be a string.')

            if len(filename) > 0 and filename.endswith('.txt') is False:
                raise BadValueError('File must be a .txt file.')

            # SKIP THIS FILENAME ENTRY FOR FILENAME INCLUDED

            while filename == '':
                
                # prompt user for filename  
                print('Enter filename below and include the .txt extension.' + \
                      '\nThe file must be in the current directory.\n' + \
                      'Leave the field blank and ' + \
                      'hit <enter> to abort.\n')
                
                while not (filename := input('Enter filename >> ')):

                    # if user leaves blank return abort code
                    if filename == '':
                        return '`->!ABORT!<-`'
                      
                    print('Invalid filename. Please try again.')

                if not filename.endswith('.txt'):
                    
                    print('\nOnly .txt file types are supported. Please ' + \
                          'try again.\n')

                    # reset filename 
                    filename = ''

                    # go back and get it again
                    continue

           


##                # confirm file name - [P]roceed [R]etype or [A]bort            
##                header: str = f'\nConfirm filename: {filename}'
##
##                options: List[str} = [
##                    'Proceed',
##                    'Redo',
##                    'Abort',
##                    ]
##
##                choice = _get_selection(options, header)



                # confirm file name - [P]roceed [R]etype or [A]bort
                print(f'\nConfirm filename: {filename}')

                print('1: Proceed')
                print('2: Redo')
                print('3: Abort')

                loop_get_choice: bool = True

                while loop_get_choice:

                    choice: str = input('\nEnter selection >> ')

                    if choice == '1': # proceed

                        # ENTRY POINT FOR COMMAND LINE WHEN FILENAME INCLUDED

                        loop_load_file: bool = True

                        while loop_load_file:

                            print('\nLoading file...', end = '')

                            message: str = ''

                            # perform file operation
                            try:

                                with open(filename, mode = 'r') as file:
                             
                                    while line := file.readline():

                                        message += line                                        
                                      
                                if message:

                                    print('Completed.')
                                    
                                    return message

                                else:
                                    print('Failed.\n')
                                          
                                    raise Exception(f'\nCould not load ' + \
                                                    f'{filename}')

                            except Exception as err:

                                # if file not found or other problem notify user
                                print(' ')
                                print(err)
                                print(type(err))

                                print(' ')
                                print('What would you like to do?\n')
                                print('1: Retry filename')
                                print('2: Re-enter filename')
                                print('3: Abort')

                                while True:

                                    recourse: str = input('\nEnter ' + \
                                                          'selection >> ')

                                    if recourse == '1': # retry same filename

##                                        print(' ')

                                        # return to beginning of file operation
                                        loop_get_choice = False
                                        break

                                    elif recourse == '2': # re-enter filename

                                        print(' ')

                                        # reset filename
                                        filename = ''

                                        # return to beginning of filename entry
                                        loop_get_choice = False
                                        loop_load_file = False
                                        break

                                    elif recourse == '3': # abort

                                        return '`->!ABORT!<-`' # UNLESS COMMAND LINE

                                    else:
                                        print('Invalid selection. Please ' + \
                                              'try again.')
                                    
                    elif choice == '2': # redo
                        
                        print('\nRedoing...\n')

                        # reset filename as blank
                        filename = ''

                        # go up one level to get file name again
                        break
                        
                    elif choice == '3': # abort

                        print('\nAborting...\n')
                        
                        return '`->!ABORT!<-`' # UNLESS COMMAND LINE

                    else:
                        print('Invalid response. Please try again.')

        except BadValueError as err:
            print(err)
            return False

        except TypeMismatchError as err:
            print(err)
            return False

        except Exception as err:
            print('Unable to load from file. ' +
                  'An unexpected error has occured.')
            print(err)
            print(type(err))
            
            return False

    def _save_file(filename: str = '', message: str = '') -> int:
        """Saves a message as a .txt file.

        Returns an int value of 1 if message saved as file successfully.
        Returns an int value of 0 if unsuccessful.
        Returns an int value of -1 if user aborts operation.

        """

        from os.path import exists

        try:
            if type(filename) is not str:
                raise TypeMismatchError('Filename must be a string.')

            if type(message) is not str:
                raise TypeMismatchError('Message must be a string.')            

            if len(filename) > 0 and filename.endswith('.txt') is False:
                raise BadValueError('File must be a .txt file.')

            if len(message) == 0:
                raise BadValueError('Message cannot be empty.')
            

            # PRINT MESSAGE ABOUT SUPPORTED FILE TYPES AND RESTRICTIONS
                # DO IT HERE INSTEAD OF IN MAIN PROGRAM MENUS ???
            

            # SKIP THIS FILENAME ENTRY FOR FILENAME INCLUDED

            while filename == '':
                
                # prompt user for filename  
                print('Enter filename below and include the .txt extension.' + \
                      '\nThe file will be saved in the current directory ' + \
                      'and cannot already exist.\nLeave the field blank and ' + \
                      'hit <enter> to abort.\n')
                
                while not (filename := input('Enter filename >> ')):

                    # if user leaves blank return abort code
                    if filename == '':
                        return -1
                      
                    print('Invalid filename. Please try again.')

                if not filename.endswith('.txt'):
                    
                    print('\nOnly .txt file types are supported. Please ' + \
                          'try again.\n')

                    # reset filename 
                    filename = ''

                    # go back and get it again
                    continue

                # confirm file name - [P]roceed [R]etype or [A]bort
                print(f'\nConfirm filename: {filename}')

                print('1: Proceed')
                print('2: Redo')
                print('3: Abort')

                loop_get_choice: bool = True

                while loop_get_choice:

                    choice: str = input('\nEnter selection >> ')

                    if choice == '1': # proceed

                        # ENTRY POINT FOR COMMAND LINE WHEN FILENAME INCLUDED

                        loop_save_file: bool = True

                        while loop_save_file:

                            print('\nSaving file...', end = '')

                            # perform file operation
                            try:

                                # check to see if file already exists
                                if exists(filename):
                                    
                                    raise BadValueError('A file with that ' + \
                                                        'name already exists.')

                                # proceed with operation
                                with open(filename, mode = 'w') as file:
                                    chars_written: int = file.write(message)

                                if chars_written == len(message):
                                    
                                    print('Completed.')
                                    
                                    return 1

                                else:
                                    print('Failed.')
                                          
                                    raise Exception(f'Could not save ' + \
                                                    f'{filename}')

                            except Exception as err:

                                # if file exists or other problem notify user
                                print(' ')
                                print(err)
                                print(type(err))

                                print(' ')
                                print('What would you like to do?\n')
                                print('1: Retry filename')
                                print('2: Re-enter filename')
                                print('3: Abort')

                                while True:

                                    recourse: str = input('\nEnter ' + \
                                                          'selection >> ')

                                    if recourse == '1': # retry same filename

                                        # return to beginning of file operation
                                        loop_get_choice = False
                                        break

                                    elif recourse == '2': # re-enter filename

                                        print(' ')

                                        # reset filename
                                        filename = ''

                                        # return to beginning of filename entry
                                        loop_get_choice = False
                                        loop_save_file = False
                                        break

                                    elif recourse == '3': # abort

                                        return -1

                                    else:
                                        print('Invalid selection. Please ' + \
                                              'try again.')
                                    
                    elif choice == '2': # redo
                        
                        print('\nRedoing...\n')

                        # reset filename as blank
                        filename = ''

                        # go up one level to get file name again
                        break
                        
                    elif choice == '3': # abort

                        print('\nAborting...\n')
                        
                        return -1

                    else:
                        print('Invalid response. Please try again.')
        
        except BadValueError as err:
            print(err)
            return 0

        except TypeMismatchError as err:
            print(err)
            return 0

        except Exception as err:
            print('Unable to save file. ' +
                  'An unexpected error has occured.')
            print(err)
            print(type(err))
            
            return 0            

    exit_program: bool = False
    info_ciphertext: List[str] = [
        'To pass validation, a ciphertext message has these requirements:\n',
        '*Must be a non-empty string containing one or more alphabetic letters',
        '*English-language letters from the ASCII character set count',
        '*Punctuation and special characters are not allowed',
        '*Non-printable ASCII characters are not allowed',
        '*Unicode characters are not allowed',
        '*All letters must be capitalized',
        '*White space is not allowed',
        '*Digits are not allowed',
        ]
    info_file_types: List[str] = [
        'This implementation enables loading and saving messages as .txt ',
        'files. This is the only file type supported and files will not be',
        'encrypted in place, that is to say, they will not be overwritten.',
        'The reason for these restrictions is that the Twosquare cipher is',
        'not suitable for encrypting all types of data or file, but rather ',
        'only works with alphabetic ASCII character sets. The encoding ',
        'process omits white space, digits, punctuation, special characters,',
        'and other valuable data and thus is not suitable for general usage.',
        'The file capabilities are provided merely to facilitate the storage',
        'and transfer of messages at the personal discretion of the user.',
        'Professional use is discouraged. No guarantee is made that the data',
        'will be secure, and no warranty is made against the possibility of ',
        'data loss or corruption. Use at your own risk.',
        ]
    info_plaintext: List[str] = [
        'To pass validation, a plaintext message has these requirements:\n',
        '*Must be a non-empty string containing one or more alphabetic letters',
        '*English-language letters from the ASCII character set count',
        '*Unicode characters do not count and, while allowed, will be ignored',
        '*Digits are allowed, but will be ignored. Numbers can be spelled out',
        '*Punctuation and special characters are allowed, but are ignored',
        '*Non-printable ASCII characters are not allowed',
        '*White space is allowed, but will be ignored',
        ]
    loop_main: bool = True
    key_description: List[str] = [
        'The Twosquare cipher uses two keys to encrypt and decrypt messages.',
        ' ',
        '>Each key can be a key word or phrase:',
        '* Up to twenty-five letters in length',
        '* Each letter may not be used more than once in a key',
        '* Digits are not allowed so all numbers must be spelled out',
        '* No white space, punctuation, or special characters',
        ]
    keys: Union[List[str], bool] = ['', '']
    menu_options: List[str] = [
        'Display options menu',
        'Encrypt a plaintext',
        'Decrypt a ciphertext',
        'Create a new key',
        'Display current keys',
        'Display current tables',
        'Validate a key',
        'Validate a message',
        'About this program',
        'Exit program',
        ]
    more_info: List[List[str]] = [
        [
        'When encrypting a plaintext message, please note the ',
        'following: All white space, punctuation, special characters,',
        'and digits will be removed from the plaintext during the ',
        'encryption process. In basic terms, all non-alpha characters,',
        'while allowed, will be ignored and thus removed from the ',
        'message. No data is stored about what was removed and ',
        'therefore, when the ciphertext is later decrypted, the white',
        'space, digits, and punctuation will not be restored.',
        ' ',
        ],
        [
        "Another thing to keep in mind is that 'I' and 'J' characters ",
        'are combined into a single IJ letter by this cipher. While ',
        'not ideal by any means, that is the way the cipher was ',
        'designed. Hence, there can be some loss of information when ',
        'the process is reversed and the ciphertext is decrypted back ',
        'to a plaintext. In practicality, this makes little ',
        'difference, as the decoded message is still typically easy to ',
        'read and understand.',
        ' ',
        ],
        [
        'If the number of characters in the plaintext is odd after ',
        'removing all white space, special characters, and digits, a ',
        "'Z' character is added to the end to make the number of ",
        'characters even. This is necessary for the cipher to function',
        'properly, as the text is broken into digraphs (two-letter ',
        'combinations) during the encoding or decoding process. This',
        'trailing character is, of course, easy enough to remove or ',
        'simply to ignore when reading the decrypted message.',
        ' ',
        ],
        [
        'For these reasons, among others, the Twosquare cipher is not',
        'a tool with practical use for encrypting and decrypting files',
        'and documents where a loss of data would be unacceptable, or ',
        'where high levels of data security and integrity are ',
        'essential. It is best used as a relatively simple means of ',
        'sending English alphabetic messages and is perhaps valuable ',
        'in real terms mainly for its historical significance and for ',
        'educational purposes.',
        ],
        ]
    ordinal: List[str] = ['first', 'second']
    program_name: str = "twosquare"
    program_description: str = \
        "encrypt and decrypt messages with the two-square cipher"
    return_to_main_menu: bool = False
    table_description: List[str] = [
        'The Twosquare cipher uses two 5 x 5 Playfair tables to',
        'encrypt and decrypt messages for you. These two tables',
        'are each generated using one of the keys you create.',
        ]
    tables: Union[Table, bool] = [[''], ['']] # SET HINT AS TABLE OR LIST???

    ##### PROGRAM START #####

    ##### ADD TRY EXCEPT BLOCKS TO MAIN PROGRAM TO HANDLE ERRORS GRACEFULLY ###

    # display program title
    _display_title(program_name, program_description)

    # display menu of program options
    number = _display_menu(menu_options)

    # main program loop
    while loop_main:

        while True:
            try:
                selection = int(input('Enter selection number >> '))
                
                if selection < 0 or selection > number:
                    raise ValueError

            except:
                print('Invalid selection. Please try again.')

            else:
                break

        print(f'\n*** {menu_options[selection].upper()} ***')

        # handle the user's selection
      
        if selection == 0: # display options menu
            print(' ')
            
            _display_title(program_name, program_description)
            
            _display_menu(menu_options)

        elif selection == 1 or selection == 2: # [en/de]crypt a text

            code_prefix: str = 'en' if selection == 1 else 'de'
            loop_encode: bool = True
            mode: str = 'encrypt' if selection == 1 else 'decrypt'
            return_to_loop_encode: bool = False
            text_prefix: str = 'plain' if selection == 1 else 'cipher'

            while loop_encode:

                print(' ')

                try:

                    # if not enough keys exist, notify user
                    if min(len(keys[0]), len(keys[1])) == 0:
                        ending = 'your keys' if keys[0] == '' else 'another key'

                        print(f'{mode.title()}ion requires two keys. Please ' + \
                              f'create {ending} first.')

                        # return to main menu
                        break

                    # print a brief description of process and requirements
                    # give option for more detailed information
                    for index in range(3):
                        for line in more_info[index]:
                            print(line)

                    # prompt user for input method (manual / file)
                    print(f'Select {text_prefix}text source:\n')
                    print('1: Manual entry')
                    print('2: From file')
                    print('3: Main menu\n')

                    loop_get_message: bool = True
                    
                    while loop_get_message:
                        
                        method: str = input('Enter selection: ')

                        if method == '1': # manual entry

                            print(' ')
                            
                            # prompt the user for message to encrypt / decrypt
                            prompt: str = f'Enter {text_prefix}text to {mode}: '
                            message: str = input(prompt)

                            # validate message format and get again until valid
                            while not (message_is_valid := \
                                       validate_message(message)):
                                
                                print(' ')
                                
                                message: str = input(prompt)
                            
                            break                        

                        elif method == '2': # from file

                            print(' ')

                            # display info about file types                      
                            for line in info_file_types:
                                print(line)

                            print(' ')

                            if not (message := _load_file()):
                                
                                break # raise error here or return to menu???

                            if message == '`->!ABORT!<-`': # abort code

                                # return to [en/de]crypt menu
                                loop_get_message = False
                                break

                            if not (message_is_valid := \
                                    validate_message(message)):
                                
                                print(' ')
                                
                                raise BadValueError('Loaded message fails ' + \
                                                    'validation check.')
                            
                            # if message loaded and validated, break and proceed
                            break


                        elif method == '3': # return to main menu
                            
                            return_to_main_menu = True
                            break

                        else:
                            print('Invalid method selection. Please try again.')

                    if return_to_main_menu:                   
                        return_to_main_menu = False
                        break

                    if message == '`->!ABORT!<-`': # abort code

                            # return to [en/de]crypt menu
                            continue
              
                    # prepare to perform encoding or decoding of message  
                    # choose function to call depending on selected mode
                    func: Callable[[str, str, str], Union[str, bool]] = \
                        encrypt if mode == 'encrypt' else decrypt

                    # plug appropriate function into callable partial with args
                    action: Callable[[ ], str] = partial(func, message, \
                                                         keys[0], keys[1])

                    # call function to perform [en/de]cryption
                    # and get processed_text
                    processed_text: str = action()            

                    # report operation success / failure
                    if processed_text:
                        print('\nOperation succcessful.')

                    # include else
                        # raise 

                    display_message_actions: bool = True
                    
                    while display_message_actions:

                        # if successful, ask user what would like to do
                        print('What would you like to do?\n')
                        print('1: View message')
                        print('2: Save message')
                        print(f'3: {code_prefix.title()}crypt another message.') 
                        print('4: Exit to main menu\n')

                        # get selection for message action

                        loop_get_message_action: bool = True
                        
                        while loop_get_message_action:
                            
                            method: str = input('Enter selection: ')

                            if method == '1': # view message

                                print(f'\nHere is the {code_prefix}coded ' + \
                                      'message:\n')

                                print(processed_text)
                                
                                print(' ')
                                
                                # break from loop_get_message_action
                                # and print actions menu again
                                break

                            elif method == '2': # save file

                                print(' ')

                                # display info about file types                      
                                for line in info_file_types:
                                    print(line)

                                print(' ')

                                filename: str = ''

                                save_status: int = \
                                    _save_file(filename, processed_text)

                                if save_status == 1:
                                    print('File write successful. ' + \
                                          'Message saved.')
                                                                        
                                elif save_status == 0:
                                    print('File write failed.\n')
                                    
                                elif save_status == -1:
                                    print('File write aborted.\n')
                                    
                                else:
                                    raise('File write error.\n')

                                # break and return to message actions menu
                                break

                            elif method == '3': # [en/de]crypt another message

                                # break and return to encode menu:
                                return_to_loop_encode = True
                                break 

                            elif method == '4': # return to main menu

                                # up three levels:
                                return_to_main_menu = True
                                return_to_loop_encode = True
                                break                               

                            else:
                                print('Invalid method selection. Please try ' + \
                                      'again.')

                        if return_to_loop_encode:
                            break

                    if return_to_main_menu:
                        
                        break

                    if return_to_loop_encode:
                        
                        return_to_loop_encode = False

                        continue

                except BadValueError as err:
                    print('\nUnable to complete operation.')
                    print(err)

                except FooBarError as err:
                    print('\nUnable to complete operation.')
                    print(err)
                    print(type(err))
                    print(err.subtext)
                    
                except Exception as err:
                    print('\nUnable to complete operation.')
                    print('\nAn unexpected error occurred.')
                    print(err)
                    print(type(err))
                    raise

                if return_to_main_menu:
                    
                    return_to_main_menu = False
                    
                    break  
            
                # build prompt string with appropriate type of action
                prompt: str = f'{mode.title()} another {text_prefix}text'

                # ask user if they would like to continue or exit
                loop_encode: bool = _get_response(prompt)

        elif selection == 3: # create a new key

            loop_create_key: bool = True

            while loop_create_key:

                print(' ')

                # print description of key requirements
                for line in key_description:
                    print(line)
  
                # display current keys, if any
                _display_keys()

                print('')
                
                # check for empty key slot to set as target for new key
                target: int = 0 if len(keys[0]) <= len(keys[1]) else 1

                if len(keys[target]) == 0:

                    _create_key(keys, ordinal, target)

                # if both slots already contain keys, ask user which key they
                # want to replace or give option to abort and keep current keys
                else:  
                    print('Which key would you like to replace: (1 or 2)?')
                    print('Enter 0 to abort and return to main menu.')

                    loop_replace_key: bool = True
                    
                    while loop_replace_key:
                        choice: str = input('Select key >> ')

                        if choice == '0':
                            print('\nKey replacement aborted. No changes made.')

                            # end current loop and return to main menu
                            loop_replace_key = False   # up one level
                            return_to_main_menu = True # up two levels
                        
                        elif choice == '1' or choice == '2':
                            print(f'\nOkay, replace key {choice}...')

                            # adjust for target list index for keys and ordinal
                            index: int = int(choice) - 1
                            
                            _create_key(keys, ordinal, index, 'replace')
                            
                            loop_replace_key = False
                           
                        else:
                            print('Invalid selection. Please try again.')               

                if return_to_main_menu:
                    
                    # set flag back to False and break to main menu loop
                    return_to_main_menu = False
                    
                    break
                
                # display updated keys
                _display_keys()

                # build prompt string with appropriate type of action
                action: str = 'Create' if min(len(keys[0]), len(keys[1])) == 0 \
                    else 'Update'

                action += ' another key'

                # ask user if they would like to create another key
                loop_create_key: bool = _get_response(action)

        elif selection == 4: # display current keys
            
            # list all current keys or 'None' if none exist            
            _display_keys()

        elif selection == 5: # display current tables

            print(' ')
            
            for line in table_description:
                print(line)               

            if len(keys[0]) == 0:
                print('\nYou have not created any keys yet so')
                print('no tables can be generated using them.\n')

                fill_type: str = ''

            else:
                print('\nHere are the tables generated with your keys:')
                
                fill_type: str = '\n'

            # display all current tables or 'None' if none exist
            for table_number in range(1,3):
                print(f'{fill_type}TABLE {table_number}: ', end = '')
            
                # adjust for target list index for keys and tables
                index: int = table_number - 1

                # check to see if key exists, and if so...
                if len(keys[index]) > 0:

                    print('\n')

                    # create a table with existing key and
                    # replace the current table at that index, if any
                    tables.pop(index)
                    tables.insert(index, create_table(keys[index]))

                    # display the table
                    display_table(tables[index])
                    
                else:
                    print('[None]')

        elif selection == 6: # validate a key

            while True:

                # print description of key requirements
                for line in key_description:
                    print(line)

                print('\nIf you want to check to see if a key meets ' + \
                      'these requirements,')
                print('you may enter it below. Empty <enter> to abort.\n')

                # get key from user
                test_key: str = input('Enter key >> ')
                
                # run validation check on key
                if len(test_key) > 0:

                    print(' ')
                    
                    key_is_valid: bool = validate_key(test_key)

                    # report test results
                    if key_is_valid:
                        print('Key passes validation check.')

                    else:
                        print('Key fails validation check.')

               # abort if user left field blank and hit enter
                else:
                    
                    break
               
                # ask user if they would like to validate another key
                validate_another: bool = _get_response('Validate another key')

                # if not, break and return to main menu
                if not validate_another:

                    break

        elif selection == 7: # validate a message

            loop_validate_message: bool = True

            while loop_validate_message:

                try:
         
                    print('\nSelect message type:')
                    print('1: Plaintext')
                    print('2: Ciphertext')
                    print('3: Main menu\n')

                    while True:

                        choice: str = input('Enter selection >> ')

                        if choice in ['1', '2']: # plaintext or ciphertext

                            choice = int(choice)
                            break
                           
                        elif choice == '3': # return to main menu
                            return_to_main_menu = True
                            break

                        else:
                            print('Invalid selection. Please try again.')

                    if return_to_main_menu:
                        break

                    code_prefix: str = 'en' if choice == 1 else 'de'
                    info_message: List[str] = info_plaintext if choice == 1 \
                        else info_ciphertext
                    loop_print_message: bool = True
                    mode: str = 'encrypt' if choice == 1 else 'decrypt'

                    return_to_loop_print_message: bool = False
                    text_prefix: str = 'plain' if choice == 1 else 'cipher'

                    while loop_print_message:

                        message_type: str = ''

                        print(f'\nOkay, {text_prefix}text...')

                        print(' ')

                        # print out brief description of message requirements
                        for line in info_message:
                            print(line)

                        print(' ')                  

                        # prompt user for input method (manual / file)
                        print(f'Select {text_prefix}text source:\n')
                        print('1: Manual entry')
                        print('2: From file')
                        print('3: Main menu\n')

                        loop_get_message: bool = True
                        
                        while loop_get_message:
                            
                            method: str = input('Enter selection: ')

                            if method == '1': # manual entry

                                print(' ')
                                
                                # prompt the user for message
                                prompt: str = f'Enter {text_prefix}text to ' + \
                                              f'validate: '
                                message: str = input(prompt)

                                loop_get_message = False
                                loop_print_message = False
                                break                        

                            elif method == '2': # from file

                                print(' ')

                                # display info about file types                      
                                for line in info_file_types:
                                    print(line)

                                print(' ')

                                if not (message := _load_file()):
                                    
                                    break

                                if message == '`->!ABORT!<-`': # abort code

                                    # return to [en/de]crypt menu
                                    loop_get_message = False            
                                    break                                
                               
                                # if message loaded, break 
                                loop_print_message = False
                                break

                            elif method == '3': # return to main menu
                                
                                return_to_main_menu = True
                                break

                            else:
                                print('Invalid method selection. Please try' + \
                                      ' again.')

                        if return_to_main_menu:
                            break
                        
                    if return_to_main_menu:
                        return_to_main_menu = False   
                        break                

                    if mode == 'encrypt':
                        message_is_valid = \
                            validate_plaintext(message)
                
                    elif mode == 'decrypt':
                        message_is_valid = \
                            validate_ciphertext(message)

                    else: # this should never happen
                        raise FooBarError('Error: Invalid mode.')

                    # report validation check results
                    result: str = 'passes' if message_is_valid else 'fails'
                    print(f'Validation check {result} as {text_prefix}text.')

                except BadValueError as err:
                    print('\nUnable to complete operation.')
                    print(err)

                except FooBarError as err:
                    print('\nUnable to complete operation.')
                    print(err)
                    print(type(err))
                    print(err.subtext)
                    
                except Exception as err:
                    print('\nUnable to complete operation.')
                    print('\nAn unexpected error occurred.')
                    print(err)
                    print(type(err))
                    raise

                # build prompt
                action: str = 'Validate another message'

                # ask user if they would like to validate another message
                loop_validate_message: bool = _get_response(action)

        elif selection == 8: # about program / help / credits

            # print description of program
            print(__doc__, end = '')

            # print description of cipher
            for line in key_description:
                print(line)

            print(' ')
                
            for line in table_description:
                print(line)

            print(' ')

            # print all lines in each part of more_info
            for index in range(4):
                for line in more_info[index]:
                    print(line)

            print(' ')

            # print link to more info
            print('For more information on the Twosquare cipher, check out')
            print('the Wikipedia article at: \n')
            print('https://en.wikipedia.org/wiki/Two-square_cipher')
            
            print(' ')

            # print credits (author, contributors)
            print('>>> Program Credits <<<')
            print('* Creator: Scott Milton')
            print('* Contributors: [None]')
            print('* License: GPL-3.0')
            print('\nIf you would like to contribute to this project,')
            print('please feel free to visit the GitHub repo at: \n')
            print('https://github.com/scottmilton1/two-square-cipher')

            print(' ')

            # print special thanks
            print('This implementation is based on the description of the ')
            print('Twosquare cipher provided in the book Modern Cryptography:')
            print('Applied Mathematics for Encryption and Information Security')
            print('(First Version) by Chuck Eastom, McGraw Hill Publishing.')
            print('\nSpecial thanks to Chuck for writing this great book.')

        elif selection == 9: # exit program
            
            # confirm before exiting
            while True:
                confirm: str = input('\nConfirm: exit program? (Y/N)')
                
                if confirm.upper() == 'Y':
                    exit_program = True
                    loop_main = False
                    break
                
                elif confirm.upper() == 'N':
                    break

        else:
            print("Whoops! That's an invalid selection!")

        # display Main Menu caption for new loop
        if not exit_program and selection > 0 :
              
            print('\nMain Menu:\n'.upper())

    print('\nThank you for using Twosquare.\n')

    # exit program
    return

if __name__ == '__main__':
    __main__()
