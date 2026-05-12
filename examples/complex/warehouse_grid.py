"""Example: complex composition.

Demonstrates the full expressive power of the library by combining:
    * nested ``Struct``s,
    * ``c_array`` *inside* a ``Struct``,
    * ``c_array`` of ``c_array`` (a 2D matrix),
    * the matrix elements themselves being ``Struct``s.

Equivalent C declarations::

    typedef struct {
        uint16_t lat;       // latitude  (encoded)
        uint16_t lon;       // longitude (encoded)
    } Location;

    typedef struct {
        uint8_t   id;
        Location  loc;          // <-- nested struct
        char      label[8];
        uint16_t  samples[4];   // <-- array inside struct
    } Bin;

    struct Warehouse {
        uint8_t version;
        Bin     grid[2][3];     // <-- array of array of struct
    };
"""

from packed_struct import (
    Struct,
    c_array,
    c_char,
    c_unsigned_int,
)

ROWS = 2
COLS = 3
SAMPLES_PER_BIN = 4
LABEL_BYTES = 8

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
location_tmpl = Struct({
    "lat": c_unsigned_int(16),
    "lon": c_unsigned_int(16),
})

bin_tmpl = Struct({
    "id":      c_unsigned_int(8),
    "loc":     location_tmpl,                                      # nested struct
    "label":   c_char(LABEL_BYTES * 8),
    "samples": c_array(c_unsigned_int(16), SAMPLES_PER_BIN),       # array inside struct
})


def make_warehouse() -> Struct:
    """Build a fresh Warehouse struct (templates are deep-copied internally)."""
    return Struct({
        "version": c_unsigned_int(8),
        # array of array of Bin
        "grid": c_array(c_array(bin_tmpl, COLS), ROWS),
    })


# ---------------------------------------------------------------------------
# Populate
# ---------------------------------------------------------------------------
warehouse = make_warehouse()
warehouse.set_data(version=1)

for r in range(ROWS):
    for c in range(COLS):
        bin_ = warehouse["grid"][r][c]              # the actual Bin Struct (deep-copied template)
        bin_data = bin_.get_data()                  # dict {field_name: Type/Struct/c_array}
        bin_data["loc"].set_data(lat=45000 + r, lon=9000 + c)   # nested struct
        bin_.set_data(
            id=r * COLS + c,
            label=f"B{r}-{c}",
            samples=[r * 100 + c * 10 + k for k in range(SAMPLES_PER_BIN)],
        )

# ---------------------------------------------------------------------------
# Pack
# ---------------------------------------------------------------------------
packed = warehouse.pack()
print("packed :", packed.hex())
print("size   :", warehouse.size, "bits /", len(packed), "bytes")

# ---------------------------------------------------------------------------
# Unpack into a fresh instance and verify
# ---------------------------------------------------------------------------
restored = make_warehouse()
restored.unpack(packed)

print("\nrestored.version =", restored["version"])
for r in range(ROWS):
    for c in range(COLS):
        b = restored["grid"][r][c]
        loc = b.get_data()["loc"]
        print(
            f"  grid[{r}][{c}]: id={b['id']:>2}  "
            f"loc=({loc['lat']}, {loc['lon']})  "
            f"label={b['label']!r:<10}  "
            f"samples={[b['samples'][k].value for k in range(SAMPLES_PER_BIN)]}"
        )

# Round-trip sanity check
assert restored.pack() == packed, "round-trip mismatch"
print("\nround-trip OK")
