#!/usr/bin/env python3

"""Test suite for twosquare.py

This is a suite of unit tests comprised of simple builtin assertions.
The reason for this type of implementation is educational in nature -
simply to gain a better understanding of how to write unit tests
without relying on a module or package to do the heavy lifting and
abstract away the basic underlying processes involved.

Feel free to replace this test suite with your test runner of choice.

"""

# import all functions to be tested
from twosquare.twosquare import Row
from twosquare.twosquare import Table
from twosquare.twosquare import create_table
from twosquare.twosquare import decrypt
from twosquare.twosquare import display_table
from twosquare.twosquare import encode
from twosquare.twosquare import encrypt
from twosquare.twosquare import validate_ciphertext
from twosquare.twosquare import validate_key
from twosquare.twosquare import validate_message
from twosquare.twosquare import validate_plaintext
from twosquare.twosquare import validate_table

# import general types (optional: for type hint checking)
from typing import List
from typing import NoReturn
from typing import Tuple
from typing import Union

# use logging for test output
import logging
logging.basicConfig(level=logging.DEBUG, format = '%(message)s',)

# globals
VERBOSE: bool = True
##global_passed: int = 0
##global_failed: int = 0

# table data is not of type string
invalid_table_example_1: Table = [
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
    ]

# same letter more than once
invalid_table_example_2: Table = [
    ['A', 'B', 'C', 'D', 'E'],
    ['A', 'B', 'C', 'D', 'E'],
    ['A', 'B', 'C', 'D', 'E'],
    ['A', 'B', 'C', 'D', 'E'],
    ['A', 'B', 'C', 'D', 'E'],
    ]        

# not enough rows in table
invalid_table_example_3: Table = [           
    ['A', 'B', 'C', 'D', 'E'],
    ['A', 'B', 'C', 'D', 'E'],
    ]

# too many items in row
invalid_table_example_4: Table = [           
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['A', 'B', 'C', 'D', 'E'],
    ['A', 'B', 'C', 'D', 'E'],
    ['A', 'B', 'C', 'D', 'E'],
    ['A', 'B', 'C', 'D', 'E'],
    ]

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

def test_function_generic(function_name: str, tests: list, verbose: bool = True) -> Tuple[int, int]:
    """Test suite for an arbitrary function.

    Test harness:
    Takes lists of tests and passees them to a test runner function.
    Tallies totals for passed and failed tests.

    # USE THIS FORMAT TO CREATE GENERALIZED FUNCTION THAT CAN PASS
    # TEST BANKS TO AS ARGUMENTS - REFACTOR FOR DRY PRINCIPLE

    """

    local_passed: int = 0
    local_failed: int = 0

    if verbose:
        logging.debug(f'\nRunning unit tests for {function_name} function.')

    # aliases for type hints
    Result: Tuple[str, str]
    Summary: List[Result] = [ ]

    # run tests using the list of assertions
    Summary.append(test_runner(tests, verbose))
    
    # unpack results and add to counters
    for result in Summary:
        passed, failed = result
        local_passed += passed
        local_failed += failed

    if verbose:
        logging.debug(f'{local_passed} tests passed.')
        logging.debug(f'{local_failed} tests failed.')

    return (local_passed, local_failed)

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

def assert_False():
    """TO BE IMPLEMENTED...

    """
    
    pass

def assert_in():
    """TO BE IMPLEMENTED...

    """
    
    pass

def assert_is():
    """TO BE IMPLEMENTED...

    """
    
    pass

def assert_is_instance():
    """TO BE IMPLEMENTED...

    """
    
    pass

def assert_is_None():
    """TO BE IMPLEMENTED...

    """
    
    pass

def assert_True():
    """TO BE IMPLEMENTED...

    """
    
    pass

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

tests_create_table: List[str] = [
    "assert create_table('string')",
    "assert not create_table(str)",
    "assert not create_table('') #mt string",
    "assert not create_table(' an invalid string!')",
    "assert not create_table(123)",
    "assert not create_table(b'01') #bytes",
    "assert type(create_table('keyword')) in [list, bool]",
    "assert type(create_table('keyword')) not in [str, int, tuple, dict]",
    "assert type(create_table('keyword')) not in [True, None, [ ], '']",
    ]

