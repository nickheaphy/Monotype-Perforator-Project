# Monotype Hardware Interface

The interface that connects the perforator to a computer is based on a [Teensy++ 2.0](https://www.pjrc.com/store/teensypp.html) (unfortunately, like the perforator, now discontinued). This board was chosen as it has enough hardware output pins for the 31 channel perforator and uses 5V logic, the same as the perforator.

The Teensy, being 5V logic allows for direct connection to the perforator without the need for additional components such as level shifters. The pins on the Teensy are [connected](Monotype%20Punch%Connector.pdf) to a EDAC 516-56 plug that connects directly to the socket on the perforator.

## Microcontroller 

The Teensy [code](monotype.ino) sets up the microcontroller as a serial device, expecting to see serial data in the form of a virtual tape.

```
|----o---------------------o----| T: J 11
|-----o----------------o--------| h: I 7
|----o--------------o-----------| e: J 4
|------o--o------o--------------|  : S H 1
|--------------o-------------o--| Q: B 13
|------o---------------o--------| u: H 7
|-----o----------o--------------| i: I 1
|--o----------------o-----------| c: L 4
|--------o-------------o--------| k: F 7
|------o--o------o--------------|  : S H 1
|-----o-------------------o-----| B: I 10
|-----o------------o------------| r: I 3
|------o----------------o-------| o: H 8
|--------o------------------o---| w: F 12
|-----o-----------------o-------| n: I 8
|------o--o------o--------------|  : S H 1
|-------------o----------o------| F: C 9
|------o----------------o-------| o: H 8
|-------o-------------o---------| x: G 6
```

The virtual tape was chosen just to make debugging easier - you can visually see what you are expecting to have punched.

### Punch Commands

A row that starts with a `|` instructs the microcontroller that this line contains punch data. The next 31 characters should be a combination of `-` and `o` characters, where the `o` indicates a hole is required. The punch instructions are terminated with another `|` character. The line can then continue with any characters effectively being comments (in the example above, the character and punches are listed)

### Special Instructions

A row that starts with `**` are special instructions to send to the microcontroller that change things like the speed of punching, or additional tape advance instructions.

#### Test Patterns

- **t1 - Test 1 - Punches each channel in sequence and advance
- **t2 - Test 2 - Punch just the left and right channels
- **t3 - Test 3 - Punch all the channels
- **t4 - Test 4 - Punch all the channels sequently. 

I normally would use the **t4 at the beginning of a tape punching session as it allows you to visually check that all the channels are punching and nothing needs cleaning.

#### Tape Advance

- **fXX - advance the tape XX steps
- **bXX - reverse the tape XX steps

This is useful at the beginning and end of the tape so you can remove it from the machine.

#### Other Commands

- **mX - set the maximum number of punches that can be energised at once (default 8)
- **pXX - set the delay to X between punching operations (default 60ms)
- **dXXX - set the delay to X between the last punch instruction and the tape advance command (default 500ms)

### Comments

Any line that does not begin with either `|` or `**` is ignored.

Any characters between the final `|` and the newline is ignored.

## Sending data to the microcontroller

When you connect the microcontroller to the computer it acts as a serial device. You can send the virtual tape to the microcontroller using a terminal emulator, Python or the GUI wrapper as part of this project.