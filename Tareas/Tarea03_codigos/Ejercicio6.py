def suma_inversa(x):
    """
    Calcula la suma de una lista en orden inverso:
    S = sum_{i=n}^{1} x_i
    """
    suma = 0
    for i in range(len(x) - 1, -1, -1):
        suma += x[i]
    return suma

# Ejemplo de uso
x = [1, 2, 3, 4, 5]
resultado = suma_inversa(x)
print("Suma en orden inverso:", resultado)
