#variant 25
import itertools


functions = {
    'f1': [0, 84, 49, 66, 76, 47],
    'f2': [0, 44, 24, 62, 81, 81],
    'f3': [0, 34, 60, 37, 87, 89]
}

def calculate_profit(x, function_values):
    return function_values[x // 50]

X0 = 250
investments = [0, 50, 100, 150, 200, 250]

combinations = itertools.product(investments, repeat=3)

max_profit, best_distribution = max(
    (calculate_profit(x1, functions['f1']) + calculate_profit(x2, functions['f2']) + calculate_profit(x3, functions['f3']), (x1, x2, x3))
    for x1, x2, x3 in combinations if x1 + x2 + x3 <= X0)

print(f"Общая прибыль: {max_profit}")
print(f"Распределение вкладов: {best_distribution}")