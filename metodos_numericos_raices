% Script para resolver x*cos(x) - 1 = 0
% Métodos: Bisección, Newton-Raphson y Secante
clc; clear; close all;

% Definición de la función anónima y su derivada
f = @(x) x.*cos(x) - 1;
df = @(x) cos(x) - x.*sin(x);

% Interfaz de usuario
disp('=================================================');
disp('   Búsqueda de Raíces para f(x) = x*cos(x) - 1   ');
disp('=================================================');
disp('1. Método de Bisección');
disp('2. Método de Newton-Raphson');
disp('3. Método de la Secante');
disp('4. Comparar los tres métodos');
disp('-------------------------------------------------');
opcion = input('Seleccione el método a utilizar (1-4): ');

tol = input('Ingrese la tolerancia o error máximo permitido (ej. 1e-6): ');
max_iter = 100; % Límite de seguridad para evitar bucles infinitos

disp('-------------------------------------------------');

% Ejecución según la selección
switch opcion
    case 1
        a = input('Ingrese el límite inferior del intervalo (a): ');
        b = input('Ingrese el límite superior del intervalo (b): ');
        try
            [raiz, iter, err] = biseccion(f, a, b, tol, max_iter);
            mostrar_resultados('Bisección', raiz, iter, err);
        catch ME
            disp(['Error: ', ME.message]);
        end
        
    case 2
        x0 = input('Ingrese el punto semilla (x0): ');
        [raiz, iter, err] = newton(f, df, x0, tol, max_iter);
        mostrar_resultados('Newton-Raphson', raiz, iter, err);
        
    case 3
        x0 = input('Ingrese el primer punto semilla (x0): ');
        x1 = input('Ingrese el segundo punto semilla (x1): ');
        [raiz, iter, err] = secante(f, x0, x1, tol, max_iter);
        mostrar_resultados('Secante', raiz, iter, err);
        
    case 4
        disp('Para la comparación, el intervalo [a, b] servirá como:');
        disp('- Límites para Bisección.');
        disp('- Puntos semilla x0 y x1 para la Secante.');
        disp('- El punto "a" como semilla para Newton-Raphson.');
        a = input('Ingrese el valor de a: ');
        b = input('Ingrese el valor de b: ');
        
        disp(' ');
        disp('--- Resultados de la Comparación ---');
        
        % 1. Bisección
        try
            [r_b, i_b, e_b] = biseccion(f, a, b, tol, max_iter);
            mostrar_resultados('Bisección', r_b, i_b, e_b);
        catch ME
            fprintf('Bisección: %s\n\n', ME.message);
        end
        
        % 2. Newton-Raphson
        [r_n, i_n, e_n] = newton(f, df, a, tol, max_iter);
        mostrar_resultados('Newton-Raphson', r_n, i_n, e_n);
        
        % 3. Secante
        [r_s, i_s, e_s] = secante(f, a, b, tol, max_iter);
        mostrar_resultados('Secante', r_s, i_s, e_s);
        
    otherwise
        disp('Opción no válida. Por favor, ejecute el script nuevamente.');
end

%% --- Funciones Locales de los Métodos Numéricos ---

function [x, iter, err] = biseccion(f, a, b, tol, max_iter)
    % El teorema de Bolzano requiere un cambio de signo en el intervalo
    if f(a) * f(b) >= 0
        error('El intervalo no garantiza una raíz (f(a)*f(b) >= 0). Revise sus valores.');
    end
    
    iter = 0; err = inf; x_prev = a;
    while err > tol && iter < max_iter
        iter = iter + 1;
        x = (a + b) / 2;
        
        % Cálculo del error absoluto aproximado
        if iter > 1
            err = abs(x - x_prev);
        end
        x_prev = x;
        
        % Evaluación del subintervalo
        if f(a) * f(x) < 0
            b = x;
        else
            a = x;
        end
        
        % Condición de raíz exacta
        if f(x) == 0, err = 0; break; end 
    end
end

function [x, iter, err] = newton(f, df, x0, tol, max_iter)
    iter = 0; err = inf; x = x0;
    while err > tol && iter < max_iter
        iter = iter + 1;
        derivada = df(x);
        
        if derivada == 0
            warning('Derivada cero detectada. El método de Newton fallará.');
            break;
        end
        
        x_new = x - f(x) / derivada;
        err = abs(x_new - x); % Error absoluto aproximado
        x = x_new;
    end
end

function [x, iter, err] = secante(f, x0, x1, tol, max_iter)
    iter = 0; err = inf;
    while err > tol && iter < max_iter
        iter = iter + 1;
        
        denominador = f(x1) - f(x0);
        if denominador == 0
            warning('División por cero detectada en el método de la Secante.');
            break;
        end
        
        x_new = x1 - f(x1) * (x1 - x0) / denominador;
        err = abs(x_new - x1); % Error absoluto aproximado
        
        % Actualización de puntos
        x0 = x1;
        x1 = x_new;
    end
    x = x1;
end

function mostrar_resultados(nombre_metodo, raiz, iter, err)
    fprintf('Método: %s\n', nombre_metodo);
    fprintf('  - Raíz obtenida: %.8f\n', raiz);
    fprintf('  - Número de iteraciones: %d\n', iter);
    fprintf('  - Error estimado: %.4e\n\n', err);
end