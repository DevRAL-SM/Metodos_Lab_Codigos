#include <iostream>
#include <iomanip>
#include <fstream>

using namespace std;

const int MAX = 100;

// Función para calcular el polinomio de Lagrange en un punto x
double evaluarLagrange(double valor, double x[], double y[], int n) {
    double resultado = 0;

    for (int i = 0; i < n; i++) {
        double termino = y[i];
        for (int j = 0; j < n; j++) {
            if (i != j) {
                termino *= (valor - x[j]) / (x[i] - x[j]);
            }
        }
        resultado += termino;
    }
    return resultado;
}

int main() {
    int n;
    double x[MAX];
    double y[MAX];

    cout << "--- Interpolacion de Lagrange + Exportacion CSV ---" << endl;
    cout << "Ingrese el numero de puntos: ";
    cin >> n;

    if (n > MAX) return 1;

    cout << "Ingrese los valores de x e y:" << endl;
    for (int i = 0; i < n; i++) {
        cout << "Punto " << i << " [x y]: ";
        cin >> x[i] >> y[i];
    }

    // 1. Exportar datos para graficar
    ofstream archivo("lagrange_grafica.csv");
    if (archivo.is_open()) {
        archivo << "x,y" << endl;

        double minX = x[0], maxX = x[0];
        for(int i=1; i<n; i++) { // Buscamos rango real
            if(x[i] < minX) minX = x[i];
            if(x[i] > maxX) maxX = x[i];
        }

        double paso = (maxX - minX) / 100.0;
        for (int i = 0; i <= 100; i++) {
            double xi = minX + (i * paso);
            double yi = evaluarLagrange(xi, x, y, n);
            archivo << xi << "," << yi << endl;
        }
        archivo.close();
        cout << "\n[OK] Archivo 'lagrange_grafica.csv' generado." << endl;
    }

    // 2. Prueba en consola
    double valorX;
    cout << "\nIngrese el valor de x a interpolar: ";
    cin >> valorX;
    cout << "Resultado (Lagrange): " << evaluarLagrange(valorX, x, y, n) << endl;

    return 0;
}
