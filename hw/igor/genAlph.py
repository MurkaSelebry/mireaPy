

alphabet_map = {}

for i, letter in enumerate(' АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    binary = bin(i)[2:]
    alphabet_map[letter] = binary.zfill(5)
    if letter == 'Е':
        alphabet_map['Ё'] = alphabet_map[letter]
    elif letter == 'И':
        alphabet_map['Й'] = alphabet_map[letter]
print(alphabet_map)


def coder(path_to_text, path_to_gamma, path_to_out):


    # Открываем файл для чтения
    with open(path_to_text, 'r', encoding='utf8') as file:
        # Читаем содержимое файла
        text = file.read()
    text = text.upper()
    print(len(text))
    # Преобразуем текст в одну строку с помощью Alphabet Map
    converted_text = ''.join(alphabet_map[letter] for letter in text)
    print(len(converted_text))
    # Открываем файл для записи
    with open('texts/binOut.txt', 'w', encoding='utf8') as file:
        # Записываем преобразованный текст в файл
        file.write(converted_text)

    # Открываем файлы для чтения
    with open(path_to_gamma, 'r', encoding='utf8') as file1:
        # Читаем содержимое файлов
        text1 = file1.read()
    sum_text = ""
    for el1, el2 in zip(text1, converted_text):
        sum_text += str(int(el1 != el2))

    with open(path_to_out, 'w', encoding='utf8') as file:
        # Записываем преобразованный текст в файл
        file.write(sum_text)
    return 1

def decoder(gamma_path, coder_path):
    with open(coder_path, 'r', encoding='utf8') as file1, open(gamma_path, 'r', encoding='utf8') as file2:
        # Записываем преобразованный текст в файл
        text_coder = file1.read()
        text_gamma = file2.read()

    text_decode = ""

    for el_coder, el_gamma in zip(text_coder, text_gamma):
        if el_coder == '1':
            if el_gamma == '0':
                text_decode += '1'
            else:
                text_decode += '0'
        else:
            text_decode += el_gamma

    with open('texts/binOut2.txt', 'w', encoding='utf8') as file:
        # Записываем преобразованный текст в файл
        file.write(text_decode)

    # Создаем пустой список для хранения преобразованного текста
    converted_text = []

    # Разбиваем двоичный текст на группы по 5 символов
    for i in range(0, len(text_decode), 5):
        # Получаем группу символов
        group = text_decode[i:i + 5]
        # Используем alphabet_map для получения соответствующего символа
        letter = next((letter for letter, binary in alphabet_map.items() if binary == group), None)
        # Если символ найден, добавляем его в список
        if letter is not None:
            converted_text.append(letter)

    # Преобразуем список в строку и возвращаем ее
    converted_text = ''.join(converted_text)
    return converted_text

coder_path = 'texts/coderText.txt'
gamma_path = 'texts/binGamma.txt'

print(coder('texts/textInput.txt', gamma_path, coder_path))
print(decoder(gamma_path, coder_path))



