from packed_struct import *
import paho.mqtt.publish as publish

if __name__ == "__main__":
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
    person.set_data(name="Luca", age=29, weight=76.9)
    person.dresses.set_data(tshirt="foo", shorts="boo")
    person.dresses.shoes.set_data(number=42, brand="bar")
    print(person)

    payload = person.pack("small")

    topic = u"example/mqtt"
    publish.single(topic, payload, hostname="localhost") 
