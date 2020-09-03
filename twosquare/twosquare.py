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
for error_class_name in custom_error_classes:
    exec(f'from {import_path} import {error_class_name}') 

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

    Prints a Playfair table to the console for viewing purposes to
    facilitate development and testing.

    Returns True if successful or False if an error occurs.

    Dependencies:

    from twosquare:
        BadValueError
        validate_table
    
    """

    try:

        if not validate_table(table):
            raise BadValueError('Table is invalid.')
        
        print()

        # print each row of the table
        for row in table:

            # print each cell in current row
            for cell in row:
             
                print('%6s' % cell, end='')

            # white space to separate rows
            print('\n\n')

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
        # validate_message
        # validate_ciphertext
        # validate_plaintext

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
        if not validate_message(plaintext):
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

def get_mode() -> Union[str, bool]:
    """Gets program mode from user.

    Prompts user for program mode (encryption or decryption).

    Returns string value 'encrypt' or 'decrypt' based on user selection
    or returns False if user has made an invalid selection.

    Dependencies:
        None
        
    """
    
    try:

        mode: str = input("Select mode: 1 for encrypt or 2 for decrypt >> ")

        if mode == '1':
            return 'encrypt'

        elif mode == '2':
            return 'decrypt'

    except Exception as err:
        from inspect import currentframe as cf
        print('Unexpected exception type raised during execution:')
        print(f'In function: {cf().f_code.co_name}') # function name
        print(type(err))
        print(err)
        raise

    else:
        return False

def validate_ciphertext(message: bool) -> bool:
    """Validates a ciphertext message for the Twosquare cipher.

    Basically a thin wrapper that serves as syntactic sugar for the
    validate_message() function.

    
    Dependencies:

    From twosquare:
        validate_message

    TO BE IMPLEMENTED...

    """

    pass

def validate_key(key: str) -> bool:
    """Validates a key for a Playfair table.

    Takes a string as input and validates it against the formatting
    specifications of a keyword or key phrase for a Playfair table.

    Returns True if key passes all checks.
    Prints a failure message and returns False if key is invalid.

    Dependencies:
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

def validate_message(message: str, mode: str = 'encrypt') -> bool:
    """Validates a message for the Twosquare cipher.

    Validates a plaintext or ciphertext message according to the requirements
    and expected values of the Twosquare cipher.

    Helper function for encrypt and decrypt functions.

    Returns True if the message is valid or False otherwise.

    Dependencies:
        BadValueError
        TypeMismatchError

    """

    try:

        message_type: str = 'Plaintext' if mode == 'encrypt' else 'Ciphertext'

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
        if not (message.isascii() and message.isprintable()):
            raise BadValueError(f'Error: {message_type} can consist of ' + \
                                'printable ASCII characters only.\n' + \
                                'Sorry, my friend. No unicorns allowed!')

        contains_a_letter: bool = False

        # filter to remove non-alpha characters
        for character in message:
            if character.isalpha():
                contains_a_letter = True
                break      

        if contains_a_letter == False:
            raise BadValueError('Error: No alpha characters in plaintext. ' + \
                                'Alas, symbolism is sensational,\nand ' + \
                                'punctuation is paramount, but letters ' + \
                                'are legendary!')        

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
    

def validate_plaintext(message: str) -> bool:
    """Validates a plaintext message for the Twosquare cipher.

    Basically a thin wrapper that serves as syntactic sugar for the
    validate_message() function.

    Dependencies:

    From twosquare:
        validate_message

    TO BE IMPLEMENTED...

    """

    pass

   
