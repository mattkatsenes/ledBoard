// Sketch that turns on our LEDs one at a time.

#include <Adafruit_NeoPixel.h>

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN        6

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 150

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYLIGHT 500 // Time (in milliseconds) to pause with light on
#define DELAYDARK 1000 // Time (in milliseconds) to pause between lights

void setup() {
  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
}

void loop() {

  // iterates over each pixel in the string, turns it on for DELAYLIGHT, then all off for DELAYDARK.
  for(int i=0; i<NUMPIXELS; i++){
    pixels.setPixelColor(i, pixels.Color(255, 255, 255));
    pixels.show();
    delay(DELAYLIGHT);
    pixels.clear();
    pixels.show();
    delay(DELAYDARK);
  }
  
  
}
