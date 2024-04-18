def insert(source_str, insert_str, pos):
    return source_str[:pos] + insert_str + source_str[pos:]


'''
if temp_row:
    temp_row[0] = temp_row[0].split(';')
    temp_row[0][0] = temp_row[0][0][:2] + temp_row[0][0][4:]
    temp_row[0][1] = insert(insert(temp_row[0][1][3:], '-', 3), '-', 6)
    temp_row[0:1] = temp_row[0]
    temp_row[2] = str(round(float(temp_row[2]) * 100)) + '%'
    temp_row[3] = '/'.join(temp_row[3].split('-')[::-1])
    temp_row.insert(3, temp_row.pop(1))
    temp_row.insert(2, temp_row.pop(1))
'''


def main(table):
    new_table = list()
    for el in table:
        temp_row = list(filter(None, dict.fromkeys(el)))
        if temp_row:
            temp_row[0] = temp_row[0].split('[at]')[0]
            temp_row[1] = temp_row[1].split('.')[1][1::]
            temp_row[2] = temp_row[2] + '0'
            if temp_row[3] == 'Y':
                temp_row[3] = 'true'
            else:
                temp_row[3] = 'false'
        new_table.append(tuple(temp_row))
    new_table = list(filter(None, dict.fromkeys(new_table)))
    return [list(new_table[i]) for i in range(len(new_table))]


t = [['vonasberg81[at]mail.ru', 'Адель У. Вонасберг', '0.79', None, None, 'Y'], [None, None, None, None, None, None],
     ['tulin12[at]yahoo.com', 'Амир У. Тулин', '0.29', None, None, 'Y'],
     ['anatolij77[at]gmail.com', 'Анатолий Б. Барешев', '0.08', None, None, 'N']]
print(main(t))
