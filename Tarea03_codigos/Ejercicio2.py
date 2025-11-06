
import math
from decimal import Decimal, getcontext

def n_min_by_tolerance(tol):
    """
    Calcula el menor entero n tal que 4/(2n+1) < tol.
    Devuelve n (entero).
    """
    if tol <= 0:
        raise ValueError("tol debe ser positivo")
    N_real = (4.0 / tol - 1.0) / 2.0
    n_min = math.ceil(N_real)
    return n_min

def compute_Pn_arctan_1(n):
    """
    Calcula P_n(1) = sum_{i=1..n} (-1)^{i+1} / (2i - 1)
    usando Decimal para mayor precisión.
    """
    getcontext().prec = 50  # precisión de 50 dígitos
    Pn = Decimal(0)
    for i in range(1, n + 1):
        term = Decimal((-1)**(i + 1)) / Decimal(2 * i - 1)
        Pn += term
    return Pn

if __name__ == "__main__":
    # Parte (a): tolerancia 1e-3
    tol_a = 1e-3
    n_a = n_min_by_tolerance(tol_a)
    print("Parte (a): tolerancia =", tol_a)
    print("n mínimo =", n_a)

    # Calcular P_n y comparar con pi
    Pn_a = compute_Pn_arctan_1(n_a)
    pi_approx_a = Decimal(4) * Pn_a
    pi_true = Decimal(str(math.pi))
    error_abs_a = abs(pi_true - pi_approx_a)
    print("Aproximación π ≈", pi_approx_a)
    print("Error absoluto =", error_abs_a)

    # Parte (b): tolerancia 1e-10
    tol_b = 1e-10
    n_b = n_min_by_tolerance(tol_b)
    print("\nParte (b): tolerancia =", tol_b)
    print("n mínimo =", n_b)
  