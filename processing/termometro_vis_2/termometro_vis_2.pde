import processing.serial.*;

Serial arduino;

int sizex = 640;
int sizey = 480;

void setup() {
  size(sizex, sizey);
  
  String port = Serial.list()[0];
  arduino = new Serial(this, port, 9600);
  
  background(0);
}

int x = 0;
int y = 0;

String val;
float voltaje, temperatura;

boolean data = true;
boolean first = true;

int squarex = 1;
int squarey = 1;

int r, b;

void draw() {
  if (arduino.available() > 0) {
    val = arduino.readStringUntil('.');
    
    try {
      temperatura = ((((int(val) * 5.0)) / 1024) - 0.5) * 100;
    }
    catch (NullPointerException e) {
      data = false;
    }
    
    if (data) {
      r = int(map(temperatura, 15, 30, 0, 255));
      b = int(map(temperatura, 30, 15, 0, 255));
      
      fill(r, 0, b);
      noStroke();
      rect(x, y, squarex, squarey);
      
      x += squarex;
      
      if (x >= sizex) {
        x = 0;
        y += squarey;
        
        if (y >= sizey) {
          y = 0;
          x = 0;
        }
      }
    }
    
    data = true;
  }
}
