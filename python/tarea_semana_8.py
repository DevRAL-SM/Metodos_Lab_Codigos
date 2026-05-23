"""
=============================================================
  MÉTODOS NUMÉRICOS - Lectura desde Excel
=============================================================
  Opciones:
    1) Interpolación: Spline Cúbico Natural vs Diferencias
       Divididas de Newton (el usuario ingresa los puntos x)
    2) Primera derivada por Diferencias Centradas
       (el usuario ingresa los valores x directamente)
    3) Raíces por Bisección (tolerancia 1e-3)
=============================================================
  CONFIGURACIÓN — editar las tres constantes de abajo:
    RUTA_EXCEL   → ruta del archivo Excel de entrada
    RUTA_GRAFICAS → carpeta donde se guardarán las imágenes
=============================================================
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# ─────────────────────────────────────────────────────────
#  ★  RUTAS FIJAS — EDITAR SEGÚN TU EQUIPO
# ─────────────────────────────────────────────────────────
# Carpeta donde está guardado este script (punto de referencia fijo)
_BASE = os.path.dirname(os.path.abspath(__file__))

# os.path.abspath() resuelve los '..' y devuelve la ruta absoluta real,
# independientemente del directorio desde donde se ejecute el script.
RUTA_EXCEL    = os.path.abspath(os.path.join(_BASE, '..', 'data', 'raw', 'biosensor_output.xlsx'))
RUTA_GRAFICAS = os.path.abspath(os.path.join(_BASE, '..', 'data', 'processed'))
# ─────────────────────────────────────────────────────────


def _asegurar_carpeta(ruta: str) -> None:
    """Crea la carpeta de gráficas si aún no existe."""
    os.makedirs(ruta, exist_ok=True)


def _ruta_imagen(nombre_archivo: str) -> str:
    """Devuelve la ruta completa de guardado para una imagen."""
    _asegurar_carpeta(RUTA_GRAFICAS)
    return os.path.join(RUTA_GRAFICAS, nombre_archivo)


# ─────────────────────────────────────────────
#  LECTURA DEL ARCHIVO EXCEL
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
#  DIFERENCIAS DIVIDIDAS DE NEWTON
# ─────────────────────────────────────────────
def tabla_diferencias_divididas(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Devuelve los coeficientes del polinomio de Newton."""
    n = len(x)
    coef = y.copy().astype(float)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])
    return coef


def evaluar_newton(x_data: np.ndarray, coef: np.ndarray, x_eval) -> float:
    """Evaluación por el método de Horner generalizado."""
    n = len(coef) - 1
    resultado = coef[n]
    for i in range(n - 1, -1, -1):
        resultado = resultado * (x_eval - x_data[i]) + coef[i]
    return resultado


# ─────────────────────────────────────────────
#  UTILIDADES DE ENTRADA
# ─────────────────────────────────────────────
def pedir_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("  ✗ Ingrese un número válido.")


def pedir_n_puntos_x(x_min: float, x_max: float, n: int) -> np.ndarray:
    """
    Solicita al usuario 'n' valores x dentro del dominio [x_min, x_max].
    Repite la petición si el valor está fuera de rango.
    """
    puntos = []
    print(f"\n  Dominio disponible: [{x_min:.6f}, {x_max:.6f}]")
    for i in range(1, n + 1):
        while True:
            val = pedir_float(f"  Ingrese el punto x_{i} a estimar: ")
            if x_min <= val <= x_max:
                puntos.append(val)
                break
            print(f"  ✗ {val} está fuera del dominio [{x_min:.6f}, {x_max:.6f}].")
    return np.array(puntos)


