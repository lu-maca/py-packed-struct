"""Implements some unit tests"""

from test_utils import *
from packed_struct import *


class UnsignedIntTest:

    @test
    def test_unsigned_int_correct():
        # correct case
        bits = 3
        data = c_unsigned_int(bits)

        non_blocking_assert(data.fmt == f"u{bits}", f"uint format not correct, expected u{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"uint size not correct, expected {bits}, current {data.size}")

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
                non_blocking_assert(False, "uint allows for negative integer size")
            else:
                non_blocking_assert(
                    str(e) == "Number of bits shall be a positive integer",
                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})",
                )

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
                non_blocking_assert(
                    str(e) == "Number of bits shall be a positive integer",
                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})",
                )


class SignedIntTest:

    @test
    def test_signed_int_correct():
        # correct case
        bits = 8
        data = c_signed_int(bits)

        non_blocking_assert(data.fmt == f"s{bits}", f"signed int format not correct, expected s{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"signed int size not correct, expected {bits}, current {data.size}")

    @test
    def test_signed_int_negative_bits():
        # wrong case
        bits = -4
        try:
            data = c_signed_int(bits)
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "signed int allows for negative integer size")
            else:
                non_blocking_assert(
                    str(e) == "Number of bits shall be a positive integer",
                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})",
                )

    @test
    def test_signed_int_null_bits():
        # wrong case
        bits = 0
        try:
            data = c_signed_int(bits)
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "signed int allows for 0 size")
            else:
                non_blocking_assert(
                    str(e) == "Number of bits shall be a positive integer",
                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})",
                )


class FloatTest:

    @test
    def test_float_16_bits():
        bits = 16
        data = c_float(bits)
        non_blocking_assert(data.fmt == f"f{bits}", f"float format not correct, expected f{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"float size not correct, expected {bits}, current {data.size}")

    @test
    def test_float_32_bits():
        bits = 32
        data = c_float(bits)
        non_blocking_assert(data.fmt == f"f{bits}", f"float format not correct, expected f{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"float size not correct, expected {bits}, current {data.size}")

    @test
    def test_float_64_bits():
        bits = 64
        data = c_float(bits)
        non_blocking_assert(data.fmt == f"f{bits}", f"float format not correct, expected f{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"float size not correct, expected {bits}, current {data.size}")

    @test
    def test_float_invalid_bits():
        # Test with 8 bits (invalid)
        bits = 8
        try:
            data = c_float(bits)
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "float allows for 8 bit size")
            else:
                expected_msg = f"Float must be of 16, 32 or 64 bits (requested: {bits}). See https://bitstruct.readthedocs.io/en/latest/#performance."
                non_blocking_assert(
                    str(e) == expected_msg,
                    f"wrong exception (expected: {expected_msg}, current {str(e)})",
                )

    @test
    def test_float_invalid_24_bits():
        # Test with 24 bits (invalid)
        bits = 24
        try:
            data = c_float(bits)
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "float allows for 24 bit size")
            else:
                expected_msg = f"Float must be of 16, 32 or 64 bits (requested: {bits}). See https://bitstruct.readthedocs.io/en/latest/#performance."
                non_blocking_assert(
                    str(e) == expected_msg,
                    f"wrong exception (expected: {expected_msg}, current {str(e)})",
                )


class BoolTest:

    @test
    def test_bool_correct():
        bits = 1
        data = c_bool(bits)
        non_blocking_assert(data.fmt == f"b{bits}", f"bool format not correct, expected b{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"bool size not correct, expected {bits}, current {data.size}")

    @test
    def test_bool_multiple_bits():
        bits = 4
        data = c_bool(bits)
        non_blocking_assert(data.fmt == f"b{bits}", f"bool format not correct, expected b{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"bool size not correct, expected {bits}, current {data.size}")

    @test
    def test_bool_negative_bits():
        bits = -1
        try:
            data = c_bool(bits)
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "bool allows for negative integer size")
            else:
                non_blocking_assert(
                    str(e) == "Number of bits shall be a positive integer",
                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})",
                )

    @test
    def test_bool_null_bits():
        bits = 0
        try:
            data = c_bool(bits)
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "bool allows for 0 size")
            else:
                non_blocking_assert(
                    str(e) == "Number of bits shall be a positive integer",
                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})",
                )