tests_display_table: List[str] = [
##    "assert_equal(False, display_table, 'string')",
    "assert not display_table(list)",
    "assert not display_table(123)",      
    "assert not display_table({'dict': 'ionary'})",
    "assert not display_table([" +
        "['A', 'B', 'C', 'D', 'E']," +
        "['A', 'B', 'C', 'D', 'E']," +
        "['A', 'B', 'C', 'D', 'E']," +
        "['A', 'B', 'C', 'D', 'E']," +
        "['A', 'B', 'C', 'D', 'E']," +
        "])",
    # bad table structure
    "assert not display_table(['list'])",
    # table data is not of type string
    "assert not display_table(invalid_table_example_1)",
    # not enough rows in table
    "assert not display_table(invalid_table_example_3)",
    # too many items in row
    "assert not display_table(invalid_table_example_4)",
    "assert type(display_table([[1,2],[3,4]])) == " +
        "display_table.__annotations__.get('return')", # bool
    "assert type(display_table(123) == " +
        "display_table.__annotations__.get('return'))", # bool
    "assert type(display_table([[5,6],[7,8]])) is bool",
    "assert type(display_table('false return')) is bool",
    ]

tests_encrypt: List[str] = [
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
    'assert type(encrypt("This should pass", "falcon", "osprey")) == str',
    'assert type(encrypt("Retürns Fälse", "python", "tricks")) is bool', 
    ]

##tests_decode: List[str] = ['']
##
##tests_decrypt: List[str] = ['']
##
##tests_validate_ciphertext: List[str] = ['']

tests_validate_key: List[str] = [
    "assert validate_key('astring')",
    "assert not validate_key(['list', 2])",
    "assert not validate_key(123)",
    "assert not validate_key(True)",
    "assert not validate_key(None)",
    "assert not validate_key({})",
    "assert type(validate_key('foo')) is bool",
    "assert not type(validate_key('bar')) == None",
    "assert not type(validate_key('baz')) == str",
    "assert not type(validate_key('bah')) == int",
    ]

tests_validate_message: List[str] = [
    "assert validate_message('astring')",
    "assert not validate_message('')",
    "assert not validate_message('      ')",        
    "assert not validate_message('    3   ')",     
    "assert validate_message('  c     ')",        
    "assert not validate_message('12345')",        
    "assert not validate_message('!$%*')",
    "assert not validate_message('    1   ')",
    'assert validate_message("This should pass")',
    'assert not validate_message("1.234")',
    'assert not validate_message("accént")',
    'assert not validate_message("umläütö")', 
    'assert not validate_message("文字")',
    "assert not validate_message(['list', 2])",
    "assert not validate_message(123)",
    "assert not validate_message(True)",
    "assert not validate_message(None)",
    "assert not validate_message({})",
    "assert type(validate_message('foo')) is bool",
    "assert not type(validate_message('bar')) == None",
    "assert not type(validate_message('baz')) == str",
    "assert not type(validate_message('bah')) == int",
    ]

##tests_validate_plaintext: List[str] = ['']

tests_validate_table: List[str] = [
    "assert validate_table(valid_table_example)",
    # table data is not of type string
    "assert not validate_table(invalid_table_example_1)",        
    # same letter more than once
    "assert not validate_table(invalid_table_example_2)",        
    # not enough rows in table
    "assert not validate_table(invalid_table_example_3)",
    # too many items in row
    "assert not validate_table(invalid_table_example_4)",
    # bad table structure
    "assert not validate_table(['list'])",
    # wrong parameter type
    "assert not validate_table('string')",
    "assert not validate_table(123)",
    "assert not validate_table(b'01') #bytes",
    "assert type(validate_table('keyword')) in [list, bool]",
    "assert type(validate_table('keyword')) not in [str, int, tuple, dict]",
    "assert type(validate_table('keyword')) not in [True, None, [ ], '']",
    ]

def __main__(verbose: bool = VERBOSE):

    # run unit tests if debugging is on
    if __debug__:

        from time import perf_counter as tpc
    
        start_time = tpc()
        total_failed: int = 0
        total_passed: int = 0

        # get all names beginning with 'tests' from global scope
        for key, value in globals().items():
            if key.startswith('tests'):

                # remove 'tests' from key to get actual function name
                name = key[6:]

                # pass each test bank to test harness
                passed, failed = test_function_generic(name, value, verbose)
              
                # add current test results to total passed and failed
                total_passed += passed
                total_failed += failed

        end_time = tpc()
        total_time = end_time - start_time
        total_tests = total_passed + total_failed

        message = 'Completed %d tests in %.2f seconds:' % \
                  (total_tests, total_time)
        # message = f'Completed {total_tests} tests in {total_time} seconds:'
        border = '-' * len(message)

        logging.debug('') # white space before completion message
        logging.debug(message)
        logging.debug(border)
        logging.debug(f'TOTAL TESTS PASSED: {total_passed}')
        logging.debug(f'TOTAL TESTS FAILED: {total_failed}')

if __name__ == '__main__':
    __main__()
