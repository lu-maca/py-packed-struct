# py-packed-struct
An implementation of C-like packed structures in Python based on the [`bitstruct`](https://bitstruct.readthedocs.io/en/latest/index.html) package 


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


