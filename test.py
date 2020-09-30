#!/usr/bin/env python3

"""Test suite for twosquare.py

This is a suite of unit tests comprised of simple builtin assertions.
The reason for this type of implementation is educational in nature -
simply to gain a better understanding of how to write unit tests
without relying on a module or package to do the heavy lifting and
abstract away the basic underlying processes involved.

Feel free to replace this test suite with your test runner of choice.

Set VERBOSE to True for more detailed logging and print output during
testing.

"""

VERBOSE: bool = True # Could expand this to several levels (e.g. - 0, 1, 2)

# import general types (optional: for type hint checking)
from typing import List
from typing import NoReturn
from typing import Tuple

# use logging for test output
import logging
logging.basicConfig(level=logging.DEBUG, format = '%(message)s',)

# create list of all units to import
import_items: List[str] = [
    '_get_coordinates',
    '_xcrypt',
    'Row',
    'Table',
    'create_table',
    'decrypt',
    'display_table',
    'encrypt',
    'validate_ciphertext',
    'validate_key',
    'validate_message',
    'validate_plaintext',
    'validate_table',
    ]
import_path: str = 'twosquare.twosquare'

# import the items from import path
for item in import_items:
    exec(f'from {import_path} import {item}')

##### GLOBALS #####

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
     ['E', 'F', 'G', 'I', 'K'],
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
  
    except AssertionError:

        if verbose:
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

