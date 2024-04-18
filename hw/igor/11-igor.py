from struct import unpack_from, calcsize, unpack


class Types:
    char = 'c'
    int8 = 'b'
    uint8 = 'B'
    int16 = 'h'
    uint16 = 'H'
    int32 = 'i'
    uint32 = 'I'
    int64 = 'q'
    uint64 = 'Q'
    float = 'f'
    double = 'd'


class BinaryReader:
    def __init__(self, stream, offset, order="<"):
        self.stream = stream
        self.offset = offset
        self.order = order

    def jump(self, offset):
        reader = BinaryReader(self.stream, offset, self.order)
        return reader

    def read(self, pattern):
        size = calcsize(pattern)
        unpack_data = unpack_from(self.order + pattern,
                                  self.stream, self.offset)
        self.offset += size
        return unpack_data[0]


def read_c(reader):
    c1 = reader.read(Types.int64)
    c2 = reader.read(Types.uint8)
    c3 = [reader.read(Types.uint8) for _ in range(8)]
    return dict(C1=c1, C2=c2, C3=c3)


def read_d(reader):
    d1_size = reader.read(Types.uint16)
    d1_offset = reader.read(Types.uint32)
    d1_reader = reader.jump(d1_offset)
    d1 = [d1_reader.read(Types.uint16) for _ in range(d1_size)]
    d2 = reader.read(Types.uint32)
    d3 = reader.read(Types.int8)
    return dict(D1=d1, D2=d2, D3=d3)


def read_b(reader):
    b1_size = reader.read(Types.uint16)
    b1_offset = reader.read(Types.uint32)
    b1_reader = reader.jump(b1_offset)
    b1 = [b1_reader.read(Types.uint64) for _ in range(b1_size)]
    b2 = read_c(reader)
    return dict(B1=b1, B2=b2)


def read_a(reader):
    struct_a = {}

    # Field 1: Size and address of array of B addresses
    a1_offset = reader.read(Types.uint16)
    b_addresses_reader = reader.jump(a1_offset)
    a1_size = b_addresses_reader.read(Types.uint16)

    # Increase the buffer size to accommodate the uint32 values
    buffer_size = a1_size * 4
    b_addresses_buffer = b_addresses_reader.read_buffer(buffer_size)

    # Read the uint32 values from the buffer
    b_addresses = [b_addresses_buffer[i:i + 4].unpack(Types.uint32)[0] for i in range(0, buffer_size, 4)]
    struct_a['A1'] = [read_b(reader.jump(addr)) for addr in b_addresses]
    # Field 2: Address of structure D
    a2_offset = reader.read(Types.uint16)
    d_reader = reader.jump(a2_offset)
    a2 = read_d(d_reader)
    struct_a['A2'] = a2

    # Field 3: int8
    a3 = reader.read(Types.int8)
    struct_a['A3'] = a3

    # Field 4: uint64
    a4 = reader.read(Types.uint64)
    struct_a['A4'] = a4

    # Field 5: uint16
    a5 = reader.read(Types.uint16)
    struct_a['A5'] = a5

    return struct_a


def main(stream):
    return read_a(BinaryReader(stream, 5))

data = (b'YQUV\x18\x02\x00\x80\x00\x90\x004_\xd8\xcc\x85*\xc6\xf2\xe5\x8fQP\xae'
 b'\xe9\n\xaa\xea\x83\xdez\x9b\xf37\xb8/\x8a\x85\x98\xa2\xb2\xf8\xdf\xa4'
 b'\x1d;T\xcaZ&;\xafV\x7f\x04\x00\x00\x00\x16\x00\x00\x00\xb52x\\\xa47'
 b"\x1bX\x18h\xc0\xec2\x15q'\x84\x05\xf5W\xd4M\x04\xaew\x0b\x0c\x9fI\xe2"
 b'8\xf2\xb4E?L\x0e\xe5z\xb9\x00\x03\x00\x00\x00O\x00\x00\x00\x97'
 b'\x0b\x8a\x08\x8e\x99\xcb\xaf\xfe4\xfd\xee\rF\xb9d\xdd6\x00\x00\x00'
 b'g\x00\x00\x00\x81P\xcd\x0c\xb8\xa7J\x99\x04\x00\x88\x00\x00\x00\xd1\xa1'
 b'\xf1\x85\xb8')
print(main(data))