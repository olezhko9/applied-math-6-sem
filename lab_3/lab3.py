import numpy as np

# вариант 4
# p = {
#     'lambda': 7.92,     # Интенсивность входящего потока заявок
#     'nu': 3.6,          # Интенсивность обслуживания заявки
#     'r': 3,             # Количество каналов
#     'm': 1              # Возможная длина очереди
# }

# пример
p = {
    'lambda': 6.07,     # Интенсивность входящего потока заявок
    'nu': 3.1,          # Интенсивность обслуживания заявки
    'r': 2,             # Количество каналов
    'm': 2              # Возможная длина очереди
}

print(p)


# transition_matrix = np.array([
#     np.array([-p['lambda'], p['nu'], 0, 0, 0]),
#     np.array([p['lambda'], -(p['nu']+p['lambda']), 2*p['nu'], 0, 0]),
#     np.array([0, p['lambda'], -(2*p['nu']+p['lambda']), 3*p['nu'], 0]),
#     np.array([0, 0, p['lambda'], -(3*p['nu']+p['lambda']), 3*p['nu']]),
#     np.array([0, 0, 0, p['lambda'], -3*p['nu']])
# ])

transition_matrix = np.array([
    np.array([-p['lambda'], p['nu'], 0, 0, 0]),
    np.array([p['lambda'], -(p['nu']+p['lambda']), 2*p['nu'], 0, 0]),
    np.array([0, p['lambda'], -(2*p['nu']+p['lambda']), 2*p['nu'], 0]),
    np.array([0, 0, p['lambda'], -(2*p['nu']+p['lambda']), 2*p['nu']]),
    np.array([0, 0, 0, p['lambda'], -2*p['nu']])
])


def solve_stationary_probability(transition_matrix):
    """Аналитическое нахождение стационарного состояния"""
    n = len(transition_matrix)
    A = transition_matrix
    probability_dist = np.ones((1, n))

    A = np.vstack((A, probability_dist))
    B = np.zeros(n + 1)
    B[-1] = 1

    p = np.linalg.lstsq(A, B, rcond=1)[0]
    return p


stationary = solve_stationary_probability(transition_matrix)
print(stationary)
# print(list(map(lambda x: np.around(x, 6), stationary)))


def average_machines(arr):
    parts = []
    for i in range(p['r']):
        parts.append([arr[i]])
    parts.append(arr[-(len(arr) - p['r']):])

    working_mean = sum([sum(a) * idx for idx, a in enumerate(parts)])

    parts = parts[::-1]
    not_working_mean = sum([sum(a) * idx for idx, a in enumerate(parts)])

    return working_mean, not_working_mean


working, not_working = average_machines(stationary)
print(working, not_working)


work_coef = working / p['r']
idle_coef = not_working / p['r']
print("Коэффициент загрузки: %.2f" % (work_coef * 100))
print("Коэффициент простаивания: %.2f" % (idle_coef * 100))