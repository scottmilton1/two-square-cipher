#!/usr/bin/env python3

"""An implementation of the two-square cipher.

This program encypts and decrypts messages using the two-square cipher,
aka double Playfair. There are two variations of the cipher, vertical
and horizontal, depending on how the two Playfair tables are arranged.
This implementation uses the first variation, so the two tables are
placed vertically.

""" 

# globals
from functools import partial

from typing import Callable
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Tuple
from typing import Union

if __name__ == 'twosquare.twosquare':
    _import_path = 'twosquare.exceptions'
    
else:
    _import_path = 'exceptions' 

# user-defined error class names
_custom_error_classes = [
    'BadValueError',
    'FooBarError',
    'StakesTooHighError',
    'TypeMismatchError',
    ]

# import the custom error classes from resolved path
for _error_class in _custom_error_classes:
    exec(f'from {_import_path} import {_error_class}') 

# use type aliases for type hints on complex types
Row = List[str]
Table = List[Row]

# set all print statements globally with setting flush = True
print = partial(print, flush = True)

def _get_coordinates(table: Table, letter: str) -> Tuple[int, int]:
    """Gets a letters coordinates from a Playfair table.

    Helper function for _xcrypt function.

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

def _xcrypt(mode: str, message: str, key1: str, key2: str, omit_j = True,
            remove_z = True) -> Union[str, bool]:
    """Encrypts or decrypts a message using the Twosquare cipher.

    Backend private function that serves as the workhorse for the public
    interface provided by the encrypt and decrypt functions. See the
    documentation for those two functions for more detailed information
    about each particular operation type.

    Parameters:

    mode must be a non-empty string.
    Valid values are:
        'e' or 'encrypt' for encryption
        'd' or 'decrypt' for decryption

    message must be a non-empty string containing the plaintext or
    ciphertext message to be rendered by the [en/de]cryption process.
    For the formatting rules required for validation of either message
    type, see the documentation for the corresponding function (encrypt
    or decrypt).

    keys must be non-empty strings with valid format. See the
    documentation for the encrypt function for more information about
    specific requirements.

    omit_j and remove_z are optional parameters and if included must be
    bool types. They are used for decryption operations only, and have
    no effect on message encryption. See the documentation for the
    decrypt function for more details on their use and effects.

    Returns:

    the [en/de]crypted message if the operation is successful        
    False if the operation is unsuccessful

    Dependencies:

    From string:
    ascii_uppercase

    from twosquare:
    _get_coordinates  
    BadValueError
    create_table
    FooBarError    
    Row
    Table
    TypeMismatchError
    validate_ciphertext
    validate_key
    validate_plaintext    

    from typing:
    List

    """

    from string import ascii_uppercase

    MAX_COLUMNS: int = 5
    MAX_ROWS: int = 5

    digraphs: List[str] = [ ]
    filtered_text: str = ''
    processed_text: str = ''  

    try:

        # validate mode
        if type(mode) is not str:

            raise TypeMismatchError('Mode must be a string.')

        if mode in ['e', 'encrypt']:

            mode = 'encrypt'

        elif mode in ['d', 'decrypt']:

            mode = 'decrypt'

        else:

            raise BadValueError('Error: Invalid mode.')

        # validate keys
        if not (validate_key(key1) and validate_key(key2)):
            raise BadValueError('Invalid key error. I am the gatekeeper. ' + \
                                'Are you the keymaster?')
        
        # validate message
        message_type = 'plain' if mode == 'encrypt' else 'cipher'
        
        if not validate_message(message, message_type):
            raise BadValueError(f'Invalid {message_type}text error.')

        # validate omit_j
        if type(omit_j) is not bool:
            raise TypeMismatchError('Type for omit_j must be bool.')

        # validate remove_z
        if type(remove_z) is not bool:
            raise TypeMismatchError('Type for remove_z must be bool.') 

        if mode == 'encrypt':
            
            # capitalize all letters in plaintext
            capitalized: str = message.upper()
            
            # filter to remove everything but ASCII letter characters
            for character in capitalized:
                if character in ascii_uppercase: # ignore Unicode letters
                    filtered_text += character

            # if length is odd add a 'Z' to end to make it even
            if len(filtered_text) % 2 != 0:
                filtered_text += 'Z'

        elif mode == 'decrypt':

            # remove J's from ciphertext string since they
            # are combined with I's in the encypted text
            filtered_text: str = message.replace('J', '')

            # if length of purged ciphertext is odd after removing Js raise  
            if len(filtered_text) % 2 != 0:
                
                raise BadValueError('Error: uneven number of letters in ' + \
                                    f'{message_type}text.')

        else:

            raise FooBarError('Error: Invalid mode value.')

        # split ciphertext into digraphs -
        # get two letters at a time
        for n in range(0, len(filtered_text), 2):

            # create a digraph with the two letters
            current_digraph: list = [filtered_text[n], filtered_text[n+1]]

            # store the current digraph in the list of all digraphs
            digraphs.append(current_digraph)

        # create first table with first key
        first_table: Table = create_table(key1) 

        # create second table with second key
        second_table: Table = create_table(key2)

        # create processed_text from message using the tables
        for digraph in digraphs:

            # unpack digraph
            letter1, letter2 = digraph

            column1: int = -1
            column2: int = -1
            row1: int = -1
            row2: int = -1

            # get each letter's coordinates in its table (row, column)
            row1, column1 = _get_coordinates(first_table, letter1)
            row2, column2 = _get_coordinates(second_table, letter2)

            if min(row1, row2, column1, column2) < 0:
                
                raise FooBarError('Table mismatch error. Unable to find ' + \
                                  'one or more letters of the ' + \
                                  f'{message_type}text using the tables ' + \
                                  'generated by the program.')

            # check to see which of two cases is true:
            # case 1: letters are in different columns - swap column numbers
            if column1 != column2:
                temp: int = column1
                column1 = column2
                column2 = temp

                # fetch letters from table using new coordinates
                processed_letter1 = first_table[row1][column1]
                processed_letter2 = second_table[row2][column2]

            # case 2: letters are in same column - leave letters as is
            else: # nope, that's not lazy, that's what the cipher says to do
                processed_letter1 = letter1
                processed_letter2 = letter2

            # remove J's from output if optional flag set
            if (mode == 'decrypt' and omit_j == True):
                
                if processed_letter1 == 'IJ':
                    processed_letter1 = 'I'
                    
                if processed_letter2 == 'IJ':
                    processed_letter2 = 'I'

            # add the two processed letters to the processed_text
            processed_text = processed_text + processed_letter1 + \
                             processed_letter2

        # remove trailing 'Z' from end of text if decrypt and optional flag set
        if mode == 'decrypt':
            
            if (remove_z == True and processed_text[-1] == 'Z'):
                
                processed_text = processed_text[0:-1]

    except BadValueError as err:
        print(err)
        return False

    except FooBarError as err:
        print(err)
        print(err.subtext)
        raise

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
        return processed_text

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

    From twosquare:
    BadValueError
    validate_key

    """

    # set table size
    MAX_ROWS: int = 5
    MAX_COLUMNS: int = 5

    try:

        if not validate_key(key):
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

