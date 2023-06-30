"""Implements some unit tests"""
from test_utils import *
from packed_struct import *

class TypesTest:
    
    @test
    def test_unsigned_int():
        bits = 3
        data = c_unsigned_int(bits)
        
        non_blocking_assert(data.fmt == f"u{bits}", f"uint format not correct, expected u{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"uint size not correct, expected {bits}, current {data.size}")

        bits = -4
        try:
            data = c_unsigned_int(bits)
        except Exception as e:
            non_blocking_assert(str(e) == "Number of bits shall be unsigned int", "Number of bits shall be a positive integer")
        
        bits = 0
        try:
            data = c_unsigned_int(bits)
        except Exception as e:
            non_blocking_assert(str(e) == "Number of bits shall be unsigned int", "Number of bits shall be a positive integer")




################
# 
#     RUN
#
################
if __name__ == "__main__":
    run()