#include <ADCTouch.h>

#undef FAST_SAMPLING
// slow mode: 224 micros per sample, 7 ms per scan of all buttons
// fast mode: 40 micros per sample, 1.3 ms per scan of all buttons

#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit)) // see http://yaab-arduino.blogspot.com/2015/02/fast-sampling-from-analog-input.html
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))

int pins[] = {A0,A1,A2,A3,A4,A5,A6,A7};

const uint8_t notes[] = {60, 62, 64, 65, 67, 69, 71, 72};
const int numPins = sizeof(pins)/sizeof(*pins);
const uint8_t NOTE_ON = 0b10010000;
const uint8_t NOTE_OFF = 0b10000000;
int ref[numPins];
uint8_t prev[8];

void setup() 
{
#ifdef FAST_SAMPLING
    sbi(ADCSRA, ADPS2);
    cbi(ADCSRA, ADPS1);
    cbi(ADCSRA, ADPS0);
#endif    
    
    Serial.begin(115200);

    pinMode(LED_BUILTIN , OUTPUT);
    digitalWrite(LED_BUILTIN, 1);     

    for (int i=0; i<numPins; i++) {
        ref[i] = ADCTouch.read(pins[i], 500);
        prev[i] = 0;
    }

    digitalWrite(LED_BUILTIN, 0);
/*
    uint32_t t = micros();
    ADCTouch.read(A0, 10000);
    t = micros() -t;
    Serial.println(t);
*/
} 

void midiNote(uint8_t status, uint8_t note, uint8_t velocity) {
  Serial.write(status);
  Serial.write(note);
  Serial.write(velocity);
}

void loop() 
{
    uint8_t pressed = 0;
    
    for (int i=0; i<numPins; i++) {
      if (ADCTouch.read(pins[i], 5) - ref[i] > 25) {
         pressed = 1;
         if(!prev[i]) {
           midiNote(NOTE_ON, notes[i], 127);
           prev[i] = 1;
         }
      }
      else {
         if(prev[i]) {
           midiNote(NOTE_OFF, notes[i], 127);
           prev[i] = 0;
         }
      }
    }
    digitalWrite(LED_BUILTIN, pressed);
}