def validate_table(table: Table) -> bool:
    """Validates a Playfair table.

    Returns True if the table is valid or False otherwise.

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

        print('\nThat feature is coming soon...\n')

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
            key_list.insert(index, key)

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

        Prompts the user for an input response.
        
        Use case example: whether or not the user wants to
        perform the same action again.

        Only accepts [upper/lower]case variants of 'Y' and 'N'

        Returns True if user selects 'Y'
        Returns False if user selects 'N'

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

    exit_program: bool = False
    loop_main: bool = True
    key_description: List[str] = [
        '\nThe Twosquare cipher uses two keys to encrypt and decrypt messages.',
        '\n>Each key can be a key word or phrase:',
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
    ordinal: List[str] = ['first', 'second']
    program_name: str = "twosquare"
    program_description: str = \
        "encrypt and decrypt messages with the two-square cipher"
    return_to_main_menu: bool = False
    tables: Union[Table, bool] = [[ ], [ ]] # CHANGE THIS TO LIST FOR HINT???

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

        elif selection == 1: # encrypt a plaintext
            _coming_soon()

            # if 0 or 1 keys exist, notify user
                # (and ask if would like to create a key)
                # (if so, take directly to create key operation)

            # print a brief description of process and requirements
            # give option for more detailed information

            # get plaintext from user
                # manual entry
                # load from .txt file

            # confirm plaintext / file name

            # perform encryption

            # report operation success / failure
                # give reason / feedback for failure

            # if successful, ask user if they would like to display the
            # encrypted message (or save it as a .txt file)
                # if so, display / save message
                # print success / failure message

            # ask user if they would like to encrypt another file using the
            # same keys


##            text_prefix: str = 'plain' if mode == 'encrypt' else 'cipher'
##
##            prompt: str = f'Enter {text_prefix}text to {mode}: '
##            
##            # prompt the user for message to encrypt / decrypt
##            message: str = input(prompt)
##
##            # validate message format and get again until valid
##            while not (message_is_valid := validate_message(message)):
##                print(' ')
##                message: str = input(prompt)
##
##            # prepare to perform encoding or decoding of message  
##            # choose function to call depending on selected mode
##            func: Callable[[str, str, str], Union[str, bool]] = encrypt if \
##                mode == 'encrypt' else decrypt
##
##            # plug appropriate function into callable partial with args
##            action: Callable[[ ], str] = partial(func, message, keys[0], keys[1])
##
##            # call function and get [en/de]decoded processed_text
##            processed_text: str = action()
##            
##            if processed_text:
##                print('\nOperation succcessful.')
##
##                code_prefix: str = 'en' if mode == 'encrypt' else 'de'
##
##                # display (en/de)coded message
##                print(f'Here is the {code_prefix}coded message:\n')
##                print(processed_text)
##
##            else:
##                print('\nUnable to perform operation.')
##
##                # include information about why operation failed
##
##                # give option to retry or quit



        elif selection == 2: # decrypt a ciphertext
            _coming_soon()

            # print a brief description of process and requirements
            # give option for more detailed information

            # get ciphertext from user
                # manual entry
                # load from .txt file

            # confirm ciphertext / file name

            # perform decryption

            # report operation success / failure
                # give reason / feedback for failure

            # if successful, ask user if they would like to display the
            # decrypted message (or save it as a .txt file)
                # if so, display / save message
                # print success / failure message

            # ask user if they would like to decrypt another file using the
            # same keys

        elif selection == 3: # create a new key

            loop_create_key: bool = True

            while loop_create_key:

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

            print('\nThe Twosquare cipher uses two 5 x 5 Playfair tables to')
            print('encrypt and decrypt messages for you. These two tables')
            print('are each generated using one of the keys you create.')

            if len(keys[0]) == 0:
                print('\nYou have not created any keys yet so')
                print('no tables can be generated using them.\n')

            else:
                print('\nHere are the tables generated with your keys:\n')

            # display all current tables or 'None' if none exist
            for table_number in range(1,3):
                print(f'TABLE {table_number}: ', end = '')
            
                # adjust for target list index for keys and tables
                index: int = table_number - 1

                # check to see if key exists, and if so...
                if len(keys[index]) > 0:

                    print(' ')

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
            _coming_soon()

            # prompt user for type of message to validate
            # plaintext or ciphertext

            # print out brief description of message requirements
            # with option for more detailed information

            # get message from user

            # run validation check

            # report results

            # ask user if they would like to validate another message

            # if so continue

            # if not break and return to main menu

        elif selection == 8: # about program / help
            _coming_soon()

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

        if not exit_program and selection > 0 :
            print('\nMain Menu:\n'.upper())

    print('Thank you for using Twosquare.')

    # exit program
    return

    ######

##    try:
##       
##        text_prefix: str = 'plain' if mode == 'encrypt' else 'cipher'
##
##        prompt: str = f'Enter {text_prefix}text to {mode}: '
##        
##        # prompt the user for message to encrypt / decrypt
##        message: str = input(prompt)
##
##        # validate message format and get again until valid
##        while not (message_is_valid := validate_message(message)):
##            print(' ')
##            message: str = input(prompt)
##
##        # prepare to perform encoding or decoding of message  
##        # choose function to call depending on selected mode
##        func: Callable[[str, str, str], Union[str, bool]] = encrypt if \
##            mode == 'encrypt' else decrypt
##
##        # plug appropriate function into callable partial with args
##        action: Callable[[ ], str] = partial(func, message, keys[0], keys[1])
##
##        # call function and get [en/de]decoded processed_text
##        processed_text: str = action()
##        
##        if processed_text:
##            print('\nOperation succcessful.')
##
##            code_prefix: str = 'en' if mode == 'encrypt' else 'de'
##
##            # display (en/de)coded message
##            print(f'Here is the {code_prefix}coded message:\n')
##            print(processed_text)
##
##        else:
##            print('\nUnable to perform operation.')
##
##            # include information about why operation failed
##
##            # give option to retry or quit
##
##    except Exception as err:
##        print('Unexpected exception type raised during program execution:')
##        print(type(err))
##        print(err)
##        # add stack trace
##        # add error code and way to report it to me - email
##        raise

    # TODOs - PLANNED FUNCTIONALITY TO IMPLEMENT:

    # add main program menu with options for help and program exit

    # prompt user to accept or redo keys after table display

    # confirm message before (en/de)coding - e.g. - [P]roceed or [R]edo  
    
    # OPTIONAL FUNCTIONALITY TO POSSIBLY IMPLEMENT LATER:

    # command-line usage

    # get message text from file instead of keyboard

    # write message output to file

if __name__ == '__main__':
    __main__()
