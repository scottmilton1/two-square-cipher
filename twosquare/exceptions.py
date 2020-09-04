#!/usr/bin/env python3

"""Custom exception classes for the twosquare module.

"""

class BadValueError(ValueError):
    """Raised when the value is flagrantly and absolutely invalid.

    Attributes:
        message -- explanation of the error
        subtext -- humorous subtext message to accompany the error info

    """

    def __init__(self, message = ''):
        self.message = message
        
        if len(message) == 0: # default message
            self.message =  \
                'Raised when the value is flagrantly and absolutely invalid.'
            
        self.subtext = 'You have attempted to exceed the limits ' + \
                        'of reality imposed by the Architect.\n' + \
                        'Neo could bend the Matrix ' + \
                        'to his will, but can you?'     
     
        super().__init__(self.message)

    def __repr__(self):
        return f'{self.message!r}'

class FooBarError(Exception):
    """Raised when something really bad happens.

    Attributes:
        message -- explanation of the error
        subtext -- humorous subtext message to accompany the error info

    """

    def __init__(self, message = 'Raised when something really bad happens.'):
        self.message = message
        
        self.subtext = '\nI do not like green eggs and ham. ' + \
                       'This should never happen, but if it does, ' + \
                       'it is an unforeseen error. ' + \
                       "It's okay to panic!"
        
        super().__init__(self.message)

    def __repr__(self):
        return f'{self.message!r}'     
    
class StakesTooHighError(IndexError):
    """Raised when the stakes are just too dang high!

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message):
        self.message = message if len(message) > 0 else \
            'Raised when the stakes are just too dang high!'     
        
        super().__init__(self.message)

    def __repr__(self):
        return f'{self.message!r}'

class TypeMismatchError(TypeError):
    """Raised when someone tries to put a square peg in a round hole.

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message):
        self.message = message if len(message) > 0 else \
            'Raised when someone tries to put a square peg in a round hole.'        
       
        super().__init__(self.message)

    def __repr__(self):
        return f'{self.message!r}'

