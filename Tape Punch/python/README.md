# Tape Punch - Python

This was a quick and dirty hack, that was barely a step up from using Putty to send the tape commands.

On the command line `python3 send.py tape.txt`

This will connect to `/dev/cu.usbmodem123451` (on the Mac) and send down a couple of microcontoller instructions to set the punch speed (`**p30 **d100`), and test all the punches (`**t4`), advance the tape 400mm (`**f125`) then transmit the contents of the `tape.txt` file, before again, feeding 400mm of tape and testing the punches.