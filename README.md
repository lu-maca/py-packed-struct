# py-packed-struct

[![PyPI version](https://badge.fury.io/py/py-packed-struct.svg)](https://badge.fury.io/py/py-packed-struct)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/lu-maca/py-packed-struct/actions/workflows/python-package.yml/badge.svg)](https://github.com/lu-maca/py-packed-struct/actions/workflows/python-package.yml)

A Python library for defining and manipulating C-like packed structures with support for bit-fields, nested structures, and various data types.

## Overview

**py-packed-struct** provides an elegant, Pythonic interface for working with binary data structures that are compatible with C's packed structures. Built on top of the [`bitstruct`](https://bitstruct.readthedocs.io/en/latest/index.html) library, it eliminates the need to manually craft format strings while offering powerful features like nested structures, bit-field manipulation, and automatic serialization/deserialization.

### Key Features

- **Intuitive API**: Define structures using native Python syntax instead of cryptic format strings
- **Type Safety**: Strongly-typed data fields with validation
- **Bit-Level Precision**: Full support for bit-fields and non-byte-aligned data
- **Nested Structures**: Create complex hierarchical data structures
- **Endianness Control**: Support for big-endian, little-endian, and native byte order
- **Array Support**: Built-in support for fixed-size arrays
- **C Compatibility**: Generate structures that are binary-compatible with C's `__attribute__((packed))` structs
- **Zero Dependencies**: Only requires `bitstruct` package

## Installation

Install via pip:

```bash
pip install py-packed-struct
```

Requirements:
- Python >= 3.8
- bitstruct

## Quick Start

Here's a comparison between the standard library's `struct` module and `py-packed-struct`:

```python
# Using Python's built-in struct module
from struct import pack
one, two, three = 1, 2, 3
data = pack(">bhl", one, two, three)
# Result: b'\x01\x00\x02\x00\x00\x00\x03'

# Using py-packed-struct
from packed_struct import Struct, c_signed_int

s = Struct({
    "one": c_signed_int(8),
    "two": c_signed_int(16),
    "three": c_signed_int(32)
})
s.set_data(one=1, two=2, three=3)
data = s.pack(byte_endianness="big")
# Result: b'\x01\x00\x02\x00\x00\x00\x03'

# Unpack back to dictionary
values = s.unpack(data, byte_endianness="big")
# Result: {'one': 1, 'two': 2, 'three': 3}
```

## API Reference

### Data Types

All data types inherit from the base `Type` class and support bit-level precision:

#### Integer Types

- **`c_unsigned_int(bits)`**: Unsigned integer
  ```python
  age = c_unsigned_int(8)  # 8-bit unsigned int (0-255)
  ```

- **`c_signed_int(bits)`**: Signed integer (two's complement)
  ```python
  temperature = c_signed_int(16)  # 16-bit signed int (-32768 to 32767)
  ```

#### Floating Point Types

- **`c_float(bits)`**: IEEE 754 floating-point number
  - Supported sizes: 16, 32, or 64 bits
  ```python
  weight = c_float(32)  # 32-bit float
  ```

#### Boolean Type

- **`c_bool(bits)`**: Boolean value
  ```python
  flag = c_bool(1)  # Single bit boolean
  ```

#### Character/Text Types

- **`c_char(bits)`**: Text string (UTF-8 encoded)
  - Size must be multiple of 8 bits
  ```python
  name = c_char(80)  # 10-character string (10 * 8 bits)
  ```

#### Raw Data Type

- **`c_raw_bytes(bits)`**: Raw binary data
  ```python
  buffer = c_raw_bytes(64)  # 8 bytes of raw data
  ```

#### Padding

- **`c_padding(bits)`**: Reserved/padding space (always zero)
  ```python
  padding = c_padding(16)  # 16 bits of padding
  ```

#### Arrays

- **`c_array(type, type_size_bits, array_size)`**: Fixed-size array
  - `type_size_bits` must be multiple of 8
  ```python
  # Array of 5 unsigned 8-bit integers
  values = c_array(c_unsigned_int, 8, 5)
  values.set_value([10, 20, 30, 40, 50])
  ```

### Struct Class

The `Struct` class represents a collection of typed fields:

```python
person = Struct({
    "name": c_char(10*8),      # 10 characters
    "age": c_unsigned_int(8),   # 1 byte
    "height": c_float(32)       # 4 bytes
})
```

#### Methods

- **`set_data(**kwargs)`**: Set values for fields
  ```python
  person.set_data(name="Alice", age=30, height=165.5)
  ```

- **`pack(byte_endianness="=")`**: Serialize to bytes
  - `byte_endianness`: `"big"`, `"little"`, or `"="` (native)
  ```python
  binary_data = person.pack(byte_endianness="big")
  ```

- **`unpack(byte_string, byte_endianness="=", text_encoding="utf-8", text_errors="strict")`**: Deserialize from bytes
  ```python
  values = person.unpack(binary_data, byte_endianness="big")
  ```

- **`get_data()`**: Get dictionary of all fields
  ```python
  fields = person.get_data()
  ```

#### Properties

- **`size`**: Total size in bits
- **`fmt`**: Format string (bitstruct format)
- **`value`**: List of all field values

#### Accessing Field Values

```python
# Using dictionary syntax
name = person["name"]

# Using attribute syntax
age = person.age
```

### Nested Structures

Structures can be nested to create complex hierarchical data:

```python
address = Struct({
    "street": c_char(20*8),
    "number": c_unsigned_int(16)
})

person = Struct({
    "name": c_char(10*8),
    "age": c_unsigned_int(8),
    "address": address  # Nested structure
})

person.set_data(name="Bob", age=25)
person["address"].set_data(street="Main St", number=123)
```

## Examples

### Bit-Fields

Working with individual bits and bit-fields:

```python
from packed_struct import Struct, c_unsigned_int, c_bool

# Define a status register with bit-fields
status = Struct({
    "enabled": c_bool(1),      # 1 bit
    "ready": c_bool(1),        # 1 bit
    "error": c_bool(1),        # 1 bit
    "reserved": c_unsigned_int(5),  # 5 bits padding
    "code": c_unsigned_int(8)  # 8 bits
})

status.set_data(enabled=True, ready=False, error=False, reserved=0, code=42)
packed = status.pack()
```

### Nested Structures Example

A complete example demonstrating nested structures (from [`examples/mqtt`](https://github.com/lu-maca/py-packed-struct/tree/main/examples/mqtt)):

```python
from packed_struct import Struct, c_char, c_unsigned_int, c_float

# Define nested shoe structure
shoes = Struct({
    "number": c_unsigned_int(8),
    "brand": c_char(10*8)
})

# Define clothing structure with nested shoes
clothes = Struct({
    "tshirt": c_char(10*8),
    "shorts": c_char(10*8),
    "shoes": shoes  # Nested structure
})

# Define person structure with nested clothes
person = Struct({
    "name": c_char(10*8),
    "age": c_unsigned_int(8),
    "weight": c_float(32),
    "dresses": clothes  # Nested structure
})

# Set values
person.set_data(name="Luca", age=29, weight=76.9)
person["dresses"].set_data(tshirt="foo", shorts="boo")
person["dresses"]["shoes"].set_data(number=42, brand="bar")

# Serialize
binary_data = person.pack()
```

This Python structure is binary-compatible with the following C structure:

```c
typedef struct __attribute__((packed)) {
    uint8_t number;
    char brand[10];
} shoes_t;

typedef struct __attribute__((packed)) {
    char tshirt[10];
    char shorts[10];
    shoes_t shoes;
} clothes_t;

typedef struct __attribute__((packed)) {
    char name[10];
    uint8_t age;
    float weight;
    clothes_t clothes;
} person_t;
```

### Array Example

```python
from packed_struct import Struct, c_array, c_unsigned_int

# Array of integers
data = Struct({
    "header": c_unsigned_int(16),
    "values": c_array(c_unsigned_int, 8, 10)  # 10 bytes
})

data.set_data(header=0xFFFF)
data["values"].set_value([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Iterate over array elements
for i, element in enumerate(data["values"]):
    print(f"values[{i}] = {element.value}")
```

## Use Cases

- **Embedded Systems**: Communicate with hardware devices using binary protocols
- **Network Protocols**: Implement custom network packet formats
- **File Formats**: Read/write binary file formats
- **IoT Applications**: Exchange data between Python and C/C++ applications
- **Data Serialization**: Efficient binary serialization for size-constrained environments

## Supported Features

| Feature | Status |
|---------|--------|
| C-like structures | ✅ Supported |
| Bit-fields | ✅ Supported |
| Nested structures | ✅ Supported |
| Arrays | ✅ Supported |
| Byte endianness | ✅ Supported (big, little, native) |
| Bit endianness | 🚧 Planned |
| Dynamic arrays | 🚧 Planned |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/lu-maca/py-packed-struct.git
cd py-packed-struct

# Install in development mode
pip install -e .

# Run tests
python tests/tests.py
```

### Running Tests

The project includes comprehensive unit tests covering all data types and functionality:

```bash
python tests/tests.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **PyPI**: https://pypi.org/project/py-packed-struct/
- **GitHub**: https://github.com/lu-maca/py-packed-struct
- **Documentation**: https://github.com/lu-maca/py-packed-struct/tree/main/examples
- **Issue Tracker**: https://github.com/lu-maca/py-packed-struct/issues

## Acknowledgments

Built on top of the excellent [`bitstruct`](https://bitstruct.readthedocs.io/en/latest/index.html) library by Erik Moqvist.

---

**Author**: Luca Macavero


