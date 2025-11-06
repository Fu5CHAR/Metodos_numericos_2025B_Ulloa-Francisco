def suma_simplificada(a, b):
    """
    Calcula S = sum_{i=1}^{n} a_i * (sum_{j=1}^{i} b_j)
    usando sumas prefijo para optimizar los cálculos.
    """
    n = len(a)
    B = [0] * n  # Sumas prefijo de b
    B[0] = b[0]
    
    for i in range(1, n):
        B[i] = B[i-1] + b[i]
    
    S = 0
    for i in range(n):
        S += a[i] * B[i]
    
    return S

# Ejemplo de uso:
a = [2, 3, 4, 5]
b = [1, 2, 3, 4]

resultado = suma_simplificada(a, b)
print("Resultado:", resultado)
