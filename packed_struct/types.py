"""This module wraps the `bitstruct` package to implement a C like packed struct (https://bitstruct.readthedocs.io/en/latest/index.html)"""

import copy
import bitstruct as bstruct
from typing import Union

BYTE_ENDIANNESS = {
    "=": "",
    "big": ">",
    "little": "<",
}


class Type:
    """Generic type

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        if bits <= 0 or type(bits) != int:
            raise Exception("Number of bits shall be a positive integer")
        self.fmt = None
        self.value = None
        self.size = bits

    def __repr__(self) -> str:
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, Type):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def set_value(self, value):
        self.value = value


class _NumericType(Type):
    """Intermediate base class for numeric types (integers and floats).

    Adds arithmetic and ordering operations on top of :class:`Type`. Non-numeric
    subclasses (booleans, chars, raw bytes, padding, arrays) intentionally do
    *not* inherit from this class so that meaningless operations like
    ``c_char(...) * 2`` or ``c_bool(...) - 1`` raise a ``TypeError`` instead of
    silently returning a value.
    """

    def __add__(self, other):
        if isinstance(other, Type):
            return self.value + other.value
        return self.value + other

    def __sub__(self, other):
        if isinstance(other, Type):
            return self.value - other.value
        return self.value - other

    def __mul__(self, other):
        if isinstance(other, Type):
            return self.value * other.value
        return self.value * other

    def __truediv__(self, other):
        if isinstance(other, Type):
            return self.value / other.value
        return self.value / other

    def __floordiv__(self, other):
        if isinstance(other, Type):
            return self.value // other.value
        return self.value // other

    def __mod__(self, other):
        if isinstance(other, Type):
            return self.value % other.value
        return self.value % other

    def __pow__(self, other):
        if isinstance(other, Type):
            return self.value ** other.value
        return self.value ** other

    def __radd__(self, other):
        return other + self.value

    def __rsub__(self, other):
        return other - self.value

    def __rmul__(self, other):
        return other * self.value

    def __rtruediv__(self, other):
        return other / self.value

    def __rfloordiv__(self, other):
        return other // self.value

    def __rmod__(self, other):
        return other % self.value

    def __rpow__(self, other):
        return other ** self.value

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value

    def __abs__(self):
        return abs(self.value)

    def __lt__(self, other):
        if isinstance(other, Type):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, Type):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, Type):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, Type):
            return self.value >= other.value
        return self.value >= other

    __hash__ = Type.__hash__


class c_unsigned_int(_NumericType):
    """`u` stands for unsigned integer, according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        self.fmt: str = f"u{bits}"


class c_signed_int(_NumericType):
    """`s` stands for signed integer, according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        self.fmt: str = f"s{bits}"


class c_float(_NumericType):
    """`f` stands for float (16, 32, 64 bits), according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        if bits not in (16, 32, 64):
            raise Exception(
                f"Float must be of 16, 32 or 64 bits (requested: {bits}). See https://bitstruct.readthedocs.io/en/latest/#performance."
            )

        self.fmt: str = f"f{bits}"


class c_bool(Type):
    """`b` stands for boolean, according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        self.fmt: str = f"b{bits}"


class c_char(Type):
    """`c` stands for char in C language, `t` according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)

    Nota bene: a char is always contained in at least 8 bits.
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        if bits % 8 != 0:
            raise UserWarning(
                "char must be contained in multiples of 8 bits (see https://bitstruct.readthedocs.io/en/latest/#performance)"
            )
        self.fmt: str = f"t{bits}"


class c_raw_bytes(Type):
    """`r` stands for raw, for raw bytes, according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        self.fmt: str = f"r{bits}"


class c_padding(Type):
    """`p` stands for padding, according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        self.fmt: str = f"u{bits}"
        self.value = 0


