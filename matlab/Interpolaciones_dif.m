% =========================================================================
% Código de Interpolación Múltiple: Matricial, Lagrange, Newton y Spline
% =========================================================================

clear; clc; close all;

% 1. Carga de Datos desde Excel
% Usamos 'readmatrix' por ser el estándar moderno y más seguro.
% (Si usas una versión muy antigua de Matlab, reemplázalo por 'xlsread')
try
    datos = readmatrix('datos.xlsx');
    x = datos(:, 1);
    y = datos(:, 2);
catch
    error('No se pudo leer el archivo. Verifica que "datos.xlsx" exista en la ruta actual.');
end

% Validar que los vectores tengan el mismo tamaño
n = length(x);
if length(y) ~= n
    error('Los vectores x e y deben tener la misma longitud.');
end

% Vector de evaluación para generar curvas suaves
% Generamos 200 puntos entre el valor mínimo y máximo de x
xx = linspace(min(x), max(x), 200);

% Crear la figura principal
figure('Name', 'Análisis Comparativo de Interpolación', 'NumberTitle', 'off', 'Position', [100, 100, 1000, 700]);

% -------------------------------------------------------------------------
% 1. MÉTODO MATRICIAL (Vandermonde)
% -------------------------------------------------------------------------
% Consiste en resolver el sistema V * a = y, donde V es la matriz de Vandermonde.
V = vander(x);
coef_matricial = V \ y; % Resolución del sistema lineal
yy_matricial = polyval(coef_matricial, xx);

subplot(2, 2, 1);
plot(x, y, 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 6); hold on;
plot(xx, yy_matricial, 'b-', 'LineWidth', 1.5);
title('1. Método Matricial (Polinomio Global)');
xlabel('x'); ylabel('y');
grid on; legend('Datos Excel', 'Interpolación', 'Location', 'best');

% -------------------------------------------------------------------------
% 2. MÉTODO DE LAGRANGE
% -------------------------------------------------------------------------
% Construcción de los polinomios base de Lagrange y suma ponderada.
yy_lagrange = zeros(size(xx));
for i = 1:n
    L = ones(size(xx));
    for j = 1:n
        if i ~= j
            L = L .* (xx - x(j)) / (x(i) - x(j));
        end
    end
    yy_lagrange = yy_lagrange + y(i) * L;
end

subplot(2, 2, 2);
plot(x, y, 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 6); hold on;
plot(xx, yy_lagrange, 'g-', 'LineWidth', 1.5);
title('2. Interpolación de Lagrange');
xlabel('x'); ylabel('y');
grid on; legend('Datos Excel', 'Interpolación', 'Location', 'best');

% -------------------------------------------------------------------------
% 3. MÉTODO DE NEWTON (Diferencias Divididas)
% -------------------------------------------------------------------------
% Cálculo de la tabla de diferencias divididas
D = zeros(n, n);
D(:, 1) = y;
for j = 2:n
    for i = 1:(n - j + 1)
        D(i, j) = (D(i+1, j-1) - D(i, j-1)) / (x(i+j-1) - x(i));
    end
end

% Evaluación del polinomio de Newton
yy_newton = D(1, 1) * ones(size(xx));
P_base = ones(size(xx));
for j = 2:n
    P_base = P_base .* (xx - x(j-1));
    yy_newton = yy_newton + D(1, j) * P_base;
end

subplot(2, 2, 3);
plot(x, y, 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 6); hold on;
plot(xx, yy_newton, 'm-', 'LineWidth', 1.5);
title('3. Método de Newton');
xlabel('x'); ylabel('y');
grid on; legend('Datos Excel', 'Interpolación', 'Location', 'best');

% -------------------------------------------------------------------------
% 4. SPLINE CÚBICO
% -------------------------------------------------------------------------
% Interpolación fragmentada mediante polinomios de grado 3.
% Matlab posee una función nativa altamente optimizada para esto.
yy_spline = spline(x, y, xx);

subplot(2, 2, 4);
plot(x, y, 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 6); hold on;
plot(xx, yy_spline, 'k-', 'LineWidth', 1.5);
title('4. Spline Cúbico (Trazadores)');
xlabel('x'); ylabel('y');
grid on; legend('Datos Excel', 'Interpolación', 'Location', 'best');