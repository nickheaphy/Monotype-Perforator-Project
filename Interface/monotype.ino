// Function Protoypes (only needed for default arguments)
void tapeforward(int fnumber = 1);
void tapeback(int bnumber = 1);

// Define the pins
// LED Pins
#define LED 6 // this is the onboard LED
#define POWERON 33
#define ERRORSTATE 34

// punch pins
#define punch1 7
#define punch2 20
#define punch3 5
#define punch4 21
#define punch5 4
#define punch6 22
#define punch7 3
#define punch8 23
#define punch9 2
#define punch10 24
#define punch11 1
#define punch12 25
#define punch13 16
#define punch14 26
#define punchA 19
#define punchB 8
#define punchC 38
#define punchD 39
#define punchE 9
#define punchF 10
#define punchG 27
#define punchH 11
#define punchI 31
#define punchJ 12
#define punchK 30
#define punchL 13
#define punchM 41
#define punchN 14
#define punchS 29
#define punch0005 15
#define punch0075 35

// control pins
#define forward 45
#define tapestop 43
#define backward 44
#define tighttape 18
#define inhibit 42

// buttons
#define testbutton 0

// number of channels
#define numChannels 31

// duration 2.8ms minimum, 3.4ms maximum
#define signalLength 3

// maximum punches energised
int maxPunchesEnergised = 8;

// delay after forward
int forwarddelay = 500;

// post punch delay
int postPunchDelay = 60;

// punch order
int punchOrder[] = {punchN,punchM,punchL,punchK,punchJ,punchI,punchH,punchG,punchF,punchS,
                    punchE,punchD,punch0075,punchC,punchB,punchA,punch1,punch2,punch3,
                    punch4,punch5,punch6,punch7,punch8,punch9,punch10,punch11,punch12,
                    punch13,punch14,punch0005};

// punch data
bool toPunch[numChannels];

// incoming serial data
int incomingByte = 0;
int previousByte = 0;

// storing mode
bool storingdata = false;

// current punch position
int punchPositionPointer = 0;

// control mode
// if true then we send control codes to change settings
bool controlmode = false;

