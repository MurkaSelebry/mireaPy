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


def read_f(reader):
    f1 = reader.read(Types.int8)
    f2 = reader.read(Types.int16)
    f3 = reader.read(Types.double)
    f4 = reader.read(Types.uint8)
    f5 = reader.read(Types.int64)
    return dict(F1=f1, F2=f2, F3=f3, F4=f4, F5=f5)


def read_e(reader):
    e1 = reader.read(Types.int32)
    e2_size = reader.read(Types.uint16)
    e2_offset = reader.read(Types.uint32)
    e2_reader = reader.jump(e2_offset)
    e2 = [e2_reader.read(Types.float) for _ in range(e2_size)]
    e3 = reader.read(Types.uint16)
    e4 = reader.read(Types.uint32)
    return dict(E1=e1, E2=e2, E3=e3, E4=e4)


def read_d(reader):
    e_offset = reader.read(Types.uint32)
    e_reader = reader.jump(e_offset)
    d1 = read_e(e_reader)
    d2 = reader.read(Types.int64)
    d3 = reader.read(Types.int8)
    return dict(D1=d1, D2=d2, D3=d3)


def read_c(reader):
    c1 = reader.read(Types.int8)
    c2 = b''.join([reader.read(Types.char) for _ in range(2)]).decode('utf-8')
    c3 = reader.read(Types.int8)
    return dict(C1=c1, C2=c2, C3=c3)


def read_b(reader):
    b1 = reader.read(Types.uint8)
    b2 = reader.read(Types.uint16)
    c_offset = reader.read(Types.uint16)
    c_reader = reader.jump(c_offset)
    b3 = read_c(c_reader)
    b4 = reader.read(Types.uint8)
    b5 = read_d(reader)
    b6 = reader.read(Types.uint8)

    return dict(B1=b1, B2=b2, B3=b3, B4=b4, B5=b5, B6=b6)


def read_a(reader):
    a1 = reader.read(Types.int16)
    a2 = reader.read(Types.uint32)
    b_offset = reader.read(Types.uint32)
    b_reader = reader.jump(b_offset)
    a3 = read_b(b_reader)
    a4 = [read_f(reader.jump(reader.read(Types.uint32))) for _ in range(2)]
    a5 = [reader.read(Types.uint16) for _ in range(2)]
    a6 = reader.read(Types.float)
    return dict(A1=a1, A2=a2, A3=a3, A4=a4, A5=a5, A6=a6)


def main(stream):
    return read_a(BinaryReader(stream, 5))


data = (b'\xe7XYBQ\x9b\x928\xc0g|O\x00\x00\x00c\x00\x00\x00w\x00\x00\x00\x88'
 b'\xa9f\xcb\x82NL?>yn\x95K&_?8P\x94=\xf6\x99I\xbfb\xd8\x8f\xbe\x19\xb5z?B'
 b'#\xb0\xbe\r\\%\xbf\\5-=\x07\x00#\x00\x00\x00M\x02.CJ\xe3\xb6\r;\x1f\x00'
 b'^?\x00\x00\x00[\xed\xe6q\xcc9"\xb1\x06\xda\xcb{\x87\xc8.\xa1\x93\xa5\x1b'
 b'\xc7?\xfe\x98\x8d\x92\xac\x9e\x06\xa2\xc2\xb8\x9e\xcfd\xcd\x04\xdf\x8f#'
 b'\xd9?\xa8\xf3\x8d\xd4\x9f\x16\xfc:Q')
#main(data)

# Данные для разбора
data = (b'\xe7XYBQ\x9b\x928\xc0g|O\x00\x00\x00c\x00\x00\x00w\x00\x00\x00\x88'
        b'\xa9f\xcb\x82NL?>yn\x95K&_?8P\x94=\xf6\x99I\xbfb\xd8\x8f\xbe\x19\xb5z?B'
        b'#\xb0\xbe\r\\%\xbf\\5-=\x07\x00#\x00\x00\x00M\x02.CJ\xe3\xb6\r;\x1f\x00'
        b'^?\x00\x00\x00[\xed\xe6q\xcc9"\xb1\x06\xda\xcb{\x87\xc8.\xa1\x93\xa5\x1b'
        b'\xc7?\xfe\x98\x8d\x92\xac\x9e\x06\xa2\xc2\xb8\x9e\xcfd\xcd\x04\xdf\x8f#'
        b'\xd9?\xa8\xf3\x8d\xd4\x9f\x16\xfc:Q')

print(main(data))