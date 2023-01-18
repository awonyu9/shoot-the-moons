# buttonview.py
#   A ButtonView class
#   by Alexandra Wonyu

from graphics import *

class ButtonView:
    "Creates a button widget."
    
    def __init__(self, window, label, center, width, height):
        "Creates a rectangular button."
        x, y = center.getX(), center.getY()
        self.xmax, self.ymax = (x + width/2), (y + height/2)
        self.xmin, self.ymin = (x - width/2), (y - height/2)
        p1, p2 = Point(self.xmin, self.ymin), Point(self.xmax, self.ymax)
        self.rectangle = Rectangle(p1, p2)
        self.rectangle.setFill("white")
        self.rectangle.draw(window)
        self.label = Text(center, label)
        self.label.draw(window)
        self.deactivate()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill("red")
        self.rectangle.setOutline("red")
        self.label.setStyle("bold")
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill("white")
        self.rectangle.setWidth(1)
        self.active = False

    def clicked(self, point):
        "Returns True if button is active and point is inside it."
        insideX = self.xmin <= point.getX() <= self.xmax
        insideY = self.ymin <= point.getY() <= self.ymax
        return self.active and insideX and insideY

    def getLabel(self):
        "Returns the button's label."
        return self.label.getText()
