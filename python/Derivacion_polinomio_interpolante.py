import os
import numpy as np
import pandas as pd
import sympy as sp

_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_EXCEL = os.path.abspath(os.path.join(_BASE, '..', 'data', 'raw', 'Derivacion_numerica.xlsx'))

def interpolacion_y_derivadas_matricial(ruta_excel, x_evaluar):
    # 1. Cargar los datos desde el archivo Excel
    if not os.path.exists(ruta_excel):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_excel}")
        
    df = pd.read_excel(ruta_excel)
    
    # Extraer las columnas x e y como arreglos numéricos
    x_datos = df['x'].to_numpy(dtype=float)
    y_datos = df['y'].to_numpy(dtype=float)
    
    n_puntos = len(x_datos)
    grado = n_puntos - 1
    
    print(f"Datos leídos desde el Excel ({n_puntos} puntos, Polinomio de grado {grado}):")
    for xi, yi in zip(x_datos, y_datos):
        print(f"  Punto: ({xi}, {yi})")
    print("-" * 60)
    
    # 2. Construir la Matriz de Vandermonde
    # np.vander genera la matriz de potencias decrecientes: [x^n, x^(n-1), ..., 1]
    V = np.vander(x_datos, increasing=False)
    
    # 3. Resolver el sistema lineal V * a = y para encontrar los coeficientes
    # coeficientes[0] será a_n, coeficientes[1] será a_(n-1), ..., coeficientes[n] será a_0
    coeficientes = np.linalg.solve(V, y_datos)
    
    # 4. Construcción simbólica del polinomio con SymPy
    x = sp.Symbol('x')
    polinomio = 0
    for i, coef in enumerate(coeficientes):
        polinomio += coef * (x ** (grado - i))
    
    # Simplificar la expresión para visualización limpia
    polinomio_simplificado = sp.simplify(polinomio)
    
    # 5. Calcular la primera y segunda derivada de forma analítica
    primera_derivada = sp.diff(polinomio_simplificado, x)
    segunda_derivada = sp.diff(primera_derivada, x)
    
    # 6. Evaluar el polinomio y sus derivadas en el punto específico x_evaluar
    val_pol = polinomio_simplificado.evalf(subs={x: x_evaluar})
    val_der1 = primera_derivada.evalf(subs={x: x_evaluar})
    val_der2 = segunda_derivada.evalf(subs={x: x_evaluar})
    
    # --- Presentación de Resultados ---
    print("============================================================")
    print("                    RESULTADOS DEL ANÁLISIS                 ")
    print("============================================================")
    print(f"Polinomio Interpolador P(x):\n  {polinomio_simplificado}\n")
    print(f"Primera Derivada P'(x):\n  {primera_derivada}\n")
    print(f"Segunda Derivada P''(x):\n  {segunda_derivada}\n")
    print("-" * 60)
    print(f"Evaluación numérica exacta en x = {x_evaluar}:")
    print(f"  P({x_evaluar})   = {val_pol:.6f}")
    print(f"  P'({x_evaluar})  = {val_der1:.6f}")
    print(f"  P''({x_evaluar}) = {val_der2:.6f}")
    print("============================================================")

if __name__ == "__main__":
    nombre_archivo = RUTA_EXCEL
    punto_evaluacion = 2.25
    
    # Ejecutar algoritmo principal
    interpolacion_y_derivadas_matricial(nombre_archivo, punto_evaluacion)