// --------------------------------------------------------------
// the setup routine runs once when you press reset:
void setup() {
  
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Serial.println("Initiating the punches...");
  for (int i = 0; i<numChannels; i++) {
    pinMode(punchOrder[i], OUTPUT);
  }

  Serial.println("Initiating the other ports...");
  pinMode(tapestop, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(POWERON, OUTPUT);
  pinMode(ERRORSTATE, OUTPUT);
  pinMode(forward, OUTPUT);
  pinMode(backward, OUTPUT);
  pinMode(tighttape, INPUT);
  pinMode(inhibit, OUTPUT);

  digitalWrite(inhibit, LOW);
  digitalWrite(tapestop, HIGH); //tape stop needs to be set HIGH to function, not sure why.

  // handle the test button being pressed
  attachInterrupt(digitalPinToInterrupt(testbutton), test_button_pressed, CHANGE);

  clear_toPunchArray();
  Serial.println("Waiting for data...");
}

// --------------------------------------------------------------
// the loop routine runs over and over again forever:
void loop() {

  if ((digitalRead(tighttape) != HIGH) && (Serial.available() > 0)) {

    digitalWrite(ERRORSTATE, LOW);

    previousByte = incomingByte; // store the previous incoming byte, so we can look back
    incomingByte = Serial.read(); // get the next byte

    if (incomingByte == '|') {
      controlmode = false; //control mode is reset by |
      //this is either the beginning or the end of a tape row
      if (storingdata == false) {
        // this is the beginnging of the punch row data
        if (previousByte == '\n' || previousByte == 0) {
          storingdata = true;
          Serial.println("Staring new line of punches");
        }
      } else {
        // this is the end of the row, so punch and clear
        Serial.println("Punching line of data");
        punchAnArray(toPunch, numChannels);
        clear_toPunchArray();
        storingdata = false;
      }

    } else if (storingdata) {
      if (incomingByte == 'o' || incomingByte == 'O') {
        // this is a punch position command
        toPunch[punchPositionPointer] = true;
        punchPositionPointer++;
      } else {
        // we are storing data, but this must not be a punch
        punchPositionPointer++;
      }
      Serial.println("Storing punch command...");

    } else if ((incomingByte == '*') && (previousByte == '*')) {
      // ** puts microcontroller into control mode and allows
      // you to change properties or send commands
      controlmode = true;
      Serial.println("Entering control mode...");

    } else if (controlmode && incomingByte == 't') {
      // this control the test patterns
      // need to get the next number
      Serial.println("Sending Control Mode Data...");
      int testpattern = Serial.parseInt();
      switch(testpattern) {
        case 1:
          testpunch();
          break;
        case 2:
          testpunch2();
          break;
        case 3:
          testpunch3();
          break;
        case 4:
          testpunch4();
          break;
        case 69:
          nickTest();
          break;
      }
      controlmode = false;
    } else if (controlmode && incomingByte == 'f') {
      tapeforward(Serial.parseInt());
      controlmode = false;
    } else if (controlmode && incomingByte == 'b') {
      tapeback(Serial.parseInt());
      controlmode = false;
    } else if (controlmode && incomingByte == 'm') {
      // adjust the maximum punches
      maxPunchesEnergised = Serial.parseInt();
      controlmode = false;
    } else if (controlmode && incomingByte == 'p') {
      //adjust the post punch delay
      postPunchDelay = Serial.parseInt();
      controlmode = false;
    } else if (controlmode && incomingByte == 'd') {
      forwarddelay = Serial.parseInt();
      controlmode = false;
    } else {
      // ignore this charater
      ;
    }
      
  } else if (digitalRead(tighttape) == HIGH) {
    // don't read any more bytes until tight tape condition resolved
    digitalWrite(ERRORSTATE, HIGH);
    Serial.println("Tightape...");
  }
    
}

// --------------------------------------------------------------
// Function: testLED()
// what frequency can we flash the led at?
//
void testLED() {

  int ton = 3;
  int toff = 500;

  for (int i = 0; i < 1000; i++){
    digitalWrite(LED, HIGH);
    delay(ton);
    digitalWrite(LED, LOW);
    delay(toff);
  }
}

// --------------------------------------------------------------
// Function: testpunch()
// Punch all channels in sequence and in reverse
//
void testpunch() {
  Serial.println("Starting Test 1");
  for (int i = 0; i < numChannels; i++) {
    punchAndAdvance(punchOrder[i]);
  }
  for (int i = numChannels-1; i >= 0; i--) {
    punchAndAdvance(punchOrder[i]);
  }
  Serial.println("End Test");
}

// --------------------------------------------------------------
// Function: testpunch2()
// Punch the edges
//
void testpunch2() {
  Serial.println("Starting Test 2");
  bool l1[] = {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1};
  punchAnArray(l1,sizeof(l1));
  Serial.println("End Test");
}

// --------------------------------------------------------------
// Function testpunch3()
// Punch all the channels using the punch functions
//
void testpunch3() {
  Serial.println("Starting Test 3");
  bool l1[] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
  punchAnArray(l1,sizeof(l1));
  Serial.println("End Test");
}

// --------------------------------------------------------------
// Function: testpunch4()
// Loop though and punch each channel in turn. Not using the punch functions
//
void testpunch4() {
  for (byte i = 0; i < (sizeof(punchOrder) / sizeof(punchOrder[0])); i++) {
    digitalWrite(punchOrder[i], HIGH);
    delay(signalLength);
    digitalWrite(punchOrder[i], LOW);
    delay(signalLength);
  }
  digitalWrite(forward, HIGH);
  delay(signalLength);
  digitalWrite(forward, LOW);
}


// --------------------------------------------------------------
// Function: punchAndAdvance(punchcode)
// Punch the code and advance the tape
//
void punchAndAdvance(int punchCode) {
  digitalWrite(LED, HIGH);
  digitalWrite(punchCode, HIGH);
  digitalWrite(forward, HIGH);
  delay(signalLength);
  digitalWrite(punchCode, LOW);
  digitalWrite(forward, LOW);
  digitalWrite(LED, LOW);
  delay(forwarddelay);
}
// --------------------------------------------------------------
// Function: punchAndDontAdvance(punchcode)
// Punch the code and don't advance the tape
//
void punchAndDontAdvance(int punchCode) {
  digitalWrite(LED, HIGH);
  digitalWrite(punchCode, HIGH);
  delay(signalLength);
  digitalWrite(punchCode, LOW);
  digitalWrite(LED, LOW);
  delay(postPunchDelay);
}


// --------------------------------------------------------------
// Function: tapeforwardnum(fnumber)
// Move the tape forward mutiple rows
void tapeforward(int fnumber) {
  deenergisePunches();
  for (int i = 0; i < fnumber; i++) {
    digitalWrite(forward, HIGH);
    delay(signalLength);
    digitalWrite(forward, LOW);
    delay(forwarddelay);
  }
}

// --------------------------------------------------------------
// Function: move the tape back
//
void tapeback(int bnumber) {
  for (int i = 0; i < bnumber; i++) {
    digitalWrite(backward, HIGH);
    delay(signalLength);
    digitalWrite(backward, LOW);
    delay(forwarddelay);
  }
}

// --------------------------------------------------------------
// Function: punchAnArray (boolean array, array length)
// Loops thought the array and punches when it finds a true
// This energises multiple punches at once.
// This is not working :-(

void punchAnArray2(bool punchPattern[], int punchPatternLength) {
  //loop though the array and punch the pattern

  // need to keep track of the number of punches that are already on
  int numpunchesenergised = 0;
  int punchesenergised[maxPunchesEnergised];

  for (int i = 0; i < punchPatternLength; i++) {
    //make sure we have not been passed too big an array
    if (i >= numChannels) {
      break;
    }
    //check if we are supposed to punch
    if (punchPattern[i]) {
      digitalWrite(punchOrder[i], HIGH);
      //keep track of channels that are energised
      punchesenergised[numpunchesenergised] = punchOrder[i];
      numpunchesenergised++;

      //check to see that we have not energised too many punches at one time
      if (numpunchesenergised == maxPunchesEnergised) {
        // delay and denergise
        delay(signalLength);
        for (int j = 0; j < numpunchesenergised; j++) {
          digitalWrite(punchesenergised[j], LOW);
        }
        delay(postPunchDelay);
        //reset counter
        numpunchesenergised = 0;
      }
    }
  }
  if (numpunchesenergised > 0) delay(signalLength);
  deenergisePunches();
  delay(postPunchDelay);
  tapeforward();
}

// --------------------------------------------------------------
// Function: punchAnArray (boolean array, array length)
// Loops thought the array and punches when it finds a true
// This just punches each consecutively, rather than energising
// multiple punches as once (the manual says that you should be
// able to energise 8 at once, but I have not been able to get this
// to reliabliy work) 

void punchAnArray(bool punchPattern[], int punchPatternLength) {

  for (int i = 0; i < punchPatternLength; i++) {
    //make sure we have not been passed too big an array
    if (i >= numChannels) {
      break;
    }
    //check if we are supposed to punch
    if (punchPattern[i]) {
      //Serial.print("Punching ");
      //Serial.println(i);
      punchAndDontAdvance(punchOrder[i]);
    }
  }
  tapeforward();
}

// --------------------------------------------------------------
// Function: clear_toPunchArray()
// Clears the global toPunchArray by setting everything to false
// Also resets the pointer
void clear_toPunchArray() {
  for (int i = 0; i < numChannels; i++) {
    toPunch[i] = false;
  }
  punchPositionPointer = 0;
}
  
// --------------------------------------------------------------
// Function: deenergisePunches
// Set all the punch pins to low
void deenergisePunches() {
  for (int i = 0; i < numChannels; i++) {
    digitalWrite(punchOrder[i], LOW);
  }
}

// --------------------------------------------------------------
// Function: nickTest
// print a Nick was Here test
//
void nickTest() {
  
  bool lfull[] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};

  bool l1[] = {0,1,0,0,0,1,0,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0};
  bool l2[] = {0,1,1,0,0,1,0,1,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  bool l3[] = {0,1,0,1,0,1,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  bool l4[] = {0,1,0,0,1,1,0,1,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  bool l5[] = {0,1,0,0,0,1,0,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0};

  bool l7[] = {0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0};
  bool l8[] = {0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0};
  bool l9[] = {0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0};
  bool l10[]= {0,0,0,1,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0};
  bool l11[]= {0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0};

  bool l12[]= {0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,1,1,0,1,1,1,0,0,1,1,1,1,0,0};
  bool l13[]= {0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0};
  bool l14[]= {0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,0,1,1,1,0,0,1,1,1,1,0,0};
  bool l15[]= {0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0};
  bool l16[]= {0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,0};

  punchAnArray(lfull,sizeof(lfull));
  tapeforward();

  punchAnArray(l1,sizeof(l1));
  punchAnArray(l2,sizeof(l2));
  punchAnArray(l3,sizeof(l3));
  punchAnArray(l4,sizeof(l4));
  punchAnArray(l5,sizeof(l5));

  tapeforward();

  punchAnArray(l7,sizeof(l7));
  punchAnArray(l8,sizeof(l8));
  punchAnArray(l9,sizeof(l9));
  punchAnArray(l10,sizeof(l10));
  punchAnArray(l11,sizeof(l11));

  tapeforward();

  punchAnArray(l12,sizeof(l12));
  punchAnArray(l13,sizeof(l13));
  punchAnArray(l14,sizeof(l14));
  punchAnArray(l15,sizeof(l15));
  punchAnArray(l16,sizeof(l16));

  tapeforward();
  tapeforward();
  punchAnArray(lfull,sizeof(lfull));

  tapeforward(25);
}

// --------------------------------------------------------------
// Function: test_button_pressed
// This is the interupt handler for the test button being pressed
// need to software debounce the button
void test_button_pressed() {
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  // If interrupts come faster than 200ms, assume it's a bounce and ignore
  if (interrupt_time - last_interrupt_time > 200) {
    tapeforward(2);
    testpunch();
    tapeforward(2);
  }
  last_interrupt_time = interrupt_time;
}