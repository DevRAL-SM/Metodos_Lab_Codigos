#include <iostream>
#include <iomanip>
#include <fstream> // Librería necesaria para manejar archivos

using namespace std;

// Definimos un tamaño máximo para los arrays
const int MAX = 100;

double evaluarNewton(double valor, double x[], double diff[][MAX], int n) {
    double resultado = diff[0][0];
    double productoX = 1.0;
    for (int i = 1; i < n; i++) { //inicia el calculo desde la b0 = y0 = dif[0,0] y va aplicando la formula en esa misma fila
        productoX *= (valor - x[i - 1]); // bi(x-xi)(x-x(i-1))...
        resultado += productoX * diff[0][i]; //acumala la suma
    }
    return resultado;
}

int main() {
    int n;
    double x[MAX];
    double diff[MAX][MAX]; // Matriz para las diferencias divididas

    cout << "--- Interpolación de Newton (Usando Arrays) ---" << endl;
    cout << "Ingrese el numero de puntos (max " << MAX << "): ";
    cin >> n;

    if (n > MAX) {
        cout << "Error: El numero de puntos excede el maximo permitido." << endl;
        return 1;
    }

    // Lectura de datos
    cout << "Ingrese los valores de x e y:" << endl;
    for (int i = 0; i < n; i++) {
        cout << "Punto " << i << " [x y]: ";
        cin >> x[i] >> diff[i][0]; // ingresa el valor de xi en el array x[i] e yi en la matriz diff[i][0] (en la columna 0 en la fila i)
    }

    // 1. Cálculo de la Tabla de Diferencias Divididas
    for (int j = 1; j < n; j++) { //empieza en la columna 1 y lo avanza hasta n
        for (int i = 0; i < n - j; i++) { //coloco los datos en la columna j
            diff[i][j] = (diff[i + 1][j - 1] - diff[i][j - 1]) / (x[i + j] - x[i]); //calcula la pendiente de los dos datos de la columna anterior
        }
    }

	// 2. Exportar datos para graficar
    ofstream archivo("datos_interpolacion.csv");
    if (archivo.is_open()) {
        archivo << "x,y" << endl; // Cabecera del CSV

        // Determinamos el rango para la grafica
        double minX = x[0], maxX = x[n-1];
        // Generamos 100 puntos entre el primer y ultimo x
        double paso = (maxX - minX) / 100.0;

        for (int i = 0; i <= 100; i++) {
            double xi = minX + (i * paso);
            double yi = evaluarNewton(xi, x, diff, n);
            archivo << xi << "," << yi << endl;
        }
        archivo.close();
        cout << "\n[OK] Archivo 'datos_interpolacion.csv' generado con exito." << endl;
    } else {
        cout << "\n[Error] No se pudo crear el archivo." << endl;
    }

// 3. Prueba rapida de interpolacion en consola
    double valorX;
    cout << "\nIngrese un valor de x para interpolar en consola: ";
    cin >> valorX;
    cout << "Resultado: " << evaluarNewton(valorX, x, diff, n) << endl;

    return 0;
}
