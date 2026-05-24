import math

def f(x):
    """Función a evaluar: e^x"""
    return math.exp(x)

def derivadas_diferencias_finitas():
    # Parámetros iniciales
    x_val = 2
    h_values = [0.5, 0.1, 0.05, 0.01, 0.005, 0.001]
    
    # El valor analítico real de e^x en x=2 para ambas derivadas
    valor_real = math.exp(x_val)
    
    print("======================================================")
    print("  ANÁLISIS DE ERROR: PRIMERA DERIVADA (Esquema Central)")
    print("======================================================")
    # Encabezados de la tabla
    print(f"{'Valor h':<10} | {'Error Abs (6 dig)':<20} | {'Error Abs (8 dig)':<20}")
    print("-" * 56)
    
    for h in h_values:
        # Fórmula de diferencia central para la 1ra derivada
        aprox_1ra = (f(x_val + h) - f(x_val - h)) / (2 * h)
        error_1ra = abs(valor_real - aprox_1ra)
        
        # Impresión con formato de precisión específica (.6f y .8f)
        print(f"{h:<10} | {error_1ra:<20.6f} | {error_1ra:<20.8f}")
        
    print("\n")
    print("======================================================")
    print("  ANÁLISIS DE ERROR: SEGUNDA DERIVADA (Esquema Central)")
    print("======================================================")
    print(f"{'Valor h':<10} | {'Error Abs (6 dig)':<20} | {'Error Abs (8 dig)':<20}")
    print("-" * 56)
    
    for h in h_values:
        # Fórmula de diferencia central para la 2da derivada
        aprox_2da = (f(x_val + h) - 2 * f(x_val) + f(x_val - h)) / (h**2)
        error_2da = abs(valor_real - aprox_2da)
        
        # Impresión con formato de precisión específica (.6f y .8f)
        print(f"{h:<10} | {error_2da:<20.6f} | {error_2da:<20.8f}")

# Ejecutar el análisis
if __name__ == "__main__":
    derivadas_diferencias_finitas()