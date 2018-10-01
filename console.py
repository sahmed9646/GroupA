import sys
import os
import platform

## -------------------------------------------------------------------------- ##
## Config variables
## -------------------------------------------------------------------------- ##

# Config variable for setting whether the console support truecolor, meaning RGB
# color values. If the variable is defined as False then only standard 
# monochrone values are supported.
rgbSupport = True

## -------------------------------------------------------------------------- ##
## Platform-specifics
## -------------------------------------------------------------------------- ##

"""
Enable virtual terminal processing on Windows. This does only support version 10 and up of Windows.
"""
def enableWinVT():
    if sys.platform == "win32":
        if (int(platform.uname().release) < 10):
            global rgbSupport
            rgbSupport = False
            return
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

## -------------------------------------------------------------------------- ##
## Color constants
## -------------------------------------------------------------------------- ##

"""
Special color that represents no color. This is used to disable any color formatting for output to the terminal.
"""
CLEAR   = -1

RED     = 9
GREEN   = 10
BLUE    = 12

CYAN    = 14
MAGENTA = 13
YELLOW  = 11
WHITE = 15
ORANGE = 208

## -------------------------------------------------------------------------- ##
## Utility functions
## -------------------------------------------------------------------------- ##

"""
Returns whether or not a string represents an integer. This means that the string only contains valid integer characters and can be converted into an integer.

\param str String to check if could represent integer.
\return True if 'str' could represent and integer, else False.
"""
def isStringInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

## -------------------------------------------------------------------------- ##

"""
Format a text with a color. The terminal needs to support ansi escape sequences and truecolor for this to display correctly.

\note rgbSupport global config can be set to 'False' to disable any color formatting.

\param text Text to format.
\param color Color to format the text with. 
"""
def coloredText(text, color):
    if (rgbSupport and color >= 0):
        return "\033[38;5;" + str(color) + "m" + text + "\033[0m"
    return text

## -------------------------------------------------------------------------- ##

"""
"""
def clear():
    os.system("cls" if sys.platform == "win32" else "clear")

## -------------------------------------------------------------------------- ##

"""
Write a set of text to the console.

\param text Text that is written.
"""
def write(text):
    print(text)
 
## -------------------------------------------------------------------------- ##

"""
Read input from the console with the specified prompt text.

\param text Prompt text.
"""
def read(text, doClear=True):
    if doClear:
        clear()
    return input(text)

## -------------------------------------------------------------------------- ##

"""
\see consoleReadAlts.

This function works like consoleReadAlts but with added support for a range of integer numbers as valid input.
"""
def readInt(text, color, min, max, choices):
    text = coloredText(text, color) + "\n"

    # Format message
    validChoices = []
    for (choiceChar, choiceText, choiceColor) in choices:
        text = text + coloredText("[" + str(choiceChar) + "] " + choiceText + "\n", choiceColor)
        validChoices.append(choiceChar.lower())

    # Prompt user until valid choice
    choice = read(text).lower()
    validNum = isStringInt(choice) and int(choice) >= min and int(choice) <= max
    while choice not in validChoices and not validNum:
        write("Invalid choice (" + choice + ")\n")
        choice = read(text).lower()
        validNum = isStringInt(choice) and int(choice) >= min and int(choice) <= max

    write("")
    return choice

## -------------------------------------------------------------------------- ##

"""
Read user input from the terminal. The user is allowed to input one of the choices in the 'choices' list.

\param text The promt text to display to the user.
\param color Color of the prompt text.
\param choices List of available choices. This list contains one tuple for each choice. The first value in the tuple is the character that the user is allowed to input, the second value is the text for the choice and the third value is the color of the text for the choice.

\example
This example would prompt the user to make a choice between Blue, Green and quit. The made choice is returned from the call.

choice = readAlts(
    "Make a choice:", CLEAR, 
    [
        ("b", "Blue", BLUE),
        ("g", "Green", GREEN),
        ("q", "Quit", MAGENTA)
    ]
)

"""
def readAlts(text, color, choices):
    return readInt(text, color, 1, 0, choices)

## -------------------------------------------------------------------------- ##
## Code to activate escape sequence support on windows
## -------------------------------------------------------------------------- ##

enableWinVT()