class c_array(Type):
    """Array of a primitive Type or of a Struct.

    Always pass a *template instance* as the first argument; it is deep-copied
    for each element.

    Examples::

        c_array(c_unsigned_int(8), 3)   # array of 3 uint8
        c_array(c_float(32), 4)         # array of 4 float32
        c_array(Struct({"x": c_unsigned_int(8), "y": c_unsigned_int(8)}), 2)
    """

    def __init__(self, template: Union["Type", "Struct"], array_size: int) -> None:
        if array_size < 0:
            raise UserWarning("array_size must be positive")
        if not isinstance(template, (Type, Struct)):
            raise TypeError(f"template must be a Type or Struct instance, got {type(template)}")

        super().__init__(template.size * array_size)
        self._array_size = array_size
        self.value = [copy.deepcopy(template) for _ in range(array_size)]

        self.fmt = ""
        for value in self.value:
            self.fmt += value.fmt

    def __iter__(self):
        yield from self.value

    def __getitem__(self, idx):
        return self.value[idx]

    def set_value(self, values: Union[list, str]):
        if isinstance(values, str) and len(values) < len(self.value):
            values += "\0" * (len(self.value) - len(values))
        if len(values) != len(self.value):
            raise UserWarning(
                f"Length of array ({self._array_size}) is different from the length of the provided list ({len(values)})"
            )
        for provided_value, value in zip(values, self.value):
            if isinstance(value, Struct):
                value.set_data(**provided_value)
            elif isinstance(value, c_array):
                value.set_value(provided_value)
            else:
                value.set_value(provided_value)


def _flatten_values(item) -> list:
    """Flatten an item (``Type``, ``Struct`` or ``c_array``, possibly nested)
    into a flat list of scalar values, in the order they should be packed.
    """
    if isinstance(item, Struct):
        return item.value
    if isinstance(item, c_array):
        out = []
        for element in item.value:
            out += _flatten_values(element)
        return out
    return [item.value]


def _set_from_unpacked(item, unpacked, idx: int) -> int:
    """Walk ``item`` (``Type``/``Struct``/``c_array``, possibly nested),
    consuming scalar values from ``unpacked`` starting at ``idx`` and writing
    them onto leaves. Return the next index to consume.
    """
    if isinstance(item, Struct):
        for _, child in item._data.items():
            idx = _set_from_unpacked(child, unpacked, idx)
        return idx
    if isinstance(item, c_array):
        for element in item.value:
            idx = _set_from_unpacked(element, unpacked, idx)
        return idx
    item.value = unpacked[idx]
    return idx + 1


