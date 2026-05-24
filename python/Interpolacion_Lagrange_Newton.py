import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. Función para leer el archivo Excel
# ==========================================    
_BASE = os.path.dirname(os.path.abspath(__file__))

RUTA_EXCEL = os.path.abspath(os.path.join(_BASE, '..', 'data', 'raw', 'Prueba_semana2.xlsx'))
RUTA_GRAFICAS = os.path.abspath(os.path.join(_BASE, '..', 'data', 'processed'))

def leer_excel() -> tuple[np.ndarray, np.ndarray]:
    """Lee columnas A (x) y B (y) de la primera hoja del Excel."""
    try:
        df = pd.read_excel(RUTA_EXCEL, header=0, usecols=[0, 1])
        df.columns = ["x", "y"]
        df.dropna(inplace=True)
        x = df["x"].to_numpy(dtype=float)
        y = df["y"].to_numpy(dtype=float)
        if len(x) < 2:
            raise ValueError("Se necesitan al menos 2 puntos en el Excel.")
        return x, y
    except FileNotFoundError:
        print(f"\n  ✗ Archivo no encontrado.")
        print(f"     Ruta buscada: {RUTA_EXCEL}")
        print(f"     Verifica que el archivo exista en esa ubicación.")
        sys.exit(1)
    except Exception as e:
        print(f"\n  ✗ Error al leer el Excel: {e}")
        sys.exit(1)

# ==========================================
# 2. Método de Lagrange
# ==========================================
def interpolacion_lagrange(x_nodos, y_nodos, x_eval):
    n = len(x_nodos)
    # Convertimos x_eval a un arreglo de numpy para manejar tanto escalares como vectores
    x_eval = np.atleast_1d(x_eval) 
    resultado = np.zeros_like(x_eval, dtype=float)
    
    for i in range(n):
        termino = y_nodos[i]
        for j in range(n):
            if i != j:
                termino = termino * (x_eval - x_nodos[j]) / (x_nodos[i] - x_nodos[j])
        resultado += termino
    return resultado

# ==========================================
# 3. Método de Diferencias Divididas de Newton
# ==========================================
def diferencias_divididas(x_nodos, y_nodos):
    n = len(x_nodos)
    coef = np.zeros([n, n])
    coef[:, 0] = y_nodos
    
    for j in range(1, n):
        for i in range(n - j):
            coef[i][j] = (coef[i+1][j-1] - coef[i][j-1]) / (x_nodos[i+j] - x_nodos[i])
            
    return coef[0, :]

def evaluar_newton(x_nodos, coef, x_eval):
    n = len(x_nodos)
    x_eval = np.atleast_1d(x_eval)
    resultado = np.full_like(x_eval, coef[0], dtype=float)
    
    for i in range(1, n):
        termino = np.full_like(x_eval, coef[i], dtype=float)
        for j in range(i):
            termino *= (x_eval - x_nodos[j])
        resultado += termino
    return resultado

# ==========================================
# 4. Función Original (Función de Runge)
# ==========================================
def funcion_runge(x):
    return 1 / (1 + 25 * x**2)


# ==========================================
# 5. Ejecución Principal
# ==========================================
def main():
    
    # 1. Cargar datos
    x_nodos, y_nodos = leer_excel()
    
    # Rango continuo para trazar curvas suaves en las gráficas (500 puntos)
    x_continuo = np.linspace(min(x_nodos), max(x_nodos), 500)
    
    # 2. Calcular los polinomios
    y_lagrange = interpolacion_lagrange(x_nodos, y_nodos, x_continuo)
    
    coef_newton = diferencias_divididas(x_nodos, y_nodos)
    y_newton = evaluar_newton(x_nodos, coef_newton, x_continuo)
    
    # 3. Evaluar la función original
    y_original = funcion_runge(x_continuo)
    
    # 4. Evaluar en un punto específico y generar reporte

    x_esp = 0.32
    # Extraemos el valor [0] porque nuestra función devuelve un arreglo
    y_esp_lagrange = interpolacion_lagrange(x_nodos, y_nodos, x_esp)[0]
    y_esp_newton = evaluar_newton(x_nodos, coef_newton, x_esp)[0]
    y_esp_real = funcion_runge(x_esp)
    
    # Imprimir reporte en consola
    print("="*45)
    print(f"REPORTE DE INTERPOLACIÓN PARA x = {x_esp}")
    print("="*45)
    print(f"Valor real de la función: {y_esp_real:.6f}")
    print(f"Valor estimado (Lagrange): {y_esp_lagrange:.6f}")
    print(f"Valor estimado (Newton):   {y_esp_newton:.6f}")
    print("-" * 45)
    print(f"Error Absoluto (Lagrange): {abs(y_esp_real - y_esp_lagrange):.6f}")
    print(f"Error Absoluto (Newton):   {abs(y_esp_real - y_esp_newton):.6f}")
    print("="*45 + "\n")

    # ==============================
    # GRÁFICA 1: Lagrange vs Newton
    # ==============================
    plt.figure(figsize=(10, 5))
    plt.plot(x_nodos, y_nodos, 'ko', markersize=6, label='Datos Originales (Nodos)')
    plt.plot(x_continuo, y_lagrange, 'r-', linewidth=2, label='Polinomio de Lagrange')
    plt.plot(x_continuo, y_newton, 'b:', linewidth=3, label='Polinomio de Newton') 
    
    plt.plot(x_esp, y_esp_lagrange, 'c*', markersize=12, label=f'Interp. en x={x_esp}')
    plt.plot(x_esp, y_esp_newton, 'm+', markersize=12, label=f'Interp. en x={x_esp} (Newton)')

    plt.title("Comparación de Métodos de Interpolación")
    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Guardar Gráfica 1
    ruta_grafica1 = os.path.join(RUTA_GRAFICAS, "1_comparacion_metodos.png")
    plt.savefig(ruta_grafica1, dpi=300, bbox_inches='tight')
    print(f"Gráfica de comparación guardada con éxito en: {ruta_grafica1}")
    
    plt.show()
    plt.close() # Cierra la figura actual para liberar memoria de video

    # ==============================
    # GRÁFICA 2: Interpolación vs Función de Runge
    # ==============================
    plt.figure(figsize=(10, 5))
    plt.plot(x_nodos, y_nodos, 'ko', markersize=6, label='Nodos de Interpolación')
    plt.plot(x_continuo, y_lagrange, 'r--', linewidth=2, label='Polinomio Interpolante')
    plt.plot(x_continuo, y_original, 'g-', linewidth=2, label='Función Original: $f(x) = 1 / (1 + 25x^2)$')
    
    plt.plot(x_esp, y_esp_lagrange, 'rX', markersize=10, label=f'Estimado (x={x_esp})')
    plt.plot(x_esp, y_esp_real, 'gX', markersize=10, label=f'Real (x={x_esp})')

    plt.title("El Fenómeno de Runge: Interpolación vs Función Real")
    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")
    plt.ylim(-0.5, 1.5) 
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    # Guardar Gráfica 2
    ruta_grafica2 = os.path.join(RUTA_GRAFICAS, "2_fenomeno_runge.png")
    plt.savefig(ruta_grafica2, dpi=300, bbox_inches='tight')
    print(f"Gráfica de Runge guardada con éxito en: {ruta_grafica2}")
    
    plt.show()
    plt.close()

if __name__ == "__main__":
    main()