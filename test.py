#!/usr/bin/env python3

"""Test suite for twosquare.py

This is a suite of unit tests comprised of simple builtin assertions.
The reason for this type of implementation is educational in nature -
simply to gain a better understanding of how to write unit tests
without relying on a module or package to do the heavy lifting and
abstract away the basic underlying processes involved.

Feel free to replace this test suite with your test runner of choice.

"""
from typing import List
from typing import NoReturn
from typing import Union

from twosquare.twosquare import Row
from twosquare.twosquare import Table
from twosquare.twosquare import create_table
from twosquare.twosquare import display_table
from twosquare.twosquare import validate_key

# use logging for test output   
import logging
logging.basicConfig(level=logging.DEBUG, format = '%(message)s',)

# globals
global_passed: int = 0
global_failed: int = 0

def run_test(assertion: str) -> bool:
    """Runs an assertion.

    Returns True if assertion passes or False if fails.
    
    """

    try:
        exec(assertion)
  
    except AssertionError as err:
        logging.debug('FAIL')
        return False
        
    else:
        logging.debug('PASS')
        return True
        

def test_create_table() -> NoReturn:
    """Test suite for create_table() function.

    """
    
    global global_passed
    global global_failed

    local_passed: int = 0
    local_failed: int = 0

    logging.debug('\nRunning unit tests for create_table() function.')
    logging.debug('Testing different argument types...')

    # test against argument types
    try:
        assert create_table('string')
        
    except AssertionError as err:
        logging.debug('FAIL')
        local_failed += 1
    else:
        logging.debug('PASS')
        local_passed += 1  

    tests: list = [
        "assert not create_table(str)",
        "assert not create_table('') #mt string",
        "assert not create_table(' an invalid string!')",
        "assert not create_table(123)",
        "assert not create_table(b'01') #bytes",
        ]

    test_suite: str = """


    """

    for test in tests:
        
        try:
            exec(test)
          
        except AssertionError as err:
            logging.debug('FAIL')
            logging.debug(err)
            local_failed += 1
            
        else:
            logging.debug('PASS')
            local_passed += 1

    # this creates problem unmentioned in the requirements for a key
    # since 'I' and 'J' are combined into a single letter in a Playfair
    # table, the key must not contain both to avoid duplicate letters
    # assert create_table('jim')

    logging.debug('Testing return values...')

    # test for return value types
    assert type(create_table('keyword')) in [list, bool]
    assert type(create_table('keyword')) not in [str, int, tuple, dict]
    assert type(create_table('keyword')) not in [True, None, [ ], '']
    
    logging.debug(f'{local_passed} tests passed.')
    logging.debug(f'{local_failed} tests failed.')

    global_passed += local_passed
    global_failed += local_failed

def test_display_table() -> NoReturn:
    """Test suite for display_table() function.

    """

    global global_passed
    global global_failed

    local_passed: int = 0
    local_failed: int = 0

    logging.debug('\nRunning unit tests for display_table() function.')
    logging.debug('Testing different argument types...')

    # test against argument types
    assert not display_table(list)
    assert not display_table('string')
    assert not display_table(123)        
    assert not display_table({'dict': 'ionary'})

    logging.debug('Testing more table values and structures...')

    # test for values
    assert display_table([
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'B', 'C', 'D', 'E'],
        ])
    assert not display_table(['list'])  # bad table structure
    # not enough rows in table
    assert not display_table([              
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'B', 'C', 'D', 'E'],
        ])
    # too many items in row
    assert not display_table([
        ['A', 'B', 'C', 'D', 'E', 'F'], 
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'B', 'C', 'D', 'E'],
        ])
    # table data is not of type string
    assert not display_table([
        [1,2,3,4,5],
        [1,2,3,4,5],
        [1,2,3,4,5],
        [1,2,3,4,5],
        [1,2,3,4,5],
        ])

    logging.debug('Testing return values...')

    # check that return value matches type hint in function annotation
    dta = display_table.__annotations__
    assert type(display_table([[1,2],[3,4]])) == dta.get('return') # bool
    assert type(display_table(123) == dta.get('return')) # bool

    assert type(display_table([[5,6],[7,8]])) is bool
    assert type(display_table('false return')) is bool  

    logging.debug(f'{local_passed} tests passed.')
    logging.debug(f'{local_failed} tests failed.')

    global_passed += local_passed
    global_failed += local_failed

def test_validate_key() -> NoReturn:
    """Test suite for validate_key() function.

    """

    global global_passed
    global global_failed

    local_passed: int = 0
    local_failed: int = 0

    logging.debug('\nRunning unit tests for validate_key() function.')
    logging.debug('Testing different argument types...')

    # test against argument types
    assert validate_key('astring')
    assert not validate_key(['list', 2])
    assert not validate_key(123)
    assert not validate_key(True)
    assert not validate_key(None)
    assert not validate_key({})

    logging.debug('Testing return values...')

    # test for return types
    assert type(validate_key('foo')) is bool
    assert not type(validate_key('bar')) == None
    assert not type(validate_key('baz')) == str
    assert not type(validate_key('bah')) == int     

    logging.debug(f'{local_passed} tests passed.')
    logging.debug(f'{local_failed} tests failed.')

    global_passed += local_passed
    global_failed += local_failed


def __main__():

    # run unit tests if debugging is on
    if __debug__:

        global global_passed
        global global_failed

        # THESE TWO WON'T WORK HERE - CREATE NEW TESTS???
        # assert mode == 'encrypt' or mode == 'decrypt'
        # assert first_key

        test_validate_key()
        test_create_table()
        test_display_table()

        logging.debug(f'TOTAL TESTS PASSED: {global_passed}')
        logging.debug(f'TOTAL TESTS FAILED: {global_failed}')

        # perhaps create decorator for unit tests and wrap functions in it

if __name__ == '__main__':
    __main__()