# ─────────────────────────────────────────────
#  OPCIÓN 1 — SPLINE CÚBICO NATURAL vs NEWTON
# ─────────────────────────────────────────────
def opcion_spline_vs_newton(x: np.ndarray, y: np.ndarray) -> None:
    print("\n" + "="*60)
    print("  OPCIÓN 1 — Spline Cúbico Natural vs Newton")
    print("="*60)

    # ── El usuario elige cuántos puntos y sus valores ──
    while True:
        try:
            n_pts = int(input("\n  ¿Cuántos puntos desea estimar? (mínimo 1): "))
            if n_pts >= 1:
                break
            print("  ✗ Ingrese un entero mayor o igual a 1.")
        except ValueError:
            print("  ✗ Ingrese un entero válido.")

    x_estimar = pedir_n_puntos_x(x[0], x[-1], n_pts)

    # ── Spline Cúbico Natural ──────────────────
    cs = CubicSpline(x, y, bc_type="natural")
    x_fino        = np.linspace(x[0], x[-1], 500)
    y_spline_fino = cs(x_fino)
    y_spline_pts  = cs(x_estimar)

    # ── Diferencias Divididas de Newton ────────
    coef_newton   = tabla_diferencias_divididas(x, y)
    y_newton_fino = np.array([evaluar_newton(x, coef_newton, xi) for xi in x_fino])
    y_newton_pts  = np.array([evaluar_newton(x, coef_newton, xi) for xi in x_estimar])

    # ── Tabla comparativa ──────────────────────
    print(f"\n  {'Punto x':>12}  {'Spline':>18}  {'Newton':>18}  {'|Error|':>14}")
    print("  " + "-"*68)
    for i in range(n_pts):
        err = abs(y_spline_pts[i] - y_newton_pts[i])
        print(f"  {x_estimar[i]:>12.6f}  {y_spline_pts[i]:>18.10f}  "
              f"{y_newton_pts[i]:>18.10f}  {err:>14.6e}")

    # ── Gráfica ────────────────────────────────
    ruta_img = _ruta_imagen("opcion1_spline_newton.png")
    fig, ax  = plt.subplots(figsize=(10, 5))
    ax.plot(x_fino, y_spline_fino, "b-",  lw=2,   label="Spline Cúbico Natural")
    ax.plot(x_fino, y_newton_fino, "r--", lw=1.5, label="Diferencias Divididas Newton")
    ax.plot(x, y,  "ko", ms=6, zorder=5, label="Datos originales")
    ax.scatter(x_estimar, y_spline_pts, marker="^", s=90, c="blue",
               zorder=6, label="Estimados (Spline)")
    ax.scatter(x_estimar, y_newton_pts, marker="v", s=90, c="red",
               zorder=6, label="Estimados (Newton)")
    # Anotar cada punto estimado
    for i in range(n_pts):
        ax.annotate(f"x={x_estimar[i]:.3f}", xy=(x_estimar[i], y_spline_pts[i]),
                    xytext=(5, 8), textcoords="offset points", fontsize=8, color="blue")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title("Spline Cúbico Natural vs Diferencias Divididas de Newton")
    ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(ruta_img, dpi=150)
    plt.show()
    print(f"\n  Gráfica guardada en '{ruta_img}'")


