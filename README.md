# py-packed-struct
An implementation of C-like packed structures in Python based on the [`bitstruct`](https://bitstruct.readthedocs.io/en/latest/index.html) package

**py-packed-struct** allows to define C-like structures in an elegant way and to convert them into `bytes` objects without having to specify the format as required by `struct`:
```python
# with struct
>>> from struct import *
>>> one, two, three = 1, 2, 3
>>> pack(">bhl", one, two, three)
b'\x01\x00\x02\x00\x00\x00\x03'

# with py-packed-struct
>>> from packed_struct import *
>>> s = Struct({"one": c_signed_int(8), "two": c_signed_int(16), "three": c_signed_int(32) })
>>> s.set_data(one = 1, two = 2, three = 3)
>>> serialized = s.pack(byte_endianness="big")
>>> print(serialized)
b'\x01\x00\x02\x00\x00\x00\x03'
>>>
>>> s.unpack(serialized)
>>> {'one': 1, 'two': 2, 'three': 3}
```
Who needs to remember struct format strings? :)

In addition, **py-packed-struct** allows to work with bit-fields and nested structures (see [examples](https://github.com/lu-maca/py-packed-struct/tree/main/examples)).

Installation
----
```bash
pip install py-packed-struct
```

Supported features
----
- C-like struct
- bit-fields handling
- byte endianess
- (TODO) bit endianness


Example
----
This example can be found in [`example/mqtt`](https://github.com/lu-maca/py-packed-struct/tree/main/examples/mqtt). `publisher.py` publishes a message on a MQTT topic and `subscriber.c` is subscribed to that topic. The publisher publishes the following structure:
```python
person = Struct(
    {
        "name": c_char(10*8),
        "age": c_unsigned_int(8),
        "weight": c_float(32),
        "dresses": Struct(
            {
                "tshirt": c_char(10*8),
                "shorts": c_char(10*8),
                "shoes": Struct(
                    {
                        "number": c_unsigned_int(8),
                        "brand": c_char(10*8)
                    }
                )
            }
        )
    }
)
# set data values
person.set_data(name="Luca", age=29, weight=76.9)
person.dresses.set_data(tshirt="foo", shorts="boo")
person.dresses.shoes.set_data(number=42, brand="bar")
```
The subscriber copies the incoming buffer in the following `struct`:
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
} person;
```

The result is the following:

![example mqtt](https://github.com/lu-maca/py-packed-struct/assets/65252677/997cadce-d79d-4117-b693-dc025957ebf9)


