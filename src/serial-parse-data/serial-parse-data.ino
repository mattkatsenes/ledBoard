// Example 5 - Receive with start- and end-markers combined with parsing
// modified my Mr. Katsenes

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

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

      // variables to hold the parsed data
//char messageFromPC[numChars] = {0};
int LEDnumber = 0;
int LEDred = 0;
int LEDgreen = 0;
int LEDblue = 0;

boolean newData = false;

//============

void setup() {
    Serial.begin(115200);
    Serial.setTimeout(1);

    pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
    
}

//============

void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        
        pixels.setPixelColor(LEDnumber, pixels.Color(LEDgreen, LEDred, LEDblue));
        pixels.show();
        newData = false;
    }
}

//============

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        //testing echo it back
        //Serial.print(rc);
        
        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            //Serial.print("starting receive");
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts
  // expects data in this format: LEDnumber,red,green,blue (all ints)

    char * strtokIndx; // this is used by strtok() as an index

    //Serial.print(tempChars); // show what we're dealing with.

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    LEDnumber = atoi(strtokIndx); // set the LED number
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    LEDred = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    LEDgreen = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    LEDblue = atoi(strtokIndx);     // convert this part to an integer

}