def decrypt(ciphertext: str, key1: str, key2: str, omit_j = True,
            remove_z = True) -> Union[str, bool]:
    """Decrypts a message using the Twosquare cipher.

    Decrypts a ciphertext message using the two keys provided.

    This function is a basically a thin wrapper that serves as the
    public interface for the _xcrypt function, which is the backend for
    both the encrypt and decrypt functions.

    Parameters:

    Each key must be a valid keyword or key phrase:  
    a non-empty string with no more than twenty-five letters,
    ASCII letter characters only; no Unicode characters allowed,
    no duplicate letters; each letter may be used only once in each key,
    a key may not contain both 'I' and 'J' as these are combined
    by this cipher and are therefore counted as the same letter,
    no digits allowed - any numbers must be spelled out,
    no white space, punctuation, or special characters.

    Keys must be identical to the original keys used to encrypt the
    plaintext message and must be given in the same order or the
    decryption will not be accurate.

    ciphertext must be a valid string containing one or more alphabetic
    letters from the ASCII character set. Punctuation, special
    characters, unicode characters, digits, and white space are not
    allowed. All letters must be capitalized.

    If present, omit_j and remove_z must be boolean values and have the
    following effects:

    Setting omit_j to True will change the output of the deciphered
    message so that I and J characters are no longer combined as one.
    All J's will be removed so any I or J characters in the original
    plaintext message will be represented only as an I in the deciphered
    message output.

    Setting remove_z to True will remove a Z character from the end of
    the deciphered message, but only if the message has an even number
    of letters. Any combined IJ characters in the message are counted as
    one single letter in this tally. This assumes that the Z was added
    to an original plaintext that had an odd number of characters so
    that the Z was added to encrypt it.

    Note:

    Any white space removed from the original plaintext during
    the encryption process will not be replaced in the decrypted message.

    Returns:

    a string containing the decrypted message if successful
    False if the decryption operation is unsuccessful

    Dependencies:
    
    from twosquare:
    _xcrypt
  
    """

    return _xcrypt('decrypt', ciphertext, key1, key2, omit_j, remove_z)

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

