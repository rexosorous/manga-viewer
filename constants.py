# dependencies
from PyQt5 import QtGui
from json import load


directory = ''
with open('config.json', 'r') as file:
    data = load(file)
    directory = data['directory']



class Colors():
    PRIMARY = QtGui.QColor.fromRgb(50, 50, 50)
    SECONDARY = QtGui.QColor.fromRgb(125, 125, 125)
    BACKGROUND = QtGui.QColor.fromRgb(75, 75, 75)
    HIGHLIGHT = QtGui.QColor.fromRgb(129, 237, 247)
    AND = QtGui.QColor.fromRgb(0, 255, 0)
    NOT = QtGui.QColor.fromRgb(255, 0, 0)
    OR = QtGui.QColor.fromRgb(0, 255, 255)
    CLEANSE = QtGui.QColor.fromRgb(185, 185, 185)
    NONE = QtGui.QBrush()



class Palettes():
    PRIMARY = QtGui.QPalette()
    SECONDARY = QtGui.QPalette()
    BACKGROUND = QtGui.QPalette()
    HIGHLIGHT = QtGui.QPalette()
    AND = QtGui.QPalette()
    NOT = QtGui.QPalette()
    OR = QtGui.QPalette()
    CLEANSE = QtGui.QPalette()

    PRIMARY.setColor(QtGui.QPalette.Window, Colors.PRIMARY)
    SECONDARY.setColor(QtGui.QPalette.Window, Colors.SECONDARY)
    BACKGROUND.setColor(QtGui.QPalette.Window, Colors.BACKGROUND)
    HIGHLIGHT.setColor(QtGui.QPalette.Window, Colors.HIGHLIGHT)
    AND.setColor(QtGui.QPalette.WindowText, Colors.AND)
    NOT.setColor(QtGui.QPalette.WindowText, Colors.NOT)
    OR.setColor(QtGui.QPalette.WindowText, Colors.OR)
    CLEANSE.setColor(QtGui.QPalette.WindowText, Colors.CLEANSE)



class Filters():
    NONE = 0
    AND = 1
    NOT = 2
    OR = 3



class Spines():
    WIDTH = 296
    HEIGHT = 471
    IMG_WIDTH = 280
    IMG_HEIGHT = 400



class Sort():
    ALPHA_ASC = 0
    ALPHA_DESC = 1
    RATING_ASC = 2
    RATING_DESC = 3
    PAGES_ASC = 4
    PAGES_DESC = 5
    DATE_ASC = 6
    DATE_DESC = 7
    RANDOM = 8