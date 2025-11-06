x = 0.25
diferencia = 1e-6

# Cálculo del lado derecho
right_side = (1 + 2 * x) / (1 + x + x**2)

# Inicialización
sum_left = 0
n = 0

while True:
    numerator = (2**n) * (x**(2**n - 1)) - (2**(n + 1)) * (x**(2**(n + 1) - 1))
    denominator = 1 - x**(2**n) + x**(2**(n + 1))
    term = numerator / denominator
    sum_left += term

    if abs(sum_left - right_side) < diferencia:
        break

    n += 1

print(f"Se necesitan {n + 1} términos para que la suma difiera del lado derecho en menos de 1e-6.")
