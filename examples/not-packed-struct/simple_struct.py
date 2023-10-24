"""In this example we create a C simple struct (not packed), padded 
"""

from packed_struct import *

s = Struct(
    {
        "x": c_unsigned_int(8),
        "y": c_signed_int(16),
        "z": c_signed_int(8)
    }
)

# # set data
s.set_data(
    x = 1, 
    y = 1, 
    z = 0
)

# # pack them 
bytes_str = s.pack("little")

print(bytes_str)

print(s.size)


"""
Comment:

"""