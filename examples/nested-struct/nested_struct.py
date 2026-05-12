"""Example: pack / unpack round-trip with nested structs

Shows how to serialize a struct to bytes and deserialize it back —
equivalent to the following C structs:

    typedef struct {
        char     brand[10];
        uint8_t  size;
    } Shoe;

    typedef struct {
        char  tshirt[10];
        char  shorts[10];
        Shoe  shoes;
    } Dresses;

    typedef struct {
        char    name[10];
        uint8_t age;
        float   weight;
        Dresses dresses;
    } Person;
"""

from packed_struct import *


def make_person_struct():
    shoes   = Struct({"brand": c_char(10 * 8), "size": c_unsigned_int(8)})
    dresses = Struct({"tshirt": c_char(10 * 8), "shorts": c_char(10 * 8), "shoes": shoes})
    person  = Struct({"name": c_char(10 * 8), "age": c_unsigned_int(8), "weight": c_float(32), "dresses": dresses})
    return person, dresses, shoes


# --- Sender side ---
sender, sender_dresses, sender_shoes = make_person_struct()

sender.set_data(name="Alice", age=30, weight=58.5)
sender_dresses.set_data(tshirt="white", shorts="blue")
sender_shoes.set_data(brand="Nike", size=38)

payload = sender.pack(byte_endianness="big")
print("payload :", payload.hex())
print("size    :", sender.size, "bits /", len(payload), "bytes")

# --- Receiver side ---
receiver, receiver_dresses, receiver_shoes = make_person_struct()
receiver.unpack(payload, byte_endianness="big")

# get_data() returns the internal dict of Type/Struct objects
top    = receiver.get_data()
dr     = receiver_dresses.get_data()
sh     = receiver_shoes.get_data()

print("\nReceived:")
print("  name   :", top["name"].value)
print("  age    :", top["age"].value)
print("  weight :", top["weight"].value)
print("  tshirt :", dr["tshirt"].value)
print("  shorts :", dr["shorts"].value)
print("  brand  :", sh["brand"].value, "  size:", sh["size"].value)
