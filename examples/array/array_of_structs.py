"""Example: array of structs

Shows how to use c_array with a Struct template to represent a fixed-size
array of composite records — equivalent to the following C struct:

    typedef struct {
        int16_t x;
        int16_t y;
    } Point;

    struct {
        uint8_t count;
        Point   waypoints[3];
    }
"""

from packed_struct import *

point = Struct({"x": c_signed_int(16), "y": c_signed_int(16)})

route = Struct(
    {
        "count": c_unsigned_int(8),
        "waypoints": c_array(point, 3),
    }
)

# Set each waypoint separately
route["waypoints"][0].set_data(x=0,    y=0)
route["waypoints"][1].set_data(x=100,  y=-50)
route["waypoints"][2].set_data(x=200,  y=75)
route.set_data(count=3)

# Or set all waypoints at once via set_data() with a list of dicts
route.set_data(waypoints=[
    {"x": 0,   "y": 0},
    {"x": 100, "y": -50},
    {"x": 200, "y": 75},
])

packed = route.pack()
print("packed :", packed.hex())
print("size   :", route.size, "bits /", len(packed), "bytes")

# Unpack back
point2 = Struct({"x": c_signed_int(16), "y": c_signed_int(16)})
route2 = Struct(
    {
        "count": c_unsigned_int(8),
        "waypoints": c_array(point2, 3),
    }
)
route2.unpack(packed)

print("count:", route2["count"])
for i in range(3):
    wp = route2["waypoints"][i]
    print(f"  waypoint[{i}]: x={wp['x']}, y={wp['y']}")
