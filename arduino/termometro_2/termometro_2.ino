// Especifica la entrada en la que el sensor se encuentra conectado
int sensorPin = 0;

int ledR = 2; // LED Rojo
int ledV = 3; // LED Verde

float temperaturaMin = 20.5;

void setup() {
  Serial.begin(9600);

  // Se especifica que los pines ledR y ledV (2, 3) son salidas
  pinMode(ledR, OUTPUT);
  pinMode(ledV, OUTPUT);
}

void loop() {
  // Obtiene la lectura de la entrada analogica
  int lectura = analogRead(sensorPin);

  // Convierte la lectura a voltage
  float voltaje = lectura * 5.0;
  voltaje /= 1024.0;

  // Imprime al serial el voltaje
  Serial.print(voltaje);
  Serial.println(" volts");

  // Convierte el voltaje a temperatura
  float temperatura = (voltaje - 0.5) * 100;

  // Imprime la temperatura
  Serial.print(temperatura);
  Serial.println(" grados C");

  Serial.println();

  // Especificamos la temperatura a la que los LEDs rojo y verde
  // se deberian encender y apagar
  if (temperatura < temperaturaMin) {
    digitalWrite(ledR, LOW);
    digitalWrite(ledV, HIGH);
  }
  else {
    digitalWrite(ledR, HIGH);
    digitalWrite(ledV, LOW);
  }

  // Espera por un segundo
  delay(250);
}
