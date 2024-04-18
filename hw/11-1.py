import struct


def parse_structure_E(data, offset):
    # Распаковка полей структуры E
    int32_value = struct.unpack('<i', data[offset:offset + 4])[0]
    offset += 4

    size, address_float_array = struct.unpack('<HI', data[offset:offset + 6])
    offset += 6

    uint16_value = struct.unpack('<H', data[offset:offset + 2])[0]
    offset += 2

    uint32_value = struct.unpack('<I', data[offset:offset + 4])[0]
    offset += 4

    return offset, int32_value, size, address_float_array, uint16_value, uint32_value


def parse_structure_F(data, offset):
    # Распаковка полей структуры F
    int8_value = struct.unpack('b', data[offset:offset + 1])[0]
    offset += 1

    int16_value = struct.unpack('<h', data[offset:offset + 2])[0]
    offset += 2

    double_value = struct.unpack('<d', data[offset:offset + 8])[0]
    offset += 8

    uint8_value = struct.unpack('B', data[offset:offset + 1])[0]
    offset += 1

    int64_value = struct.unpack('<q', data[offset:offset + 8])[0]
    offset += 8

    return offset, int8_value, int16_value, double_value, uint8_value, int64_value


def main():
    # Данные для разбора
    data = (b'\xe7XYBQ\x9b\x928\xc0g|O\x00\x00\x00c\x00\x00\x00w\x00\x00\x00\x88'
            b'\xa9f\xcb\x82NL?>yn\x95K&_?8P\x94=\xf6\x99I\xbfb\xd8\x8f\xbe\x19\xb5z?B'
            b'#\xb0\xbe\r\\%\xbf\\5-=\x07\x00#\x00\x00\x00M\x02.CJ\xe3\xb6\r;\x1f\x00'
            b'^?\x00\x00\x00[\xed\xe6q\xcc9"\xb1\x06\xda\xcb{\x87\xc8.\xa1\x93\xa5\x1b'
            b'\xc7?\xfe\x98\x8d\x92\xac\x9e\x06\xa2\xc2\xb8\x9e\xcfd\xcd\x04\xdf\x8f#'
            b'\xd9?\xa8\xf3\x8d\xd4\x9f\x16\xfc:Q')

    # Функция для разбора данных
    def unpack_data(data):
        # Сигнатура
        signature = struct.unpack('<5B', data[:5])
        print('Signature:', ' '.join([hex(byte) for byte in signature]))

        # Разбор структуры A
        offset = 5  # Начальное смещение после сигнатуры

        # Распаковка полей структуры A
        int16_value = struct.unpack('<h', data[offset:offset + 2])[0]
        offset += 2

        uint32_value = struct.unpack('<I', data[offset:offset + 4])[0]
        offset += 4

        address_b = struct.unpack('<I', data[offset:offset + 4])[0]
        offset += 4

        addresses_f = struct.unpack('<2I', data[offset:offset + 8])
        offset += 8

        uint16_values = struct.unpack('<2H', data[offset:offset + 4])
        offset += 4

        float_value = struct.unpack('<f', data[offset:offset + 4])[0]
        offset += 4

        print('\nStructure A:')
        print('int16:', int16_value)
        print('uint32:', uint32_value)
        print('address B:', address_b)
        print('addresses F:', addresses_f)
        print('uint16 values:', uint16_values)
        print('float:', float_value)

        # Разбор структуры B
        offset, uint8_value, uint16_value, address_c, uint8_value_2 = parse_structure_B(data, offset)

        # Разбор структуры C
        offset, int8_value_2, char_values, int8_value_3 = parse_structure_C(data, address_c)

        # Разбор структуры D
        offset, address_e, int64_value_2, int8_value_4 = parse_structure_D(data, offset)

        # Разбор структуры E
        offset, int32_value, size, address_float_array, uint16_value_2, uint32_value_2 = parse_structure_E(data, address_e)

        # Разбор структур полей F
        offsets_f = addresses_f

        structures_f = []
        for offset_f in offsets_f:
            offset_f, int8_value_f, int16_value_f, double_value_f, uint8_value_f, int64_value_f = parse_structure_F(data, offset_f)

            # Сохранение распакованной структуры F
            structure_f = {
                'int8': int8_value_f,
                'int16': int16_value_f,
                'double': double_value_f,
                'uint8': uint8_value_f,
                'int64': int64_value_f
            }
            structures_f.append(structure_f)

        # Вывод результатов
        print('\nStructures F:')
        for i, structure_f in enumerate(structures_f):
            print(f'Structure F {i+1}:')
            print('int8:', structure_f['int8'])
            print('int16:', structure_f['int16'])
            print('double:', structure_f['double'])
            print('uint8:', structure_f['uint8'])
            print('int64:', structure_f['int64'])

    # Запуск разбора данных
    unpack_data(data)

if __name__ == '__main__':
    main()
