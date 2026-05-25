import math

def f(x):
    """Función a evaluar: e^x"""
    return math.exp(x)

def derivadas_diferencias_finitas_detallado():
    # Parámetros iniciales
    x_val = 2
    h_values = [0.5, 0.1, 0.05, 0.01, 0.005, 0.001]
    
    # El valor analítico real de e^x en x=2
    valor_real = math.exp(x_val)
    
    print(f"Valor analítico real f'(2) = f''(2) = {valor_real:.10f}\n")
    
    # =========================================================================
    # PRIMERA DERIVADA
    # =========================================================================
    print("=========================================================================================")
    print("                      ANÁLISIS DETALLADO: PRIMERA DERIVADA (Central)")
    print("=========================================================================================")
    print(f"{'h':<6} | {'Aprox (6 dig)':<14} | {'Error (6 dig)':<14} | {'Aprox (8 dig)':<16} | {'Error (8 dig)':<16}")
    print("-" * 89)
    
    for h in h_values:
        # Fórmula de diferencia central
        aprox_1ra = (f(x_val + h) - f(x_val - h)) / (2 * h)
        error_1ra = abs(valor_real - aprox_1ra)
        
        print(f"{h:<6} | {aprox_1ra:<14.6f} | {error_1ra:<14.6f} | {aprox_1ra:<16.8f} | {error_1ra:<16.8f}")
        
    print("\n")
    
    # =========================================================================
    # SEGUNDA DERIVADA
    # =========================================================================
    print("=========================================================================================")
    print("                      ANÁLISIS DETALLADO: SEGUNDA DERIVADA (Central)")
    print("=========================================================================================")
    print(f"{'h':<6} | {'Aprox (6 dig)':<14} | {'Error (6 dig)':<14} | {'Aprox (8 dig)':<16} | {'Error (8 dig)':<16}")
    print("-" * 89)
    
    for h in h_values:
        # Fórmula de diferencia central para la 2da derivada
        aprox_2da = (f(x_val + h) - 2 * f(x_val) + f(x_val - h)) / (h**2)
        error_2da = abs(valor_real - aprox_2da)
        
        print(f"{h:<6} | {aprox_2da:<14.6f} | {error_2da:<14.6f} | {aprox_2da:<16.8f} | {error_2da:<16.8f}")

if __name__ == "__main__":
    derivadas_diferencias_finitas_detallado()