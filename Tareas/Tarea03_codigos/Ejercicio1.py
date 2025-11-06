from decimal import Decimal, getcontext
import math

getcontext().prec = 60  # suficiente precisión interna

def chop_decimal(x: Decimal, sig=3):
    if x == 0:
        return Decimal(0)
    sign = 1 if x >= 0 else -1
    x_abs = abs(x)
    exponent = int(math.floor(math.log10(float(x_abs))))
    factor = Decimal(10) ** (sig - 1 - exponent)
    truncated = ( (x_abs * factor).to_integral_value(rounding="ROUND_DOWN") ) / factor
    return Decimal(sign) * truncated

def sum_chopped(n=10, power=2, order='forward', sig=3):
    terms = [Decimal(1) / (Decimal(i) ** Decimal(power)) for i in range(1, n+1)]
    if order == 'reverse':
        terms = list(reversed(terms))
    S = Decimal(0)
    partials = []
    for t in terms:
        S = S + t
        S = chop_decimal(S, sig)
        partials.append((t, S))
    return partials, S

# Ejemplo de uso:
# a) power=2
a_f_partials, a_f_sum = sum_chopped(10, 2, 'forward', 3)
a_r_partials, a_r_sum = sum_chopped(10, 2, 'reverse', 3)

# b) power=3
b_f_partials, b_f_sum = sum_chopped(10, 3, 'forward', 3)
b_r_partials, b_r_sum = sum_chopped(10, 3, 'reverse', 3)

# Para ver los resultados:
print("a  suma desde los más grandes:", a_f_sum)   # 1.53
print("a  suma desde los más pequeños:", a_r_sum)   # 1.54
print("b  suma desde los más grandes:", b_f_sum)   # 1.16
print("b  suma desde los más pequeños:", b_r_sum)   # 1.19
