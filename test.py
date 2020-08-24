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
from typing import Tuple
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

##### TEST RUNNERS #####

def run_test(assertion: str, verbose: bool = True) -> bool:
    """Runs an assertion.

    Returns True if assertion passes or False if fails.
    
    """

    try:
        exec(assertion)
  
    except AssertionError as err:

        if verbose:
            logging.debug(err)
            logging.debug('FAIL')
            
        return False
        
    else:
        
        if verbose:
            logging.debug('PASS')
            
        return True

def test_runner(tests: list) -> Tuple[int, int]:
    """Runs a list of tests using run_test function.

    Returns a tuple with the number of tests (passed, failed).

    """

    number_passed = number_failed = 0
    
    for test in tests:

        result = run_test(test, verbose = True)

        if result == True:
            number_passed += 1
            
        else:
            number_failed += 1

    return (number_passed, number_failed)




##### TESTS #####

def test_create_table(verbose: bool = True) -> NoReturn:
    """Test suite for create_table() function.


    """
    
    global global_passed
    global global_failed

    local_passed: int = 0
    local_failed: int = 0

    if verbose:
        logging.debug('\nRunning unit tests for create_table() function.')
        logging.debug('Testing different argument types...')

    # create tests against argument types
    tests_arg_types: list = [
        "assert create_table('string')",
        "assert not create_table(str)",
        "assert not create_table('') #mt string",
        "assert not create_table(' an invalid string!')",
        "assert not create_table(123)",
        "assert not create_table(b'01') #bytes",
        ]

    # test for correct return value types
    tests_ret_val: list = [        
        "assert type(create_table('keyword')) in [list, bool]",
        "assert type(create_table('keyword')) not in [str, int, tuple, dict]",
        "assert type(create_table('keyword')) not in [True, None, [ ], '']",
        ]

    # aliases for type hints
    Result: Tuple[str, str]
    Summary: List[Result, Result] = [ ]

    # run tests using the list of assertions
    Summary.append(test_runner(tests_arg_types))
    
    if verbose:
        logging.debug('Testing return values...')

    # run second block of tests
    Summary.append(test_runner(tests_ret_val))

    # unpack results and add to local counters
    for result in Summary:
        passed, failed = result
        local_passed += passed
        local_failed += failed

    if verbose:
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