def test_suite(verbose: bool = True) -> NoReturn:
    """Test suite that runs all unit tests.

    Test suite that gathers unit tests from the global namespace and
    passes them to the test_runner function. These unit tests are lists
    with names that start with the word 'tests' and are comprised of
    list items that are strings each consisting of an assert statement
    or a call to an assert function (e.g. - assert_equal()).
      
    The test suite tallies totals for passed and failed tests and
    displays them via logging.debug statements. It has a verbose setting
    for more detailed output when set to True and when set to False,
    will attempt to suppress the print statement output from the units
    being tested.

    Dependencies:

    From logging:
        debug

    From test (current file):
        run_test
        test_runner

    From time:
        perf_counter

    """

    from time import perf_counter as tpc

    # if verbose is False, supress all print output by redirecting to a buffer
    if not verbose:  
        import io       
        from contextlib import redirect_stdout
        output_buffer = io.StringIO()

    total_failed: int = 0
    total_passed: int = 0

    # start timer for tests
    start_time = tpc()

    # get all names beginning with 'tests' from global scope
    for key, value in globals().items():
        
        if key.startswith('tests'):

            # remove 'tests' from key to get actual function name
            name = key[6:]

            if verbose:
                
                logging.debug(f'\nRunning unit tests for {name} function.')

                # pass each test bank to test harness
                passed, failed = test_runner(value)

                logging.debug(f'\nResults for {name}:')
                logging.debug(f'{passed} tests passed.')
                logging.debug(f'{failed} tests failed.')

            else: # if not verbose

                # use context manager to temporarily redirect print output
                with redirect_stdout(output_buffer):
                    
                    passed, failed = test_runner(value, verbose)
         
            # add current test results to total passed and failed
            total_passed += passed
            total_failed += failed

    end_time = tpc()
    total_time = end_time - start_time
    total_tests = total_passed + total_failed

    # adjust the time format for meaningful display
    adjusted_total_time = total_time
    powers_of_ten = 0
    
    while adjusted_total_time < 0.01:
        powers_of_ten += 3
        adjusted_total_time *= 1000

    # use floor division to set an index for each metric prefix
    # setting 3 as the maximum allowed index value
    index = min((powers_of_ten // 3), 3)

    # use index to select the appropriate prefix
    prefix = ['', 'milli', 'micro', 'nano'][index] 
   
    message = 'Completed %d tests in %.2f %sseconds:' % \
              (total_tests, adjusted_total_time, prefix)
    messsage_border = '-' * len(message)

    logging.debug('') # white space before completion message
    logging.debug(message)
    logging.debug(messsage_border)
    logging.debug(f'TOTAL TESTS PASSED: {total_passed}')
    logging.debug(f'TOTAL TESTS FAILED: {total_failed}')

##### CUSTOM ASSERTIONS #####

def assert_equal(expected_result, func, *args, **kwargs) -> bool:
    """Tests that a function's return value equals an expected result.

    This is a custom assertion designed to display improved output for a
    failed test when more information than a simple PASS / FAIL messsage
    is desired i.e. - when running multiple test cases in a test runner.
    
    To illustrate, if the return value of the function does not equal
    the value of the expected_result, the test case readout displayed
    will include the name of the function, the values of the args used in
    the test, and the expected result.

    Here is an example of output for a failed test case:

    Assume we want to use assert_equal for a custom add function that
    we know works correctly and as intended. We can test that our add
    function fails when it should by plugging the test values into our
    assert_equal function as follows...

    assert_equal(expected_result, func, *args, **kwargs)
    
    assert_equal(2, add, 1, 2)

    Doing this should produce the following failed test case output:

    '---> add(1,2) == 2'

    This info is meant to supplement the 'FAIL' message that is already
    printed by the test runner (when running tests in verbose mode).

    Just to be crystal clear, the function add() when run with the
    parameters provided for the *args, in this case 1 and 2, returned a
    value that did not match the value of the parameter provided for the
    arg expected_result, which was 2 in this case. Ergo, the test case
    failed and the corresponding failure message was displayed. More
    coffee please...

    Returns True if func returns a value that equals expected_result or 
    Returns False otherwise

    """

    try:
        assert expected_result == func(*args, **kwargs)
        
    except AssertionError:
        message = f'---> {func.__name__}('

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

        logging.debug(message)
        
        return False

    except Exception as err:
        
        logging.debug('Unexpected exception raised during test execution:')
        logging.debug(err)
        
        return False

    else:
       
        return True

##### UNIT TESTS FOR TWOSQUARE FUNCTIONS #####

tests__get_coordinates: List[str] = [
    "assert assert_equal((0, 0), _get_coordinates, valid_table_example, 'P')",
    "assert not assert_equal((0,0),_get_coordinates, valid_table_example, 'Z')",
    "assert assert_equal((4, 4), _get_coordinates, valid_table_example, 'Z')",
    "assert assert_equal((-1, -1), _get_coordinates, valid_table_example, '5')",
    # works because _get_coordinates does not enforce data types internally
    "assert assert_equal((0, 0), _get_coordinates, invalid_table_example_1, 1)",
    "assert assert_equal((-1, -1), _get_coordinates, 'bad table', 'P')",
    "assert not assert_equal((-1, -1), _get_coordinates, 123, 'P')", # bad table
    ]

tests__xcrypt: List[str] = [
    "assert _xcrypt('e', 'This should pass', 'falcon', 'osprey')",
    "assert _xcrypt('e', 'This should pass', 'falcon', 'osprey')",
    "assert not _xcrypt('e', 'One invalid keyword', 'keyword', 'pythonista')",
    "assert not _xcrypt('e', 123, 'not', 'string')",
    "assert not _xcrypt('e', '', 'empty', 'plaintex')",
    "assert not _xcrypt('e', '$^&@.', 'only', 'symbol')",
    "assert not _xcrypt('e', '1234', 'only', 'digts')", 
    "assert not _xcrypt('e', '1.234', 'only', 'numbers')",
    "assert not _xcrypt('e', '    ', 'only', 'whitespac')",
    "assert not _xcrypt('e', 'accént', 'foreign', 'chars')",
    "assert not _xcrypt('e', 'umläütö', 'foreign', 'chars')", 
    "assert not _xcrypt('e', '文字', 'foreign', 'chars')",
    "assert type(_xcrypt('e', 'This should pass', 'falcon', 'osprey')) == str",
    "assert type(_xcrypt('e', 'Retürns Fälse', 'python', 'tricks')) is bool",
    "assert _xcrypt('d', 'THISSHOULDPASS', 'key', 'keytwo')",
    "assert not _xcrypt('d', 'THISSHOULDNOTPASS', 'key', 'keytwo')", # key odd length
    "assert not _xcrypt('d', 'THISSHOULDFAIL', '123', 'keytwo')", # digits in key
    "assert not _xcrypt('d', 'THISSHOULDFAIL', 123, 'keytwo')", # key not string
    "assert not _xcrypt('d', 'InVaLiDcIpHeRtExT!', 'key', 'keytwo')", # bad cipher
    "assert not _xcrypt('d', 'IN', 'key', 'keytwo', 0)", # bad type remove_z
    # make sure decoded output correctly matches expected results
    "assert _xcrypt('d', 'BHATOKTEDZ','python', 'algo') == 'DECRYPTED'",
    "assert _xcrypt('d', 'ENQKOW', 'python', 'algo', False) == 'IIMMYZ'",
    ]

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

tests_decrypt: List[str] = [
    "assert decrypt('THISSHOULDPASS', 'key', 'keytwo')",
    "assert not decrypt('THISSHOULDNOTPASS', 'key', 'keytwo')", # key odd length
    "assert not decrypt('THISSHOULDFAIL', '123', 'keytwo')", # digits in key
    "assert not decrypt('THISSHOULDFAIL', 123, 'keytwo')", # key not string
    "assert not decrypt('InVaLiDcIpHeRtExT!', 'key', 'keytwo')", # bad cipher
    "assert not decrypt('IN', 'key', 'keytwo', 0)", # bad type remove_z
    # make sure decoded output correctly matches expected results
    "assert decrypt('BHATOKTEBPGQLBGE','python', 'algo') == 'DECRYPTEDMESSAGE'",
    "assert decrypt('ENQKPKOHDV', 'python', 'algo') == 'IIMMYIOHN'",
    "assert decrypt('ENQKPKOHDV', 'python', 'algo', False) == 'IIMMYIOHNZ'",
    ]

tests_display_table: List[str] = [
    "assert assert_equal(False, display_table, 'string')",
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

tests_validate_ciphertext: List[str] = [
    "assert assert_equal(True, validate_ciphertext, 'VALID')",
    "assert assert_equal(False, validate_ciphertext, 'InVaLid')", # not capitals
    "assert assert_equal(False, validate_ciphertext, '')", # empty string
    "assert assert_equal(False, validate_ciphertext, 'NO!!!??')", # punctuation
    "assert assert_equal(False, validate_ciphertext, 'B A D')", # white space
    "assert assert_equal(False, validate_ciphertext, 'áéíóúü')", # unicode chars
    "assert assert_equal(False, validate_ciphertext, '123')", # digits in string
    "assert assert_equal(False, validate_ciphertext, 123)", # not a string    
    ]

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

tests_validate_plaintext: List[str] = [
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

##### Inner functions in Twosquare main program #####

### CAN'T AUTO TEST THESE ONES - REQUIRE USER INTERACTION
##tests__create_key: List[str] = ['']
##tests__get_key: List[str] = ['']
##tests__get_response: List[str] = ['']
##tests__get_selection: List[str] = ['']
##tests__load_file: List[str] = ['']
##tests__save_file: List[str] = ['']
### LAST TWO COULD BE TESTED IF MOVE TO GLOBAL SCOPE AND REFACTOR FOR
### FILENAME PROVIDED AS PARAMETER OPTION INSTEAD OF GETTING USER INPUT 

### THESE THREE ARE IMPLEMENTATION DETAILS OF MAIN PROGRAM
##tests__display_keys: List[str] = ['']
##tests__display_menu: List[str] = ['']
##tests__display_title: List[str] = ['']

### TESTS FOR MAIN FUNCTION ARE INTEGRATION TESTS, NOT UNIT TESTS
##tests___main__: List[str] = ['']

def __main__(verbose: bool = VERBOSE):

    # run unit tests if debugging is on
    if __debug__:

        test_suite(verbose)

    else:

        logging.debug('Unit tests off: __debug__ is set to False.')

if __name__ == '__main__':
    __main__()
