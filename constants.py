from PyQt5 import QtGui

directory = r'C:\Users\jzlok\programming\manga-viewer\test_library'

background_color = QtGui.QPalette()
background_color.setColor(QtGui.QPalette.Window, QtGui.QColor.fromRgb(75, 75, 75))

primary_color = QtGui.QPalette()
primary_color.setColor(QtGui.QPalette.Window, QtGui.QColor.fromRgb(50, 50, 50))

secondary_color = QtGui.QPalette()
secondary_color.setColor(QtGui.QPalette.Window, QtGui.QColor.fromRgb(125, 125, 125))

highlight_color = QtGui.QPalette()
highlight_color.setColor(QtGui.QPalette.Window, QtGui.QColor.fromRgb(230, 230, 0))


FILTER_NONE = 0
FILTER_AND = 1
FILTER_NOT = 2
FILTER_OR = 3

and_color = QtGui.QColor.fromRgb(0, 255, 0)
and_palette = QtGui.QPalette()
and_palette.setColor(QtGui.QPalette.WindowText, and_color)

not_color = QtGui.QColor.fromRgb(255, 0, 0)
not_palette = QtGui.QPalette()
not_palette.setColor(QtGui.QPalette.WindowText, not_color)

or_color = QtGui.QColor.fromRgb(0, 255, 255)
or_palette = QtGui.QPalette()
or_palette.setColor(QtGui.QPalette.WindowText, or_color)

cleanse_color = QtGui.QColor.fromRgb(185, 185, 185)
cleanse_palette = QtGui.QPalette()
cleanse_palette.setColor(QtGui.QPalette.WindowText, cleanse_color)

no_color = QtGui.QBrush()

spine_img_width = 280
spine_img_height = 400

spine_width = 296
spine_height = 471


ALPHA_ASC = 0
ALPHA_DESC = 1
RATING_ASC = 2
RATING_DESC = 3
PAGES_ASC = 4
PAGES_DESC = 5
DATE_ASC = 6
DATE_DESC = 7
RAND = 8