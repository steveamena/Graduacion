volatile bool CruceCero = false;
int contador = 0;
int Time = 0;
int Angulo = 45;
int deltaT = 0;
int tiempo = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(2,INPUT);
  pinMode(5,OUTPUT);
  Serial.begin(115200);
  attachInterrupt(0, zeroCrossing,RISING);
  digitalWrite(5,LOW);
}

void zeroCrossing(){
   CruceCero = true;
}
void loop() {
  if(CruceCero){
    Time = millis();  
    contador = contador +1;      
    CruceCero = false;
}
  tiempo = 2;
  deltaT = millis()-Time;
  if(deltaT=tiempo){
    digitalWrite(5,HIGH);
    }
  digitalWrite(5,LOW);
 
  if(contador==60){
    Serial.print("1\n");
    contador = 0;
 }
}