# ─────────────────────────────────────────────
#  OPCIÓN 2 — DERIVADA POR DIFERENCIAS CENTRADAS
# ─────────────────────────────────────────────
def opcion_diferencias_centradas(x: np.ndarray, y: np.ndarray) -> None:
    print("\n" + "="*60)
    print("  OPCIÓN 2 — Primera Derivada: Diferencias Centradas")
    print("="*60)

    n = len(x)
    if n < 3:
        print("  ✗ Se necesitan al menos 3 puntos para diferencias centradas.")
        return

    # Mostrar tabla de puntos disponibles
    print(f"\n  {'Índice':>7}  {'x':>14}  {'y':>14}")
    print("  " + "-"*40)
    for i in range(n):
        marca = "  ← extremo" if i == 0 or i == n - 1 else ""
        print(f"  {i:>7}  {x[i]:>14.6f}  {y[i]:>14.6f}{marca}")

    # Índices interiores válidos
    indices_validos = list(range(1, n - 1))
    print(f"\n  (Puntos interiores válidos: índices {indices_validos[0]} … {indices_validos[-1]})")

    def pedir_indice(orden: str) -> int:
        while True:
            try:
                idx = int(input(f"\n  Ingrese el índice del {orden} punto: "))
                if idx in indices_validos:
                    return idx
                print(f"  ✗ El índice debe estar entre {indices_validos[0]} y {indices_validos[-1]}.")
            except ValueError:
                print("  ✗ Ingrese un entero válido.")

    idx1 = pedir_indice("primer")
    idx2 = pedir_indice("segundo")
    idx3 = pedir_indice("tercer")

    # ── Calcular y mostrar resultado para cada punto ──
    derivadas_calc = {}
    for idx in [idx1, idx2, idx3]:
        h = x[idx + 1] - x[idx - 1]          # paso total (funciona para paso no uniforme)
        deriv = (y[idx + 1] - y[idx - 1]) / h
        derivadas_calc[idx] = deriv

        print(f"\n  ─── Punto x[{idx}] = {x[idx]:.6f} ───")
        print(f"    x[i-1] = {x[idx-1]:>12.6f}   y[i-1] = {y[idx-1]:>14.10f}")
        print(f"    x[i]   = {x[idx]:>12.6f}   y[i]   = {y[idx]:>14.10f}")
        print(f"    x[i+1] = {x[idx+1]:>12.6f}   y[i+1] = {y[idx+1]:>14.10f}")
        print(f"    h total = x[i+1] - x[i-1] = {h:.6f}")
        print(f"    f'(x[{idx}]) ≈ (y[i+1] - y[i-1]) / h = {deriv:.10f}")

    # ── Derivada sobre todo el dominio interior ──
    derivs = np.full(n, np.nan)
    for i in range(1, n - 1):
        derivs[i] = (y[i + 1] - y[i - 1]) / (x[i + 1] - x[i - 1])

    # ── Gráfica ────────────────────────────────
    ruta_img = _ruta_imagen("opcion2_derivada_centrada.png")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    ax1.plot(x, y, "bo-", ms=5, label="Señal original")
    for idx in [idx1, idx2, idx3]:
        ax1.axvline(x[idx], color="orange", lw=1, ls="--", alpha=0.7)
        ax1.scatter(x[idx], y[idx], s=100, c="orange", zorder=6)
    ax1.set_ylabel("f(x)"); ax1.legend(); ax1.grid(True, alpha=0.3)

    ax2.plot(x[1:-1], derivs[1:-1], "r^-", ms=5, label="f'(x) — Dif. Centradas")
    ax2.axhline(0, color="gray", lw=0.8, ls="--")
    for idx in [idx1, idx2, idx3]:
        ax2.scatter(x[idx], derivadas_calc[idx], s=130, zorder=6,
                    edgecolors="black", linewidths=1.5,
                    label=f"f'(x[{idx}])={derivadas_calc[idx]:.4f}")
        ax2.annotate(f"f'({x[idx]:.3f})={derivadas_calc[idx]:.4f}",
                     xy=(x[idx], derivadas_calc[idx]),
                     xytext=(6, 8), textcoords="offset points", fontsize=8)
    ax2.set_xlabel("x"); ax2.set_ylabel("f'(x)"); ax2.legend(); ax2.grid(True, alpha=0.3)

    plt.suptitle("Primera Derivada — Diferencias Centradas")
    plt.tight_layout()
    plt.savefig(ruta_img, dpi=150)
    plt.show()
    print(f"\n  Gráfica guardada en '{ruta_img}'")


