""" Function to generate Enum types.

From http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python

>>> Numbers = enum('ZERO', 'ONE', 'TWO', THREE='three')
>>> Numbers.ZERO
0
>>> Numbers.ONE
1
>>> Numbers.reverse_mapping['three']
THREE
"""


def enum(*sequential, **named):
    """ Generate an enum type.

    Arguements:
        sequential: A list of strings that should generate sequential values.
            This is automatically any normal args passed into the function eg:
                >>> Numbers = enum('ZERO', 'ONE', 'TWO')
                sequential = ['ZERO', 'ONE', 'TWO']
        sequential type: list of strings
        named:  A dictionary of values that should have specific values.
            This is automatically any keyword args passed into the function eg:
                >>> Numbers = enum(THREE='three', FOUR=4)
                named = {THREE: 'three', FOUR: 4}
        named type: list of strings
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)
