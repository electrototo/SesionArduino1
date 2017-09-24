import processing.serial.*;

Serial arduino;

int sizex = 1080;
int sizey = 720;

void setup() {
  size(sizex, sizey);
  
  String port = Serial.list()[0];
  arduino = new Serial(this, port, 9600);
  
  background(0);
}

int x, y;
int bcolor, rcolor;
String val;

float voltaje, temperatura;

float temperaturaMin = 0;
float temperaturaMax = 40;

boolean line = true;

void draw() {
  if (arduino.available() > 0) {
    x %= sizex;
    val = arduino.readStringUntil('.');
    
    try {
      voltaje = int(val) * 5.0;
      voltaje /= 1024;
    }
    catch (NullPointerException e) {
      line = false;
    }
    
    if (line) {
      temperatura = (voltaje - 0.5) * 100;
      
      println(temperatura);
      
      y = sizey - int(map(temperatura, temperaturaMin, temperaturaMax, 0, sizey));
      rcolor = int(map(temperatura, temperaturaMin, temperaturaMax, 0, 255));
      bcolor = int(map(temperatura, temperaturaMax, temperaturaMin, 0, 255));
      
      stroke(rcolor, 0, bcolor);
      line(x, sizey, x, y);
      
      stroke(0);
      line(x + 1, sizey, x + 1, 0);
      
      x++;
    }
    
    line = true;
  }
}
