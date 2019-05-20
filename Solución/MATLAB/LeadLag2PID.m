%%%Funcion que sintetiza PID a partir de controlador de adelanto atraso

[N,D] = tfdata(C);
[r,p,k] = residue(N{1},D{1});
Kp = k;
Kd = r/p;