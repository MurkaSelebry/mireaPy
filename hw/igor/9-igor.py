def main(table):
    # Удаление дубликатов столбцов
    transposed_table = [[] for _ in range(len(table[0]))]
    for row in table:
        for i, cell in enumerate(row):
            transposed_table[i].append(cell)

    transposed_table = [list(
        t) for t in set(tuple(row) for row in transposed_table)]
    table = [[] for _ in range(len(transposed_table[0]))]
    for row in transposed_table:
        for i, cell in enumerate(row):
            table[i].append(cell)

    # Удаление дубликатов строк
    table = [list(t) for t in set(tuple(row) for row in table)]

    # Удаление пустых строк
    table = [row for row in table if any(cell is not None for cell in row)]

    # Преобразование содержимого ячеек
    table = [[cell.replace('.', '-').replace(
        '+7', '').replace(
        ' ', '') if cell is not None else '' for cell in row] for row in table]

    # Перестановка столбцов
    temp = table[0]
    table[0] = table[1]
    table[1] = temp

    temp = table[2]
    table[2] = table[0]
    table[0] = temp

    return table

table = [
    ['+78173041526', '00.08.03', '00.08.03', 'Т.А. Чоцский'],
    ['+78173041526', '00.08.03', '00.08.03', 'Т.А. Чоцский'],
    ['+79563624943', '99.07.21', '99.07.21', 'З.Р. Ширитянц'],
    [None, None, None, None],
    ['+78173041526', '00.08.03', '00.08.03', 'Т.А. Чоцский'],
    ['+73970375306', '04.08.26', '04.08.26', 'А.З. Нитук'],
    ['+75650096525', '01.05.22', '01.05.22', 'С.С. Нибов']
]

transformed_table = main(table)

print(transformed_table)
