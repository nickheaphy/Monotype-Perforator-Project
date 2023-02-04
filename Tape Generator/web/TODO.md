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

## Language

Loosely Based on LaTex.

```
\textrm{} - Roman font family (this is actually the default)
\textbf{} - Bold face
\textsc{} - Small Caps
\textit{} - Italics
\hspace{l} - horizontal space of l length
hyphen
en-dash --
em-dash ---
\begin{center}
\begin{flushleft}
\begin{flushright}
\begin{justify}
\\ - slash
\{
\}
```

Parsing logic: Character by character, when hit a \ go into a command mode. Command mode ends
when hit either a } or a space. Though also need to potentially handle having a command inside
another command (eg could have both `\textrm{\textbf{Bold roman text}}`) and need to handle the \\ and \{

Need to divide the text up into 

- characters (with a matrix position (based on character style) and width)
- words (the space is the delimiter, words have a width based on characters)
  - Note: words can be hyphenated over multiple lines
- line (based on the galley width only a specific number of words can fit, also need to know the justification for the line)
- paragraph (just a collection of lines - may actually not need this?)



