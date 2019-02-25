volatile bool CruceCero = false;
int contador = 0;
int Time = 0;
int Angulo = 45;
int deltaT = 0;
int tiempo = 0;
bool ifUnico = false;
int tensionCD = 0;


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
    Time = micros();  
    contador = contador +1;
    tensionCD = analogRead(0);
    Serial.println(tensionCD);          
    CruceCero = false;
}
  tiempo = 7*tensionCD;
  deltaT = micros()-Time;
  
  if((deltaT>=tiempo) && (deltaT<=tiempo+7000)){
    digitalWrite(5,HIGH);
    }
  digitalWrite(5,LOW);
  
  if(contador==120){
//    Serial.print("1\n");
//    Serial.print(analogRead(0));
//    Serial.print("\n");
    contador = 0;
 }
}
