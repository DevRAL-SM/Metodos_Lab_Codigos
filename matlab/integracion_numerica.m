% =========================================================================
% INTEGRACIÓN NUMÉRICA: TRABAJO TERMODINÁMICO ISOTÉRMICO
% Métodos: Trapecio Compuesto, Simpson 1/3, Simpson 3/8 (n=12) y Gauss (m=3)
% Incluye: Cálculo del Valor Real mediante REGRESIÓN LINEAL
% =========================================================================

clc; clear; close all;

% 1. LEER DATOS DEL EXCEL DESDE CARPETA HERMANA USANDO RUTA RELATIVA
% ".." significa subir un nivel (salir de la carpeta de scripts)
ruta_completa = fullfile('..', 'data', 'raw', 'integracion_numerica.xlsx');

try
    datos = readmatrix(ruta_completa);
    fprintf('Archivo cargado exitosamente desde: %s\n', ruta_completa);
catch
    error('No se pudo encontrar el archivo. Verifica que la ruta relativa sea correcta:\n%s', ruta_completa);
end

% Asignación de variables termodinámicas
x = datos(:, 1); % Volumen (V)
y = datos(:, 2); % Presión (P)
a = x(1);
b = x(end);

fprintf('Procesando datos termodinámicos mediante Regresión Lineal...\n');

% =========================================================================
% CÁLCULO DEL VALOR REAL ANALÍTICO POR REGRESIÓN LINEAL
% Ecuación: P = C * (1/V) + intercepto
% =========================================================================
X_reg = 1 ./ x; % Variable independiente linealizada (1/V)

% polyfit encuentra los coeficientes [pendiente, intercepto]
coeficientes = polyfit(X_reg, y, 1); 

C = coeficientes(1);        % La pendiente es nuestra constante térmica
intercepto = coeficientes(2); % Debería ser cercano a 0 teóricamente

v_inicial = 1;
v_final = 4;
valor_real = C * log(v_final / v_inicial); 

% =========================================================================
% MÉTODO 1: REGLA DEL TRAPECIO COMPUESTO
% =========================================================================
I_trap = 0;
for i = 1:(length(x)-1)
    h_trap = x(i+1) - x(i);
    I_trap = I_trap + h_trap * (y(i+1) + y(i)) / 2;
end

% =========================================================================
% PREPARACIÓN PARA SIMPSON: Interpolación a n=12 intervalos (13 puntos)
% =========================================================================
n = 12; 
puntos = n + 1; 
x_simp = linspace(a, b, puntos);
y_simp = spline(x, y, x_simp); 
h = (b - a) / n; 

% =========================================================================
% MÉTODO 2: REGLA DE SIMPSON 1/3 (n=12)
% =========================================================================
suma_impares = 0;
suma_pares = 0;

for i = 2:n
    if mod(i, 2) == 0 
        suma_impares = suma_impares + y_simp(i);
    else              
        suma_pares = suma_pares + y_simp(i);
    end
end
I_simp13 = (h / 3) * (y_simp(1) + 4 * suma_impares + 2 * suma_pares + y_simp(end));

% =========================================================================
% MÉTODO 3: REGLA DE SIMPSON 3/8 (n=12)
% =========================================================================
suma_38 = 0;
for i = 2:n
    if mod(i-1, 3) == 0
        suma_38 = suma_38 + 2 * y_simp(i);
    else
        suma_38 = suma_38 + 3 * y_simp(i);
    end
end
I_simp38 = (3 * h / 8) * (y_simp(1) + suma_38 + y_simp(end));

% =========================================================================
% MÉTODO 4: CUADRATURA DE GAUSS-LEGENDRE (m=3) con Splines
% =========================================================================
z = [-sqrt(3/5), 0, sqrt(3/5)];
w = [5/9, 8/9, 5/9];

x_gauss = ((b - a) .* z + (b + a)) / 2;
y_gauss = spline(x, y, x_gauss); 
I_gauss = ((b - a) / 2) * sum(w .* y_gauss);

% =========================================================================
% CÁLCULO DE ERRORES RELATIVOS PORCENTUALES
% =========================================================================
e_trap   = abs((valor_real - I_trap) / valor_real) * 100;
e_simp13 = abs((valor_real - I_simp13) / valor_real) * 100;
e_simp38 = abs((valor_real - I_simp38) / valor_real) * 100;
e_gauss  = abs((valor_real - I_gauss) / valor_real) * 100;

% =========================================================================
% IMPRESIÓN DE LA TABLA EN TERMINAL
% =========================================================================
fprintf('\n==================================================================\n');
fprintf(' RESULTADOS DEL AJUSTE POR REGRESIÓN LINEAL\n');
fprintf(' Constante C (Pendiente): %.4f\n', C);
fprintf(' Intercepto (ideal = 0):  %.4f\n', intercepto);
fprintf(' Valor Real Analítico:    %.6f\n', valor_real);
fprintf('==================================================================\n');
fprintf('%-25s | %-16s | %-15s\n', 'MÉTODO', 'VALOR APROX.', 'ERROR REL. (%)');
fprintf('------------------------------------------------------------------\n');
fprintf('%-25s | %-16.6f | %-15.4e\n', 'Trapecio Compuesto', I_trap, e_trap);
fprintf('%-25s | %-16.6f | %-15.4e\n', 'Simpson 1/3 (n=12)', I_simp13, e_simp13);
fprintf('%-25s | %-16.6f | %-15.4e\n', 'Simpson 3/8 (n=12)', I_simp38, e_simp38);
fprintf('%-25s | %-16.6f | %-15.4e\n', 'Gauss-Legendre (m=3)', I_gauss, e_gauss);
fprintf('==================================================================\n\n');