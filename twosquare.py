#!/usr/bin/env python3

"""An implementation of the two-square cipher.

This program encypts and decrypts messages using the two-square cipher,
aka double Playfair. There are two variations of the cipher, vertical
and horizontal, depending on how the two Playfair tables are arranged.
This implementation uses the first variation, so the two tables are
placed vertically.

The functionality of this program can also be used as a module.

"""

def get_key():
    """Gets key from user and returns it.

    Prompts user for keyword or key phrase. Does not perform any
    validaty checks of user input for proper key formatting
    restrictions, which is left to validate_key() function.

    Returns the string value entered by the user.

    """

    while not (key := input("Enter keyword or key phrase >> ")):

        print("Invalid entry. Please try again.")

    return key

def get_mode():
    """Gets program mode from user.

    Prompts user for program mode (encryption or decryption).

    Returns string value 'encrypt' or 'decrypt' based on user selection
    or returns False if user has made an invalid selection.
    """

    mode = input("Select mode: 1 for encrypt or 2 for decrypt >> ")

    if mode == '1':
        return 'encrypt'

    elif mode == '2':
        return 'decrypt'

    else:
        return False

def __main__():
    """This is the main program.

    The functionality of this implementation can also be used as a module.
    """

    # display program title and brief description
    name = "twosquare"
    description = "encrypt and decrypt messages with the two-square cipher"
    print('{:^80}'.format('>> ' + name.upper() + ' <<'))
    print('{:^80}'.format(description.title()))

    # print bottom border that matches the length of the program description
    border_character = '-'
    border = border_character * len(description)
    print('{:^80}'.format(border))

    # prompt user for mode - encrypt or decrypt
    print()

    # get input until user chooses a valid selection
##    while not (mode := get_mode()):
##        print('Invalid selection. Please try again!')
##       
##    assert mode == 'encrypt' or mode == 'decrypt'

    # prompt user for first key
##    first_key = get_key()
##
##    assert first_key

    # validate key
    def validate_key(key):
        """Validates a key for a Playfair table.

        Takes a string as input and validates it against the formatting
        specifications of a keyword or key phrase for a Playfair table.

        Returns True if key passes all checks.
        Prints a failure message and returns False if key in invalid.

        """

        try:
            if type(key) is not str:
                raise ValueError('key must be a string')
            
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
        
    def test_validate_key():
        """Test suite for validate_key() function.
        """

        print('Running unit tests for validate_key() function.')

        # test for types
        assert validate_key('astring')
        assert not validate_key(['list', 2])
        assert not validate_key(123)
        assert not validate_key(True)
        assert not validate_key(None)
        assert not validate_key({})

        print('All tests passed.')
    
    test_validate_key()



    # prompt user for second key

    # validate key

    # create first table with first key

    # create second table with second key

    # display the tables to the console for viewing - optional functionality

    # prompt the user for message (or text file) to encrypt / decrypt

    # perform encoding or decoding of message (or text file)

    # display message to confirm operation success or failure

    # print out the modified text to the console - optional functionality

if __name__ == '__main__':
    __main__()
