# Monotype Tape Punch

What the web interface needs to do:

* Main screen allows you to submit some text to be turned into a punch tape.
* The text submission window needs to have a WYSIWYG editor to allow you to select text to be formated in bold, italics, small caps etc
* You need to be able to enter the galley width and if you want to use quads at the end of the lines (to avoid characters falling over)
* Need to be able to enter the set size
* Need to be able to download the tape file for later punching
* Need to be able to select the MCA that you are using.

## MCA Editor

The MCA editor needs to allow you to:

* Select existing MCA and edit this
* Duplicate an existing MCA
* Create a new MCA from scratch
* Set if the MCA can be used or if it is still a work in progress
* Save the MCA
* MCA editing needs a login method (so random people can't mess with the MCAs)

Decision that needs to be made: Are we going to store the MCA as a JSON file in the file system or into a database?

## UI

* Export option to dump all the fonts matrixs to JSON to download for offline use.
* Option to process text character by character rather than word by word

## Paragraph Tape Generator

* Need to improve the logic about handing of em-dash in the text to avoid hyphenation of words that contain em dash. Need to think about the logic as to how to handle this (have tried splitting the words on the em-dash but this still sometimes runs into the problem of trying to hyphenate)