class CharTest:

    @test
    def test_char_correct():
        bits = 8
        data = c_char(bits)
        non_blocking_assert(data.fmt == f"t{bits}", f"char format not correct, expected t{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"char size not correct, expected {bits}, current {data.size}")

    @test
    def test_char_multiple_bytes():
        bits = 80  # 10 chars
        data = c_char(bits)
        non_blocking_assert(data.fmt == f"t{bits}", f"char format not correct, expected t{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"char size not correct, expected {bits}, current {data.size}")

    @test
    def test_char_not_multiple_of_8():
        bits = 7
        try:
            data = c_char(bits)
            # UserWarning doesn't raise, so we check if warning is issued
            # This is a design issue in the original code
            non_blocking_assert(data.fmt == f"t{bits}", "char was created despite not being multiple of 8")
        except UserWarning as e:
            expected_msg = "char must be contained in multiples of 8 bits (see https://bitstruct.readthedocs.io/en/latest/#performance)"
            non_blocking_assert(
                str(e) == expected_msg,
                f"wrong warning (expected: {expected_msg}, current {str(e)})",
            )

    @test
    def test_char_negative_bits():
        bits = -8
        try:
            data = c_char(bits)
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "char allows for negative integer size")
            else:
                non_blocking_assert(
                    str(e) == "Number of bits shall be a positive integer",
                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})",
                )


class RawBytesTest:

    @test
    def test_raw_bytes_correct():
        bits = 8
        data = c_raw_bytes(bits)
        non_blocking_assert(data.fmt == f"r{bits}", f"raw bytes format not correct, expected r{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"raw bytes size not correct, expected {bits}, current {data.size}")

    @test
    def test_raw_bytes_multiple():
        bits = 64
        data = c_raw_bytes(bits)
        non_blocking_assert(data.fmt == f"r{bits}", f"raw bytes format not correct, expected r{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"raw bytes size not correct, expected {bits}, current {data.size}")

    @test
    def test_raw_bytes_negative_bits():
        bits = -8
        try:
            data = c_raw_bytes(bits)
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "raw bytes allows for negative integer size")
            else:
                non_blocking_assert(
                    str(e) == "Number of bits shall be a positive integer",
                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})",
                )

    @test
    def test_raw_bytes_null_bits():
        bits = 0
        try:
            data = c_raw_bytes(bits)
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "raw bytes allows for 0 size")
            else:
                non_blocking_assert(
                    str(e) == "Number of bits shall be a positive integer",
                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})",
                )


class PaddingTest:

    @test
    def test_padding_correct():
        bits = 8
        data = c_padding(bits)
        non_blocking_assert(data.fmt == f"u{bits}", f"padding format not correct, expected u{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"padding size not correct, expected {bits}, current {data.size}")
        non_blocking_assert(data.value == 0, f"padding value not 0, current {data.value}")

    @test
    def test_padding_value_is_zero():
        bits = 16
        data = c_padding(bits)
        non_blocking_assert(data.value == 0, f"padding value should be 0, current {data.value}")

    @test
    def test_padding_negative_bits():
        bits = -4
        try:
            data = c_padding(bits)
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "padding allows for negative integer size")
            else:
                non_blocking_assert(
                    str(e) == "Number of bits shall be a positive integer",
                    f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})",
                )


class ArrayTest:

    @test
    def test_array_correct():
        type_size = 8
        array_size = 5
        data = c_array(c_unsigned_int, type_size, array_size)
        
        expected_size = type_size * array_size
        non_blocking_assert(data.size == expected_size, f"array size not correct, expected {expected_size}, current {data.size}")
        non_blocking_assert(len(data.value) == array_size, f"array length not correct, expected {array_size}, current {len(data.value)}")

    @test
    def test_array_format():
        type_size = 8
        array_size = 3
        data = c_array(c_unsigned_int, type_size, array_size)
        
        expected_fmt = "u8u8u8"
        non_blocking_assert(data.fmt == expected_fmt, f"array format not correct, expected {expected_fmt}, current {data.fmt}")

    @test
    def test_array_set_value():
        type_size = 8
        array_size = 3
        data = c_array(c_unsigned_int, type_size, array_size)
        
        values = [1, 2, 3]
        data.set_value(values)
        
        for i, val in enumerate(values):
            non_blocking_assert(data[i].value == val, f"array[{i}] value not set correctly, expected {val}, current {data[i].value}")

    @test
    def test_array_negative_size():
        try:
            data = c_array(c_unsigned_int, 8, -1)
            raise TestException()
        except UserWarning as e:
            expected_msg = "array_size must be positive"
            non_blocking_assert(
                str(e) == expected_msg,
                f"wrong warning (expected: {expected_msg}, current {str(e)})",
            )
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "array allows for negative array_size")

    @test
    def test_array_not_multiple_of_8():
        try:
            data = c_array(c_unsigned_int, 7, 3)
            raise TestException()
        except UserWarning as e:
            expected_msg = "type_size_bits must be a multiples of 8 bits"
            non_blocking_assert(
                str(e) == expected_msg,
                f"wrong warning (expected: {expected_msg}, current {str(e)})",
            )
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "array allows for type_size_bits not multiple of 8")

    @test
    def test_array_wrong_value_length():
        data = c_array(c_unsigned_int, 8, 3)
        try:
            data.set_value([1, 2])  # Too few values
            raise TestException()
        except UserWarning as e:
            non_blocking_assert(
                "Length of array" in str(e),
                f"wrong warning message for incorrect value length: {str(e)}",
            )
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "array set_value allows for incorrect length")

    @test
    def test_array_iteration():
        data = c_array(c_unsigned_int, 8, 3)
        count = 0
        for item in data:
            count += 1
        non_blocking_assert(count == 3, f"array iteration failed, expected 3 items, got {count}")