def encrypt(plaintext: str, key1: str, key2: str) -> Union[str, bool]:
    """Encrypts a message using the Twosquare cipher.

    Encrypts a plaintext message using the two keys provided.
    
    This function is a basically a thin wrapper that serves as the
    public interface for the _xcrypt function, which is the backend for
    both the encrypt and decrypt functions.

    Parameters:

    Each key must be a valid keyword or key phrase:  
    a non-empty string with no more than twenty-five letters,
    ASCII letter characters only; no Unicode characters allowed,
    no duplicate letters; each letter may be used only once in each key,
    a key may not contain both 'I' and 'J' as these are combined
    by this cipher and are therefore counted as the same letter,
    no digits allowed - any numbers must be spelled out,
    no white space, punctuation, or special characters.

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

    Returns:

    a string containing the encoded ciphertext if successful
    False if the operation is unsuccessful

    Dependencies:
    
    From twosquare:
    _xcrypt
    
    """

    return _xcrypt('encrypt', plaintext, key1, key2)

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
                raise BadValueError('Only printable ASCII characters are ' + \
                                    f'allowed in {message_type}.')

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

    To pass, a key must be a valid keyword or key phrase:  
    a non-empty string with no more than twenty-five letters,
    ASCII letter characters only; no Unicode characters allowed,
    no duplicate letters; each letter may be used only once in each key,
    a key may not contain both 'I' and 'J' as these are combined
    by this cipher and are therefore counted as the same letter,
    no digits allowed - any numbers must be spelled out,
    no white space, punctuation, or special characters.

    Returns True if key passes all checks.
    Prints a failure message and returns False if key is invalid.

    Dependencies:

    From string:
    ascii_uppercase

    From twosquare:
    BadValueError
    TypeMismatchError

    """

    from string import ascii_uppercase

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

            # make sure letters are ASCII only, not unicode
            if character in ascii_uppercase:

                # add letter to the list to track it
                letters_in_key.append(character)
            
            else:
                raise BadValueError('Only ASCII letters are allowed in key.' + \
                                    ' No Unicode.')

        # make sure key does not contain both 'I' and 'J'   
        if all(letter in letters_in_key for letter in ['I', 'J']):
            raise BadValueError("Key may contain 'I' or 'J', but not both.")

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
                                f'{message_type}. Alas, symbolism is ' + \
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

    From twosquare:
    BadValueError
    TypeMismatchError

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
    """This is the main Twosquare program.

    The functions placed in the global scope of this implementation can
    also be used as a module.

    """

    def _coming_soon() -> NoReturn:
        """Prints a message indicating that a program's feature is coming soon.

        """

        print('\nThat feature is coming soon...')

        return True

    def _create_key(key_list: List[str], ordinal: List[str], \
         index: int, action: str = 'create') -> NoReturn:
        """Gets a valid key from the user and adds it to the list of keys.

        Prompts the user for a keyword or keyphrase, passes it to the
        validate_key function for validation, and inserts it in the
        key_list at the insertion point specified by the value of the
        index parameter.

        Parameters:
        
        key_list: list with values of type str prepopulated with values;
            empty strings are okay.
        ordinal: list of strings used for print formatting. It should
            contain values that are the ordinal numbers for the keys
            being created ('first', 'second').
        index: int value that must point to a valid index in the key_list
            and the list of ordinal numbers
        action: optional string value that indicates what is being done
            (e.g. - 'create' a new key or 'update' an existing key)

        Dependencies:

        From twosquare:
        _get_key
        validate_key
        
        """

        try:

            # prompt user for a key      
            key: str = _get_key(ordinal[index])

            # validate key and get again if not valid
            while not validate_key(key):
                key: str = _get_key()

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

        Dependencies:
        None

        """
    
        print('\nHere are your current keys: \n')

        for key_number, key in enumerate(keys, start = 1):

            if len(key) == 0:
                key = '[None]'
            
            print(f'KEY {key_number}: {key}')

        return

    def _display_menu(menu_options: list) -> Union[int, bool]:
        """Print a formatted list of program options.

        Returns number of menu_options in list if successful
        or returns False if an exception occurs. Keep this in mind,
        and handle potential Exceptions accordingly.

        Dependencies:
        None

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

        Dependencies:
        None

        TODOs - Ideas for additional features:
        Add keyword arg for text_alignment with default = 'center'

        """
        
        print('{:^80}'.format('>> ' + title.upper() + ' <<'))
        print('{:^80}'.format(byline.title()))

        # print bottom border that matches the length of the byline
        border: str = border_character * len(byline)
        print('{:^80}'.format(border))
        print()

        return

    def _get_filename() -> Union[str, int]:
        """Prompts the user for a filename.

        Returns a string containing the filename entered by the user if
        successful or returns a value of -1 if the user aborts.

        Dependencies:
        None

        """

        while True:

            filename: str = ''            
           
            while not (filename := input('Enter filename >> ')):

                # if user leaves blank return abort code
                if filename == '':

                    print(' ')
                    
                    return -1
                
                print('Invalid filename. Please try again.')

            # check for correct file type extension
            if filename.endswith('.txt') == False:
                
                print('\nOnly .txt file types are supported. Please ' + \
                      'try again.\n')

            else: # if file type valid

                return filename

    def _get_key(ordinal: str = '') -> str:
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

    def _get_response(action: str) -> bool:
        """Gets a yes or no response from the user.

        Prompts the user for input. The input validation only accepts
        [upper/lower]case variants of 'Y' and 'N'.

        Example use case: to check whether or not the user wants to perform
        another action in a loop or exit (to main menu / quit program, etc.).

        Returns True if user selects 'Y'
        Returns False if user selects 'N'
        
        Dependencies:
        None

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
        TypeMismatchError

        """

        valid_choices: List[str] = [ ]

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
            print(f'\n{header}')

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
            print('Unexpected exception type raised during execution:')
            print('In function: _get_selection') # function name
            print(type(err))
            print(err)
            raise

    def _file_io(mode: str, filename: str = '', message: str = '') \
                -> Union[str, int]:
        """Loads or saves a .txt file message.

        Loads or saves a plaintext or ciphertext message. Only .txt files
        are supported. To load a file, the file must exist in the current
        directory. To save a file, the file must not already exist in the
        current directory.

        Parameters:
        
        mode must be a non-empty string.
        Valid values are:
        'l' or 'load' for file input operations
        's' or 'save' for file output operations.

        filename, if included, must be a string representing a valid
        filename and must include the .txt file type extension in the
        name. If a filename is not included, the function will prompt
        the user for a filename.
        
        message is required as parameter for save operations only
        and any value passed for load operations will be ignored

        Returns:
        
        the message if loaded successfully OR
        an int value of 1 if file saved successfully
        an int value of 0 if unsuccessful
        an int value of -1 if user aborts operation

        Dependencies:

        From os:
        path.exists

        From twosquare:
        BadValueError
        FooBarError
        _get_filename
        _get_selection
        TypeMismatchError
   
        """

        from os.path import exists

        file_operation: Dict[List[str]] = {
            'load': ['loading', 'loaded'],
            'save': ['saving', 'saved'],
            }
        filename_included: bool = False
        instructions: Dict[List[str]] = {
            'load': [
                'Enter filename below and include the .txt extension.',
                'The file must be in the current directory.',
                'Leave the field blank and hit <enter> to abort.',
                ],
            'save': [
                'Enter filename below and include the .txt extension.',
                'The file will be saved in the current directory and',
                'cannot already exist. Leave the field blank and',
                'hit <enter> to abort.',
                ],
            }
        options: List[str] = [
            'Proceed',
            'Redo',
            'Abort',
            ]
        recourse_header: str = \
            'What would you like to do?'
        recourse_options: List[str] = [
            'Retry filename',
            'Re-enter filename',
            'Abort',
            ]

        try:

            if type(mode) is not str:

                raise TypeMismatchError('Mode must be a string.')

            if mode in ['l', 'load']:

                mode = 'load'

            elif mode in ['s', 'save']:

                mode = 'save'

            else:

                raise BadValueError('Invalid mode.')
            
            if type(filename) is not str:
                
                raise TypeMismatchError('Filename must be a string.')

            # check to see if filename included as parameter
            if len(filename) > 0:

                # if so make sure it has proper file type extension
                if filename.endswith('.txt'):
                
                    # set flag for non-interactive behavior
                    filename_included = True

                else: # if invalid file type
                    
                    raise BadValueError('File must be a .txt file.')

            # enforce message type and length for save operations only
            if mode == 'save':

                if type(message) is not str:
                
                    raise TypeMismatchError('Message must be a string.')

                if len(message) == 0:
                    
                    raise BadValueError('Message cannot be empty.')

            error_message: str = f'Could not {mode} {filename}'
            current_operation: str = file_operation.get(mode)[0].title()

            while True:

                # if filename is empty, get it from user
                while filename == '':

                    for line in instructions.get(mode):
                        print(line)
                        
                    print(' ')

                    # prompt user for filename                    
                    filename = _get_filename()

                    if filename == -1:

                        return -1
                    
                    # prompt the user - proceed, redo, or abort
                    header: str = f'Confirm filename: {filename}'
                    loop_get_choice: bool = True

                    while loop_get_choice:

                        choice: int = _get_selection(options, header, '')                    

                        if choice == 0: # proceed

                            break

                        elif choice == 1: # redo
                            
                            print('\nRedoing...\n')

                            # reset filename as blank
                            filename = ''

                            # go up one level to get file name again
                            break
                            
                        elif choice == 2: # abort

                            print('\nAborting...\n')
                            
                            return -1

                        else: # if choice has an invalid value
                            
                            raise FooBarError()

                # loop load file
                while filename:
                   
                    print(f'\n{current_operation} file...', end = '')

                    # perform file operation
                    try:

                        if mode == 'load':

                            message: str = ''

                            with open(filename, mode = 'r') as file:
                         
                                while line := file.readline():

                                    message += line                                        
                                  
                            if message:

                                print('Completed.')
                                
                                return message

                            else:
                                
                                print('Failed.\n')
                                   
                                raise Exception(error_message)

                        elif mode == 'save':

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
                                
                                print('Failed.\n')
                                   
                                raise Exception(error_message)

                        else: # mode not load or save

                            raise FooBarError('Error: invalid mode.')                        

                    except Exception as err:

                        # if file not found or other problem notify user
                        print(' ')
                        print(err)
                        print(type(err))

                        # if function call included filename and was not
                        # interactive, return now
                        if filename_included:

                            return 0

                        # otherwise, will prompt user for next action
                        recourse: int = \
                            _get_selection(recourse_options,
                            recourse_header, '')

                        if recourse == 0: # retry same filename

                            continue

                        elif recourse == 1: # re-enter filename

                            print(' ')

                            # reset filename
                            filename = ''

                            # return to beginning of filename entry
                            break

                        elif recourse == 2: # abort

                            print(' ')
                            
                            return -1

                        else: # if recourse has an invalid value
                            
                            raise FooBarError()

                else: # no filename - should not happen

                    raise FooBarError('Error: No filename in ' + \
                                      f'_{mode}_file.')

        except BadValueError as err:
            print(err)
            return 0

        except FooBarError as err:
            print(f'In function: _file_io')
            print('Bad return value from _get_selection function.')
            print(err.subtext)
            raise

        except TypeMismatchError as err:
            print(err)
            return 0

        except Exception as err:
            print(f'In function: _file_io')
            print(f'Unable to {mode} file. ' +
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
        '* ASCII letter characters only; no Unicode allowed',
        '* Each letter may not be used more than once in a key',
        "* A key may contain either 'I' or 'J', but not both",
        '* Digits are not allowed so any numbers must be spelled out',
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
    method_error: str = 'Invalid method selection. Please try again.'  
    method_options: List[str] = [
        'Manual entry',
        'From file',
        'Main menu',
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

            except Exception as err:
                
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
                    for index in range(len(more_info)): # range(4):
                        for line in more_info[index]:
                            print(line)

                    method_header: str = f'Select {text_prefix}text source:'

                    # prompt user for input method (manual / file)
                    method = _get_selection(method_options, method_header, \
                                            '', error_message = method_error)

                    if method == 0: # manual entry

                        print(' ')
                        
                        # prompt the user for message to encrypt / decrypt
                        prompt: str = f'Enter {text_prefix}text to {mode}: '
                        message: str = input(prompt)

                        # validate message format and get again until valid
                        while not (message_is_valid := \
                                   validate_message(message)):
                            
                            print(' ')
                            
                            message: str = input(prompt)                 

                    elif method == 1: # from file

                        print(' ')

                        # display info about file types                      
                        for line in info_file_types:
                            print(line)

                        print(' ')

                        # get message and if unsuccessful then...
                        if not (message := _file_io('l')):
                            
                            # return to loop_encode and display menu again
                            continue

                        if message == -1: # abort code

                            continue
                        
                        # validate message
                        if not (message_is_valid := \
                                validate_message(message)):                                
                         
                            raise BadValueError('Loaded message fails ' + \
                                                'validation check.')
                        
                    elif method == 2: # return to main menu
                        
                        break

                    else: # if method has an invalid value
                        
                        raise FooBarError()
            
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

                    else:
                        raise BadValueError()

                    display_message_actions: bool = True

                    # ask user what would like to do with message                    
                    while display_message_actions:
                        
                        message_action_header: str = \
                            'What would you like to do?' 
                        message_action_options: List[str] = [
                            'View message',
                            'Save message',
                            f'{code_prefix.title()}crypt another message.',
                            'Exit to main menu',
                            ]

                        message_action: str = _get_selection( \
                            message_action_options, message_action_header, '')                         

                        if message_action == 0: # view message

                            print(f'\nHere is the {code_prefix}coded ' + \
                                  'message:\n')

                            print(processed_text)
                            
                        elif message_action == 1: # save file

                            print(' ')

                            # display info about file types                      
                            for line in info_file_types:
                                print(line)

                            print(' ')

                            filename: str = ''

                            save_status: int = \
                                _file_io('s', filename, processed_text)

                            if save_status == 1:
                                print('File write successful. ' + \
                                      'Message saved.')
                                                                    
                            elif save_status == 0:
                                print('File write failed.')
                                
                            elif save_status == -1:
                                print('File write aborted.')
                                
                            else:
                                raise BadValueError('File write error.')

                        elif message_action == 2: # [en/de]crypt another
                            
                            # break and return to encode menu
                            return_to_loop_encode = True
                            break 

                        elif message_action == 3: # return to main menu

                            # up two levels:
                            return_to_main_menu = True
                            break                               

                        else: # if value of message_action is invalid

                            raise FooBarError()

                    if return_to_main_menu:

                        return_to_main_menu = False
                        
                        break
                    
                    # return early to avoid the prompt below exceptions section
                    if return_to_loop_encode:
                        
                        return_to_loop_encode = False

                        continue

                except BadValueError:
                    print('Unable to complete operation.')

                except FooBarError as err:
                    print('Unable to complete operation.')
                    print('\nAn unexpected error occurred.')
                    print(f'In __main__ function: menu selection [1/2]')
                    print(type(err))
                    print(err)
                    print(err.subtext)
                    
                except Exception as err:
                    print('Unable to complete operation.')
                    print('\nAn unexpected error occurred.')
                    print(f'In __main__ function: menu selection [1/2]')
                    print(err)
                    print(type(err))
                    raise
           
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
            message_type_header: str = 'Select message type:'
            message_type_options: List[str] = [
                'Plaintext',
                'Ciphertext',
                'Main menu',
                ]

            while loop_validate_message:

                try:

                    message_type = _get_selection(message_type_options,
                                                  message_type_header,
                                                  '')

                    if message_type in [0, 1]: # plaintext or ciphertext

                        # assign shorter name for message_type for convenience
                        index: int = [0, 1].index(message_type)

                        # use index to assign correct values for message type
                        code_prefix: str = ['en', 'de'][index]
                        info_message: List[str] = \
                            [info_plaintext, info_ciphertext][index]
                        mode: str = ['encrypt', 'decrypt'][index]
                        text_prefix: str = ['plain', 'cipher'][index]
                       
                    elif message_type == 2: # return to main menu

                        break

                    else: # if message_type has invalid value
                        
                        raise FooBarError()

                    print(' ') 
                    
                    loop_select_method: bool = True                 

                    while loop_select_method:                       
                        
                        method_header: str = f'Select {text_prefix}text source:'

                        print(f'Okay, {text_prefix}text...')

                        print(' ')

                        # print out brief description of message requirements
                        for line in info_message:
                            print(line)

                        # prompt user for input method (manual / file)
                        method = _get_selection(method_options,
                                                method_header,
                                                '',
                                                error_message = method_error)

                        if method == 0: # manual entry

                            print(' ')
                            
                            # prompt the user for message
                            prompt: str = f'Enter {text_prefix}text to ' + \
                                          f'validate: '
                            message: str = input(prompt)

                            break                        

                        elif method == 1: # from file

                            print(' ')

                            # display info about file types                      
                            for line in info_file_types:
                                print(line)

                            print(' ')

                            # get message and if unsuccessful...
                            if not (message := _file_io('l')):

                                # return to select method menu
                                continue
                                
                            if message == -1: # abort code

                                continue        
                           
                            # if message loaded, break 
                            break

                        elif method == 2: # return to main menu
                            
                            return_to_main_menu = True
                            break

                        else: # if method has invalid value                            
                          
                            raise FooBarError()
                        
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
                    print('Unable to complete operation.')
                    print(err)

                except FooBarError as err:
                    print('Unable to complete operation.')
                    print('\nAn unexpected error occurred.')
                    print(f'In __main__ function: menu selection 7')
                    print(err)
                    print(type(err))
                    print(err.subtext)
                   
                except Exception as err:
                    print('Unable to complete operation.')
                    print('\nAn unexpected error occurred.')
                    print(f'In __main__ function: menu selection 7')
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
                confirm: str = input('\nConfirm: exit program? (Y/N) >> ')
                
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
