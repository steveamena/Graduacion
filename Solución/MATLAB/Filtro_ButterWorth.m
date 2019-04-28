%%Calculador de filtro de Butterworth

frecuencia = 15; %Hz
omega = 2*pi*frecuencia;

s = tf('s');
a0 = 1;
a1= 1.4142*omega;
a2 = omega^2;
a3 = 1;
a4 = omega*1.8475;
a5 = a2;

P1s = (a0*s^2+a1*s+a2);
P2s = (a3*s^2+a4*s+a5);
Qs = P1s;%*P2s;
Gs = a2/Qs;%*a5/Qs