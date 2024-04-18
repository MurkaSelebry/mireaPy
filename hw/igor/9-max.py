from collections import OrderedDict

def transform_data(data_list):
    # Удаление дубликатов столбцов
    unique_columns = list(OrderedDict.fromkeys(data_list[0]))
    transformed_data = [unique_columns]

    # Удаление пустых столбцов
    non_empty_columns = [column for column in unique_columns if any(row[idx] for row in data_list)]
    transformed_data.append(non_empty_columns)

    # Удаление пустых строк и преобразование содержимого ячеек
    for row in data_list:
        if any(row):
            transformed_row = []
            for item in row:
                if item is not None:
                    if '.' in item:
                        # Преобразование имени
                        name_parts = item.split()
                        transformed_name = f"{name_parts[1][0]}.{name_parts[0][0]}. {name_parts[2]}"
                        transformed_row.append(transformed_name)
                    elif '/' in item:
                        # Преобразование даты
                        date_parts = item.split('.')
                        transformed_date = f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}"
                        transformed_row.append(transformed_date)
                    elif item.lower() in ['да', 'нет']:
                        # Преобразование булевого значения
                        transformed_boolean = "true" if item.lower() == 'да' else "false"
                        transformed_row.append(transformed_boolean)
                    elif '-' in item:
                        # Преобразование номера телефона
                        phone_parts = item.split()
                        transformed_phone = f"{phone_parts[1][:3]}-{phone_parts[1][4:6]}-{phone_parts[1][7:]}"
                        transformed_row.append(transformed_phone)
                    else:
                        transformed_row.append(item)
            transformed_data.append(transformed_row)

    # Сортировка строк по столбцу №1
    sorted_data = sorted(transformed_data[1:], key=lambda x: x[0])

    # Транспонирование таблицы
    transposed_data = [list(column) for column in zip(*sorted_data)]

    return transposed_data

data_list = [['Давид Ц. Бицак', '01.10.07', 'да', None, '01.10.07', '125 853-8752'], ['Борис В. Вуримев', '00.02.02', 'да', None, '00.02.02', '374 517-7925'], [None, None, None, None, None, None], ['Павел С. Шутусиди', '99.07.07', 'да', None, '99.07.07', '674 743-1072']]

transformed_data = transform_data(data_list)
print(transformed_data)
