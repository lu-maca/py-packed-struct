"""Implements some unit tests"""
from test_utils import *
from packed_struct import *


class TypesTest:

    @test
    def test_unsigned_int_correct():
        # correct case
        bits = 3
        data = c_unsigned_int(bits)

        non_blocking_assert(
            data.fmt == f"u{bits}", f"uint format not correct, expected u{bits}, current {data.fmt}")
        non_blocking_assert(
            data.size == bits, f"uint size not correct, expected {bits}, current {data.size}")

    @test
    def test_unsigned_int_negative_bits():
        # wrong case
        bits = -4
        try:
            # this should fail
            data = c_unsigned_int(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(
                    False, "uint allows for negative integer size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def test_unsigned_int_null_bits():
        # wrong case
        bits = 0
        try:
            # this should fail
            data = c_unsigned_int(bits)
            # if it reach this point, it's not failed
            raise TestException()

        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "uint allows for 0 size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def test_signed_int():
        # correct case
        bits = 3
        data = c_signed_int(bits)

        non_blocking_assert(
            data.fmt == f"s{bits}", f"int format not correct, expected s{bits}, current {data.fmt}")
        non_blocking_assert(
            data.size == bits, f"int size not correct, expected {bits}, current {data.size}")

    @test
    def test_signed_int_negative_bits():
        # wrong case
        bits = -4
        try:
            # this should fail
            data = c_signed_int(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(
                    False, "int allows for negative integer size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def test_signed_int_null_bits():
        # wrong case
        bits = 0
        try:
            # this should fail
            data = c_signed_int(bits)
            # if it reach this point, it's not failed
            raise TestException()

        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "int allows for 0 size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def test_float_16bits():
        # correct case
        bits = 16
        data = c_float(bits)

        non_blocking_assert(
            data.fmt == f"f{bits}", f"float format not correct, expected f{bits}, current {data.fmt}")
        non_blocking_assert(
            data.size == bits, f"float size not correct, expected {bits}, current {data.size}")

    @test
    def test_float_32bits():
        # correct case
        bits = 32
        data = c_float(bits)

        non_blocking_assert(
            data.fmt == f"f{bits}", f"float format not correct, expected f{bits}, current {data.fmt}")
        non_blocking_assert(
            data.size == bits, f"float size not correct, expected {bits}, current {data.size}")

    @test
    def test_float_64bits():
        # correct case
        bits = 64
        data = c_float(bits)

        non_blocking_assert(
            data.fmt == f"f{bits}", f"float format not correct, expected f{bits}, current {data.fmt}")
        non_blocking_assert(
            data.size == bits, f"float size not correct, expected {bits}, current {data.size}")

    @test
    def test_float_wrong_bits():
        # correct case
        bits = 31
        try:
            # this should fail
            data = c_float(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(
                    False, "float allows for bits size not in [16, 32, 64]")
            else:
                non_blocking_assert(str(e) == f"Float must be of 16, 32 or 64 bits (requested: {bits}). See https://bitstruct.readthedocs.io/en/latest/#performance.",
                                    f"wrong exception (expected: Float must be of 16, 32 or 64 bits (requested: {bits}). See https://bitstruct.readthedocs.io/en/latest/#performance., current {str(e)})")

    @test
    def test_float_negative_bits():
        # wrong case
        bits = -4
        try:
            # this should fail
            data = c_float(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(
                    False, "int allows for negative integer size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def test_float_null_bits():
        # wrong case
        bits = 0
        try:
            # this should fail
            data = c_float(bits)
            # if it reach this point, it's not failed
            raise TestException()

        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "int allows for 0 size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")
    
    @test
    def test_bool():
        # correct case
        bits = 3
        data = c_bool(bits)

        non_blocking_assert(
            data.fmt == f"b{bits}", f"bool format not correct, expected b{bits}, current {data.fmt}")
        non_blocking_assert(
            data.size == bits, f"bool size not correct, expected {bits}, current {data.size}")

    @test
    def test_bool_negative_bits():
        # wrong case
        bits = -4
        try:
            # this should fail
            data = c_bool(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(
                    False, "bool allows for negative integer size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def test_bool_null_bits():
        # wrong case
        bits = 0
        try:
            # this should fail
            data = c_bool(bits)
            # if it reach this point, it's not failed
            raise TestException()

        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "bool allows for 0 size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")
    
    @test
    def test_char():
        # correct case
        bits = 8
        data = c_char(bits)

        non_blocking_assert(
            data.fmt == f"b{bits}", f"char format not correct, expected t{bits}, current {data.fmt}")
        non_blocking_assert(
            data.size == bits, f"char size not correct, expected {bits}, current {data.size}")
        
    @test
    def test_char_non_8bits_multiple():
        bits = 4
        try:
            # this should fail
            data = c_bool(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(
                    False, "char allows for bits size that are not multiple of 8 bits")
            else:
                non_blocking_assert(str(e) == "char must be contained in multiples of 8 bits (see https://bitstruct.readthedocs.io/en/latest/#performance)",
                                    f"wrong exception (expected: char must be contained in multiples of 8 bits (see https://bitstruct.readthedocs.io/en/latest/#performance), current {str(e)})")

    @test
    def test_char_negative_bits():
        # wrong case
        bits = -4
        try:
            # this should fail
            data = c_bool(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(
                    False, "char allows for negative integer size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def test_char_null_bits():
        # wrong case
        bits = 0
        try:
            # this should fail
            data = c_char(bits)
            # if it reach this point, it's not failed
            raise TestException()

        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "char allows for 0 size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")
    
    @test
    def test_raw_bytes():
        # correct case
        bits = 8
        data = c_raw_bytes(bits)

        non_blocking_assert(
            data.fmt == f"{bits}", f"raw_bytes format not correct, expected r{bits}, current {data.fmt}")
        non_blocking_assert(
            data.size == bits, f"raw_bytes size not correct, expected {bits}, current {data.size}")
        
    @test
    def test_raw_bytes_non_8bits_multiple():
        bits = 4
        try:
            # this should fail
            data = c_raw_bytes(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(
                    False, "raw_bytes allows for bits size that are not multiple of 8 bits")
            else:
                non_blocking_assert(str(e) == "raw_bytes must be contained in multiples of 8 bits (see https://bitstruct.readthedocs.io/en/latest/#performance)",
                                    f"wrong exception (expected: raw_bytes must be contained in multiples of 8 bits (see https://bitstruct.readthedocs.io/en/latest/#performance), current {str(e)})")

    @test
    def test_raw_bytes_negative_bits():
        # wrong case
        bits = -4
        try:
            # this should fail
            data = c_raw_bytes(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(
                    False, "raw_bytes allows for negative integer size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def test_raw_bytes_null_bits():
        # wrong case
        bits = 0
        try:
            # this should fail
            data = c_raw_bytes(bits)
            # if it reach this point, it's not failed
            raise TestException()

        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "raw_bytes allows for 0 size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def test_padding():
        # correct case
        bits = 3
        data = c_padding(bits)

        non_blocking_assert(
            data.fmt == f"u{bits}", f"padding format not correct, expected b{bits}, current {data.fmt}")
        non_blocking_assert(
            data.size == bits, f"padding size not correct, expected {bits}, current {data.size}")

    @test
    def test_padding_negative_bits():
        # wrong case
        bits = -4
        try:
            # this should fail
            data = c_padding(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(
                    False, "padding allows for negative integer size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def test_padding_null_bits():
        # wrong case
        bits = 0
        try:
            # this should fail
            data = c_padding(bits)
            # if it reach this point, it's not failed
            raise TestException()

        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "padding allows for 0 size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer",
                                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    @test
    def unpack_test_correct():
        pass


################
#
#     RUN
#
################
if __name__ == "__main__":
    run()
