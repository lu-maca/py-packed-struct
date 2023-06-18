"""In this example we create a C bit field struct. The respective C 
bit field is the following

struct {
    uint8_t two_bits_uint: 2;
    int8_t four_bits_signed_int: 4;
    int8_t two_bits_signed_int: 2;
}
"""

from packed_struct import *

s = Struct(
    {
        "two_bits_uint": c_unsigned_int(2),
        "four_bits_signed_int": c_signed_int(4),
        "two_bits_signed_int": c_signed_int(2)
    }
)

# set data
s.set_data(
    two_bits_uint = 3, 
    four_bits_signed_int = -8, 
    two_bits_signed_int = 1
)

# pack them (only one byte: byte endianness not relevant)
bytes_str = s.pack()

print(bytes_str)


"""
Comment:

    b'\xe1'

    This is the correct result: 
        1     1     |    1    0    0    0    |    0    1
    two_bits_uint     four_bits_signed_int     two_bits_signed_int

    This binary number is equal to 225 (unsigned) or 0xE1, which
    is the result printed.
"""