// Especifica la entrada en la que el sensor se encuentra conectado
int sensorPin = 0;

void setup() {
  Serial.begin(9600);

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

  // Espera por un segundo
  delay(1000);
}