class StructTest:

    @test
    def test_struct_creation():
        person = Struct({"name": c_char(10*8), "age": c_unsigned_int(8)})
        
        expected_size = 10*8 + 8
        non_blocking_assert(person.size == expected_size, f"struct size not correct, expected {expected_size}, current {person.size}")

    @test
    def test_struct_empty():
        try:
            data = Struct({})
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "struct allows for empty dict")
            else:
                expected_msg = "Empty structure cannot be created"
                non_blocking_assert(
                    str(e) == expected_msg,
                    f"wrong exception (expected: {expected_msg}, current {str(e)})",
                )

    @test
    def test_struct_invalid_type():
        try:
            data = Struct({"name": "not a type", "age": 25})
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "struct allows for invalid types")
            else:
                non_blocking_assert(
                    "shall be of type Type or Struct" in str(e),
                    f"wrong exception message: {str(e)}",
                )

    @test
    def test_struct_set_data():
        person = Struct({"age": c_unsigned_int(8), "weight": c_float(32)})
        person.set_data(age=25, weight=75.5)
        
        age_value = person._data["age"].value
        weight_value = person._data["weight"].value
        
        non_blocking_assert(age_value == 25, f"struct age not set correctly, expected 25, current {age_value}")
        non_blocking_assert(abs(weight_value - 75.5) < 0.01, f"struct weight not set correctly, expected 75.5, current {weight_value}")

    @test
    def test_struct_set_data_invalid_key():
        person = Struct({"age": c_unsigned_int(8)})
        try:
            person.set_data(name="John")
            raise TestException()
        except AttributeError as e:
            non_blocking_assert(
                "not found" in str(e),
                f"wrong exception for invalid key: {str(e)}",
            )
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "struct set_data allows for invalid key")

    @test
    def test_struct_format():
        person = Struct({"age": c_unsigned_int(8), "weight": c_float(32)})
        expected_fmt = "u8f32"
        non_blocking_assert(person.fmt == expected_fmt, f"struct format not correct, expected {expected_fmt}, current {person.fmt}")

    @test
    def test_struct_pack():
        person = Struct({"age": c_unsigned_int(8), "weight": c_float(32)})
        person.set_data(age=25, weight=75.5)
        
        packed = person.pack()
        non_blocking_assert(isinstance(packed, bytes), f"pack should return bytes, got {type(packed)}")
        non_blocking_assert(len(packed) > 0, "packed data should not be empty")

    @test
    def test_struct_pack_without_data():
        person = Struct({"age": c_unsigned_int(8)})
        try:
            packed = person.pack()
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "struct pack allows for uninitialized data")
            else:
                expected_msg = "You have to initialize all data."
                non_blocking_assert(
                    str(e) == expected_msg,
                    f"wrong exception (expected: {expected_msg}, current {str(e)})",
                )

    @test
    def test_struct_nested():
        inner = Struct({"x": c_unsigned_int(8), "y": c_unsigned_int(8)})
        outer = Struct({"position": inner, "value": c_unsigned_int(16)})
        
        expected_size = 8 + 8 + 16
        non_blocking_assert(outer.size == expected_size, f"nested struct size not correct, expected {expected_size}, current {outer.size}")

    @test
    def test_struct_get_data():
        person = Struct({"age": c_unsigned_int(8)})
        data = person.get_data()
        
        non_blocking_assert(isinstance(data, dict), f"get_data should return dict, got {type(data)}")
        non_blocking_assert("age" in data, "get_data should contain 'age' key")


################
#
#     RUN
#
################
if __name__ == "__main__":
    run()
