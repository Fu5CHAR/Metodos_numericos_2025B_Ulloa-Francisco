import cmath  # Maneja raíces complejas de forma automática

def raices_cuadraticas(a, b, c):
    """
    Calcula las raíces de un polinomio ax^2 + bx + c = 0.
    Maneja tanto raíces reales como complejas.
    """
    D = b**2 - 4*a*c  # Discriminante
    
    if D >= 0:
        if b >= 0:
            x1 = (2 * c) / (-b - D**0.5)   # fórmula (1.3)
            x2 = (-b - D**0.5) / (2 * a)   # fórmula (1.2)
        else:
            x1 = (-b + D**0.5) / (2 * a)   # fórmula (1.2)
            x2 = (2 * c) / (-b + D**0.5)   # fórmula (1.3)
    else:
        parte_real = -b / (2 * a)
        parte_imaginaria = (abs(D)**0.5) / (2 * a)
        x1 = complex(parte_real, parte_imaginaria)
        x2 = complex(parte_real, -parte_imaginaria)
    
    return x1, x2

# Ejemplo de uso
a, b, c = 1, -3, 2
x1, x2 = raices_cuadraticas(a, b, c)
print("x1 =", x1)
print("x2 =", x2)
