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
from twosquare.twosquare import encrypt
from twosquare.twosquare import decrypt

# use logging for test output   
import logging
logging.basicConfig(level=logging.DEBUG, format = '%(message)s',)

# globals
VERBOSE: bool = True
global_passed: int = 0
global_failed: int = 0

valid_table_example: Table = [
     ['P', 'Y', 'T', 'H', 'O'],
     ['N', 'A', 'B', 'C', 'D'],
     ['E', 'F', 'G', 'IJ', 'K'],
     ['L', 'M', 'Q', 'R', 'S'],
     ['U', 'V', 'W', 'X', 'Z'],
     ]

##### TEST RUNNERS #####

def run_test(assertion: str, verbose: bool = True) -> bool:
    """Runs an assertion.

    Executes a single assertion using builtin exec() function.

    Returns True if assertion passes or False if fails.
    
    If verbose is set to True, outputs a pass / fail message via logging.
    
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

def test_runner(tests: list, verbose: bool = True) -> Tuple[int, int]:
    """Runs a list of tests using run_test function.

    Returns a tuple with the number of tests (passed, failed).

    """

    number_passed: int = 0
    number_failed: int = 0
    
    for test in tests:

        result: bool = run_test(test, verbose)

        if result == True:
            number_passed += 1
            
        else:
            number_failed += 1

    return (number_passed, number_failed)


##### CUSTOM ASSERTIONS #####

def assert_equal(expected_result, func, *args, **kwargs) -> str:
    """Tests that a function's return value equals an expected result.

    This is a custom assertion designed to display improved output for a
    failed test when more information than a simple PASS / FAIL messsage
    is desired i.e. - when running multiple test cases in a test runner.
    
    To illustrate, if the return value of the function does not equal
    the value of the expected_result, the failure message returned will
    include the name of the function, the values of the args used in the
    test, and the expected result.

    Here is an example of output for a failed test case:

    Assume we want to use assert_equal for a custom add function that
    we know works correctly and as intended. We can test that our add
    function fails when it should by plugging the test values into our
    assert_equal function as follows...

    assert_equal(expected_result, func, *args, **kwargs)
    
    assert_equal(2, add, 1, 2)

    Doing this should produce the following failed test case output:

    'FAIL: add(1,2) == 2'

    Just to be crystal clear, the function add() when run with the
    parameters provided for the *args, in this case 1 and 2, returned a
    value that did not match the value of the parameter provided for the
    arg expected_result, which was 2 in this case. Ergo, the test case
    failed and the corresponding failure message was returned.

    More coffee please...
    

    """

    try:
        assert expected_result == func(*args, **kwargs)
        
    except AssertionError as err:
        message = f'FAIL: {func.__name__}('

        if len(args) > 0:
            if type(args[0]) == str:
                message = message + "'" + str(args[0]) + "'"
                
            else:
                message = message + str(args[0])

        if len(args) > 1:
            for i in range(1, len(args)):
                message = message + ', '

                if type(args[i]) == str:
                    message = message + "'" + str(args[i]) + "'"

                else:
                    message += str(args[i])

        if len(kwargs) == 1:
            for k, v in kwargs.items():
                message = message + str(k) + '=' + str(v) 

        elif len(kwargs) > 1:
            for k, v in kwargs.items():
                message = message + str(k) + '=' + str(v) + ', '
            message = message[0:-2]

        message = message + ') == ' +  str(expected_result)

        return message               

    except Exception as err:
        return f'Unexpected exception raised during test execution: \n{err}'

    else:
        return "PASS"

##### UNIT TESTS FOR TWOSQUARE FUNCTIONS #####

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

    # create tests for return value types
    tests_ret_val: list = [        
        "assert type(create_table('keyword')) in [list, bool]",
        "assert type(create_table('keyword')) not in [str, int, tuple, dict]",
        "assert type(create_table('keyword')) not in [True, None, [ ], '']",
        ]

    # aliases for type hints
    Result: Tuple[str, str]
    Summary: List[Result, Result] = [ ]

    # run tests using the list of assertions
    Summary.append(test_runner(tests_arg_types, verbose))
    
    if verbose:
        logging.debug('Testing return values...')

    # run second block of tests
    Summary.append(test_runner(tests_ret_val, verbose))

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

def test_display_table(verbose: bool = True) -> NoReturn:
    """Test suite for display_table() function.

    """

    global global_passed
    global global_failed

    local_passed: int = 0
    local_failed: int = 0

    if verbose:
        logging.debug('\nRunning unit tests for display_table() function.')
        logging.debug('Testing different argument types...')

    # test against argument types
    result = assert_equal(False, display_table, 'string')
   
    if result == 'PASS':
        local_passed += 1
        
    elif result.startswith('FAIL'):
        local_failed += 1
        
    else:
        if verbose:
            logging.debug('Unexpected test result from assert_equal function.')
        local_failed += 1
        
    if verbose:
        logging.debug(result)

    # create tests against argument types
    tests_arg_types: list = [
        "assert not display_table(list)",
        "assert not display_table(123)",      
        "assert not display_table({'dict': 'ionary'})",
        ]

    # create tests for values
    tests_values: list = [
        "assert display_table([" +
            "['A', 'B', 'C', 'D', 'E']," +
            "['A', 'B', 'C', 'D', 'E']," +
            "['A', 'B', 'C', 'D', 'E']," +
            "['A', 'B', 'C', 'D', 'E']," +
            "['A', 'B', 'C', 'D', 'E']," +
            "])",
        # bad table structure
        "assert not display_table(['list'])",
        # not enough rows in table
        "assert not display_table([" +          
            "['A', 'B', 'C', 'D', 'E']," +
            "['A', 'B', 'C', 'D', 'E']," +
            "])",
        # too many items in row
        "assert not display_table([" +
            "['A', 'B', 'C', 'D', 'E', 'F']," +
            "['A', 'B', 'C', 'D', 'E']," +
            "['A', 'B', 'C', 'D', 'E']," +
            "['A', 'B', 'C', 'D', 'E']," +
            "['A', 'B', 'C', 'D', 'E']," +
            "])",
        # table data is not of type string
        "assert not display_table([" +
            "[1,2,3,4,5]," +
            "[1,2,3,4,5]," +
            "[1,2,3,4,5]," +
            "[1,2,3,4,5]," +
            "[1,2,3,4,5]," +
            "])",
        ]

    # create tests for return value types
    tests_ret_val: list = [        
        "assert type(display_table([[1,2],[3,4]])) == " +
            "display_table.__annotations__.get('return')", # bool
        "assert type(display_table(123) == " +
            "display_table.__annotations__.get('return'))", # bool
        "assert type(display_table([[5,6],[7,8]])) is bool",
        "assert type(display_table('false return')) is bool", 
        ]

    # aliases for type hints
    Result: Tuple[str, str]
    Summary: List[Result, Result, Result] = [ ]

    # run tests using the list of assertions
    Summary.append(test_runner(tests_arg_types, verbose))    

    if verbose:
        logging.debug('Testing more table values and structures...')

    # run second block of tests
    Summary.append(test_runner(tests_values, verbose))

    if verbose:
        logging.debug('Testing return values...')

    # run third block of tests
    Summary.append(test_runner(tests_ret_val, verbose))

    if verbose:
        logging.debug(f'{local_passed} tests passed.')
        logging.debug(f'{local_failed} tests failed.')

    global_passed += local_passed
    global_failed += local_failed

def test_decrypt(verbose: bool = True) -> NoReturn:
    """Test suite for decrypt() function.

    # USE THIS FORMAT TO CREATE GENERALIZED FUNCTION THAT CAN PASS
    # TEST BANKS TO AS ARGUMENTS - REFACTOR FOR DRY PRINCIPLE

    """

    global global_passed
    global global_failed

    local_passed: int = 0
    local_failed: int = 0

    if verbose:
        logging.debug('\nRunning unit tests for decrypt() function.')
        logging.debug('Testing different argument types...')

    # create tests against argument types
    tests_arg_types: list = [ ]

    # create tests for correct return value types
    tests_ret_val: list = [ ]

    # aliases for type hints
    Result: Tuple[str, str]
    Summary: List[Result, Result] = [ ]

    # run tests using the list of assertions
    Summary.append(test_runner(tests_arg_types, verbose))
    
    if verbose:
        logging.debug('Testing return values...')

    # run second block of tests
    Summary.append(test_runner(tests_ret_val, verbose))

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

def test_encrypt(verbose: bool = True) -> NoReturn:
    """Test suite for encrypt() function.

    """

    global global_passed
    global global_failed

    local_passed: int = 0
    local_failed: int = 0

    if verbose:
        logging.debug('\nRunning unit tests for encrypt() function.')
        logging.debug('Testing different argument types...')

    # create tests against argument types
    tests_arg_types: list = [
        'assert encrypt("This should pass", "falcon", "osprey")',
        'assert not encrypt("One invalid keyword", "keyword", "pythonista")',
        'assert not encrypt(123, "not", "string")',
        'assert not encrypt("", "empty", "plaintex")',
        'assert not encrypt("$^&@.", "only", "symbol")',
        'assert not encrypt("1234", "only", "digts")', 
        'assert not encrypt("1.234", "only", "numbers")',
        'assert not encrypt("    ", "only", "whitespac")',
        'assert not encrypt("accént", "foreign", "chars")',
        'assert not encrypt("umläütö", "foreign", "chars")', 
        'assert not encrypt("文字", "foreign", "chars")',
        ]

    # create tests for correct return value types
    tests_ret_val: list = [
        'assert type(encrypt("This should pass", "falcon", "osprey")) == str',
        'assert type(encrypt("Retürns Fälse", "python", "tricks")) is bool',        
        ]

    # aliases for type hints
    Result: Tuple[str, str]
    Summary: List[Result, Result] = [ ]

    # run tests using the list of assertions
    Summary.append(test_runner(tests_arg_types, verbose))
    
    if verbose:
        logging.debug('Testing return values...')

    # run second block of tests
    Summary.append(test_runner(tests_ret_val, verbose))

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



def test_validate_key(verbose: bool = True) -> NoReturn:
    """Test suite for validate_key() function.

    """

    global global_passed
    global global_failed

    local_passed: int = 0
    local_failed: int = 0

    if verbose:
        logging.debug('\nRunning unit tests for validate_key() function.')
        logging.debug('Testing different argument types...')

    # create tests against argument types
    tests_arg_types: list = [
        "assert validate_key('astring')",
        "assert not validate_key(['list', 2])",
        "assert not validate_key(123)",
        "assert not validate_key(True)",
        "assert not validate_key(None)",
        "assert not validate_key({})",
        ]

    # create tests for correct return value types
    tests_ret_val: list = [        
        "assert type(validate_key('foo')) is bool",
        "assert not type(validate_key('bar')) == None",
        "assert not type(validate_key('baz')) == str",
        "assert not type(validate_key('bah')) == int",
        ]

    # aliases for type hints
    Result: Tuple[str, str]
    Summary: List[Result, Result] = [ ]

    # run tests using the list of assertions
    Summary.append(test_runner(tests_arg_types, verbose))
    
    if verbose:
        logging.debug('Testing return values...')

    # run second block of tests
    Summary.append(test_runner(tests_ret_val, verbose))

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


def __main__(verbose: bool = VERBOSE):

    # run unit tests if debugging is on
    if __debug__:

        global global_passed
        global global_failed

        # THESE TWO WON'T WORK HERE - CREATE NEW TESTS???
        # assert mode == 'encrypt' or mode == 'decrypt'
        # assert first_key

        test_validate_key(verbose)
        test_create_table(verbose)
        test_display_table(verbose)
        test_encrypt(verbose)
        # test_decrypt(verbose)

        logging.debug(f'TOTAL TESTS PASSED: {global_passed}')
        logging.debug(f'TOTAL TESTS FAILED: {global_failed}')

        # perhaps create decorator for unit tests and wrap functions in it

if __name__ == '__main__':
    __main__()
