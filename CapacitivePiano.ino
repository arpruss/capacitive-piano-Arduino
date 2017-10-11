#include <ADCTouch.h>

int pins[] = {A0,A1,A2,A3,A4,A5,A6,A7};
const int numPins = sizeof(pins)/sizeof(*pins);
int ref[numPins];
char line[numPins+1];

void setup() 
{
    Serial.begin(115200);

    pinMode(LED_BUILTIN , OUTPUT);
    digitalWrite(LED_BUILTIN, 1);     

    for (int i=0; i<numPins; i++)
        ref[i] = ADCTouch.read(pins[i], 500);

    line[numPins] = 0;

    digitalWrite(LED_BUILTIN, 0);
} 

void loop() 
{
    uint8_t pressed = 0;
    
    for (int i=0; i<numPins; i++)
      if (ADCTouch.read(pins[i], 5) - ref[i] > 25) {//40
        line[i] = '1';
        pressed = 1;
      }
      else
        line[i] = '0'; 

    Serial.println(line);

    digitalWrite(LED_BUILTIN, pressed);
}
