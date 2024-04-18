first_letters = ['М', 'Ц', 'Н', 'И']
second_letters = ['С', 'Ь', 'Т', 'О']
third_letters = ['З', 'Т', 'И', 'Д']
fourth_letters = ['Ф', 'Я', 'Х', 'С']
fifth_letters = ['Е', 'Р', 'Ж', 'В']

all_words = []

for first in first_letters:
    for second in second_letters:
        for third in third_letters:
            for fourth in fourth_letters:
                for fifth in fifth_letters:
                    word = first + second + third + fourth + fifth
                    all_words.append(word)

# Выводим первые 10 слов для проверки
for el in all_words:
    print(el)