class Struct:
    """Definition of a C-like packed struct

    Argument:
        `data_dict` dictionary of data to be included in the packed struct (key: name, item: data type)

    Nota bene:
        Data types can only be of type `Type` or of type `Struct`, for nested structures

    Example:
        1) simple struct
        ```python
        person = Struct({"name": c_char(10*8), "age": c_unsigned_int(8), "weight": c_float(32)})
        # person in C would be:
        # struct{
        #    char[10] name;
        #    uint8_t age;
        #    float weight;
        # } person;
        ```

        2) nested structs
        ```python
        person = Struct(
            {
                "name": c_char(10*8),
                "age": c_unsigned_int(8),
                "weight": c_float(32),
                "dresses": Struct(
                    {
                        "tshirt": c_char(10*8),
                        "shorts": c_char(10*8)
                    }
                )
            }
        )
        person["dresses"].set_data(tshirt="nike", shorts="adidas")
        person.set_data(name="Maria", age=26, weight=76.8)
        print(person.size)
        print(person.pack())
        ```
    """

    def __init__(self, data_dict: dict) -> None:
        if not data_dict:
            raise Exception("Empty structure cannot be created")

        # check on types of data
        for key, item in data_dict.items():
            if not (isinstance(item, Type) or isinstance(item, Struct)):
                raise Exception(f"Data {key} shall be of type Type or Struct. Current type: {type(item)}")

        # if all checks are passed, initialize attributes
        self._data = data_dict
        self._fmt = None

    def __getitem__(self, data):
        try:
            return self._data[data].value
        except KeyError:
            raise KeyError(f"Data {data} not found in struct")

    def __getattr__(self, data):
        # Guard against __getattr__ being called before _data is set (e.g. during
        # copy.deepcopy reconstruction), which would otherwise cause infinite recursion.
        if '_data' not in self.__dict__:
            raise AttributeError(data)
        try:
            return self._data[data].value
        except KeyError:
            raise AttributeError(f"Data {data} not found in struct")

    def __repr__(self) -> str:
        representation = {}
        for key, item in self._data.items():
            representation[key] = item
        return str(representation)

    """Properties"""

    @property
    def size(self) -> int:
        """Return the size of the struct"""
        bitsize = 0
        for _, item in self._data.items():
            bitsize += item.size
        return bitsize

    @property
    def fmt(self) -> str:
        """Return the composed format of a struct, i.e. data types packed together.
        If already computed, returns directly it (to save time), if not compute it.
        """
        if not self._fmt:
            self._fmt = "".join([item.fmt for _, item in self._data.items()])

        return self._fmt

    @property
    def value(self) -> list:
        """Return the flat list of values of all data (recursing into nested
        Structs and arbitrarily-nested c_arrays).
        """
        values = []
        for _, item in self._data.items():
            values += _flatten_values(item)
        return values

    """Public methods"""

    def get_data(self) -> dict:
        """Return a dict containing all data in the struct."""
        return self._data

    def pack(self, byte_endianness: str = "=") -> bytes:
        """Return a `bytes` object containing the packed string with the requested `byte_endianness`
        according to specified format

        Argument:
            `byte_endianness` shall be "big", "little" or "=" (default: "=", i.e. native)
        """

        check_array = [True if x is not None else False for x in self.value]
        if not byte_endianness in BYTE_ENDIANNESS.keys():
            raise Exception("Byte endianness shall be 'little', 'big' or '='")
        if not all(check_array):
            raise Exception("You have to initialize all data.")

        # set byte endianness
        B_endianness = BYTE_ENDIANNESS[byte_endianness]

        fmt = f"{self.fmt}{B_endianness}"
        args = self.value

        return bstruct.pack(fmt, *args)

    def set_data(self, **kwargs):
        """Set data in the struct.

        Examples of usage:
            ```python
            person = Struct({"name": c_char(10*8), "age": c_unsigned_int(8), "weight": c_float(32)})
            person.set_data(name="Mario", age=25, weight=75.8)
            ```
        """
        if not kwargs:
            raise Exception("Give me some data: see examples")

        for key, item in kwargs.items():
            if not key in self._data.keys():
                raise AttributeError(f"Data {key} not found! Current data are: {self._data.keys()}")
            # if the key exists, we can set the value
            self._data[key].set_value(item)

    def unpack(
        self,
        byte_string: bytes,
        byte_endianness: str = "=",
        text_encoding: str = "utf-8",
        text_errors: str = "strict",
    ) -> dict:
        """Unpack `byte_string: bytes` according to the format of the struct.
        Text fields are decoded with given encoding `text_encoding` and error
        handling as given by `text_errors` (both passed to `bytes.decode()`).
        Return a dict containing data.

        Arguments:
            `byte_string` the byte string you want to unpack
            `byte_endianness` shall be "big", "little" or "=" (default: "=", i.e. native)
            `text_encoding` passed to `bytes.decode()`
            `text_errors` passed to `bytes.decode()`
        """
        if not byte_endianness in BYTE_ENDIANNESS.keys():
            raise Exception("Byte endianness shall be 'little', 'big' or '='")

        # set byte endianness
        B_endianness = BYTE_ENDIANNESS[byte_endianness]
        # set unpack format
        fmt = f"{self.fmt}{B_endianness}"

        unpacked = bstruct.unpack(fmt, byte_string, text_encoding=text_encoding, text_errors=text_errors)
        i = 0

        def recursive_set(dict_item, idx: int):
            for _, item in dict_item.items():
                idx = _set_from_unpacked(item, unpacked, idx)
            return idx

        recursive_set(self._data, i)
        return self._data