# ─────────────────────────────────────────────
#  OPCIÓN 3 — RAÍCES POR BISECCIÓN (tol = 1e-30)
# ─────────────────────────────────────────────
def opcion_biseccion(x: np.ndarray, y: np.ndarray) -> None:
    print("\n" + "="*60)
    print("  OPCIÓN 3 — Raíces por Bisección  (tolerancia 1×10⁻³)")
    print("="*60)

    coef = tabla_diferencias_divididas(x, y)

    def f(xi):
        return evaluar_newton(x, coef, xi)

    print(f"\n  Función: polinomio interpolante de Newton grado {len(x)-1}")
    print(f"  Dominio disponible: [{x[0]:.6f}, {x[-1]:.6f}]")
    print("\n  Ingrese el intervalo [a, b] donde buscar la raíz:")

    while True:
        a = pedir_float("  a = ")
        b = pedir_float("  b = ")
        if abs(b - a) < 1e-60:
            print("  ✗ El intervalo es demasiado pequeño.")
            continue
        fa, fb = f(a), f(b)
        if fa * fb < 0:
            break
        print(f"  ✗ f(a)·f(b) = {fa*fb:.4e} > 0 → no hay garantía de raíz en [{a}, {b}].")
        print("  Intente otro intervalo.")

    TOL    = 1e-3
    MAX_IT = 10_000
    historial = []

    print(f"\n  {'Iter':>5}  {'a':>22}  {'b':>22}  {'c':>22}  {'f(c)':>15}  {'|b-a|':>12}")
    print("  " + "-"*102)

    for k in range(1, MAX_IT + 1):
        c  = (a + b) / 2.0
        fc = f(c)
        error = abs(b - a)
        historial.append((k, a, b, c, fc, error))

        if k <= 10 or k % 100 == 0 or error < TOL * 10:
            print(f"  {k:>5}  {a:>22.15e}  {b:>22.15e}  {c:>22.15e}  "
                  f"{fc:>15.6e}  {error:>12.4e}")

        if error < TOL or fc == 0.0:
            break
        if f(a) * fc < 0:
            b = c
        else:
            a = c

    raiz       = (a + b) / 2.0
    iter_total = len(historial)

    print(f"\n  ✔ Raíz aproximada : {raiz:.30e}")
    print(f"    f(raíz)          : {f(raiz):.6e}")
    print(f"    Tolerancia final : {abs(b-a):.4e}")
    print(f"    Iteraciones      : {iter_total}")

    # ── Gráfica ────────────────────────────────
    margen   = max(abs(b - a) * 0.5, 0.5)
    x_plot   = np.linspace(raiz - margen, raiz + margen, 600)
    y_plot   = np.array([f(xi) for xi in x_plot])
    ruta_img = _ruta_imagen("opcion3_biseccion.png")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x_plot, y_plot, "b-", lw=2, label="Polinomio interpolante (Newton)")
    ax.axhline(0, color="gray", lw=0.8, ls="--")
    ax.scatter([raiz], [f(raiz)], s=120, c="red", zorder=6,
               label=f"Raíz ≈ {raiz:.8f}")
    ax.annotate(f"raíz = {raiz:.8f}", xy=(raiz, 0),
                xytext=(10, 15), textcoords="offset points", fontsize=9, color="red")
    ax.set_xlabel("x"); ax.set_ylabel("f(x)")
    ax.set_title("Método de Bisección — Raíz del Polinomio Interpolante")
    ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(ruta_img, dpi=150)
    plt.show()
    print(f"\n  Gráfica guardada en '{ruta_img}'")


# ─────────────────────────────────────────────
#  MENÚ PRINCIPAL
# ─────────────────────────────────────────────
def mostrar_menu() -> None:
    print("\n" + "╔" + "═"*56 + "╗")
    print("║       MÉTODOS NUMÉRICOS — Lectura desde Excel         ║")
    print("╠" + "═"*56 + "╣")
    print("║  1)  Spline Cúbico Natural + Newton (puntos libres)   ║")
    print("║  2)  Primera Derivada — Diferencias Centradas         ║")
    print("║  3)  Raíces por Bisección  (tol = 1×10⁻³)            ║")
    print("║  0)  Salir                                            ║")
    print("╚" + "═"*56 + "╝")


def main() -> None:
    # ── Carga única del Excel ──────────────────
    print(f"\n  Cargando datos desde '{RUTA_EXCEL}' ...")
    x, y = leer_excel()
    print(f"  ✔ {len(x)} puntos cargados  |  "
          f"x ∈ [{x[0]:.4f}, {x[-1]:.4f}]  |  "
          f"y ∈ [{y.min():.4f}, {y.max():.4f}]")
    print(f"  Las gráficas se guardarán en: '{os.path.abspath(RUTA_GRAFICAS)}'")

    acciones = {
        "1": opcion_spline_vs_newton,
        "2": opcion_diferencias_centradas,
        "3": opcion_biseccion,
    }

    while True:
        mostrar_menu()
        op = input("\n  Seleccione una opción: ").strip()
        if op == "0":
            print("\n  ¡Hasta luego!\n")
            break
        elif op in acciones:
            acciones[op](x, y)
        else:
            print("  ✗ Opción no válida. Intente de nuevo.")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()