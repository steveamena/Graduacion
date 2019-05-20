%%Diseño del I_PD con el metodo de realimentacion 
%%de estado integral
s=tf('s');
Gs = Ms;

%%
a0 = Gs.den{1}(3);
a1 = Gs.den{1}(2);
a2 = Gs.den{1}(1);

c0 = Gs.num{1}(3);
c1 = Gs.num{1}(1);

A = [0 1;
    -a0 -a1];
B = [0;1];
C = [c0 c1];
D = 0;
% A = [0 1 0
%     0 0 1
%     -a0 -a1 -a2];
% B = [0 ; 0 ; 1];
% C = [c0  0  c2];
% D = 0;
Motor_ss = ss(A,B,C,D); %Crea un sistema con las matrices

%Discretización
Tmuestreo=0.01;
[N, D]=tfdata(Ms);
Ancf=[[0 1];[-D{1}(3) -D{1}(2)]];
Bncf=[N{1}(2);N{1}(3)];
Cncf=[1 0];

%   matrices aumentadas por el metodo del Ogata
Aaum=[[Ancf [0;0]];[-Cncf 0]];
Baum=[Bncf;0];

%polos deseados
p1=-0.3+0.001*1i;
p2=conj(p1);
p3=-20;
%polos en tiempo discreto
p1d=exp(p1*Tmuestreo);
p2d=conj(p1d);
p3d=0;

%Calculo de la matriz K
K=place(Aaum,Baum,[p1 p2 p3]);
Kp = K(1);
Ki = -K(3);
Kd = K(2);

Ts=(Ki/s*Ms)/(1+(Kp+Ki/s+Kd*s)*Ms);
Ts=minreal(Ts);
%zpk(Ts);
[Kp Ki Kd]

