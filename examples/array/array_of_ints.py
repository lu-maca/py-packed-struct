"""Example: array of integers

Shows how to use c_array with a primitive type to represent a fixed-size
sequence of values — equivalent to the following C struct:

    struct {
        uint8_t  samples[4];
        uint16_t checksum;
    }
"""

from packed_struct import *

msg = Struct(
    {
        "samples": c_array(c_unsigned_int(8), 4),
        "checksum": c_unsigned_int(16),
    }
)

# Set the array elements individually …
msg["samples"][0].set_value(10)
msg["samples"][1].set_value(20)
msg["samples"][2].set_value(30)
msg["samples"][3].set_value(40)

# … or all at once via set_data()
msg.set_data(samples=[10, 20, 30, 40], checksum=0xABCD)

packed = msg.pack()
print("packed :", packed.hex())   # 0a141e28abcd

# Unpack back into a fresh struct
msg2 = Struct(
    {
        "samples": c_array(c_unsigned_int(8), 4),
        "checksum": c_unsigned_int(16),
    }
)
msg2.unpack(packed)

print("samples:", [msg2["samples"][i] for i in range(4)])  # [10, 20, 30, 40]
print("checksum:", hex(msg2["checksum"]))                         # 0xabcd
print(msg2["checksum"] == 0xABCD)
print(msg2["samples"][2] == 30) 