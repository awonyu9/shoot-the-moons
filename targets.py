# targets.py
#   I did not use animation2.py or the projectile and button modules from the textbook website,
#   so please make sure to have my versions of the modules so you can run this as intended.
#     by Alexandra Wonyu

from graphics import *
from math import *
from random import randrange

from projectile import Projectile
from buttonview import ButtonView

class Launcher:
    """This is the base from which the shot is launched."""

    def __init__(self, win):
        """Draws the launcher base, the sea underneath, and a starry sky background.
            Sets arbitrary initial values for launch angle and velocity."""
        self.win = win

        sky = Image(Point(-10, 65), "starry_sky.gif").draw(self.win)
        
        base = Rectangle(Point(-8, 0), Point(8, 8))
        base.setFill(color_rgb(51, 255, 0))
        base.draw(win)

        sea = Rectangle(Point(-120, -10), Point(100, 0)).draw(self.win)
        sea.setFill("blue2")
        
        self.angle, self.velocity = radians(90), 40
        
        self.arrow = Line(Point(0,0), Point(0,0)).draw(win)
        self.redraw()

    def adjust_angle(self, amount):
        """Changes the launch angle by amount degrees."""
        self.angle = self.angle + radians(amount)
        self.redraw()

    def adjust_velocity(self, amount):
        """Changes the initial velocity by amount meters/second."""
        self.velocity = self.velocity + amount
        self.redraw()

    def redraw(self):
        """Redraws the arrow with adjusted angle and velocity."""
        self.arrow.undraw()
        pt1 = Point(0, 5)
        # For pt2, velocity is divided by 2 so that the arrow is not unnecessarily long
        pt2 = Point(cos(self.angle)*self.velocity/2,
                    sin(self.angle)*self.velocity/2)
        self.arrow = Line(pt1, pt2).draw(self.win)
        self.arrow.setArrow("last")
        self.arrow.setFill(color_rgb(51, 255, 0))
        self.arrow.setWidth(3)

    def fire(self):
        """Fires a shot from the launcher."""
        return ShotTracker(self.win, degrees(self.angle), self.velocity, 0)

class ShotTracker:
    """This is a circle that indicates the position of the shot."""
    
    def __init__(self, win, angle, velocity, height):
        """win is the GraphWin where the shot will be drawn.
        angle, velocity and height are parameters needed to initialise the projectile."""
        self.proj = Projectile(angle, velocity, height)
        self.marker = Circle(Point(0, height), 2)
        self.marker.setFill(color_rgb(255,69,0))
        self.marker.setOutline(color_rgb(255,69,0))
        self.marker.draw(win)

    def update(self, dt):
        """Moves the projectile and its marker dt seconds
        farther along the shot's flight."""
        self.proj.update(dt)

        marker_center = self.marker.getCenter()
        dx = self.proj.getX() - marker_center.getX()
        self.dy = self.proj.getY() - marker_center.getY()
        self.marker.move(dx, self.dy)

    def getX(self):
        """Returns the x-coordinate of the shot's centre."""
        return self.proj.getX()

    def getY(self):
        """Returns the y-coordinate of the shot's centre."""
        return self.proj.getY()

    def undraw(self):
        """Undraws the shot's marker."""
        self.marker.undraw()

class Target:
    """This is the moving target that the shot attempts to hit."""

    def __init__(self, win):
        """Draws a target, designed here as a moon."""
        self.xvel = 1
        px, py = randrange(-112, 92), randrange(85, 130)
        self.target = Circle(Point(px, py), 8)
        self.target.setFill("white")
        self.target.setOutline("gold")
        self.target.draw(win)

    def hit_by(self, shot):
        """Returns True is the target and the shot collide."""
        x1, x2 = self.target.getCenter().getX(), shot.getX()
        y1, y2 = self.target.getCenter().getY(), shot.getY()
        distance_sq = (x2-x1)**2 + (y2-y1)**2
        return sqrt(distance_sq) <= 12

    def destroy(self):
        """Undraws the target."""
        self.target.undraw()

    def update(self):
        """Moves the target horizontally.
            Reverses target's direction if it hits a vertical boundary."""
        xpos = self.target.getCenter().getX()
        if xpos == 92: self.xvel = -self.xvel
        if xpos == -112: self.xvel = -self.xvel
        self.target.move(self.xvel, 0)

class ProjectileApp:
    """This is the main interface for the shooting game."""

    def __init__(self):
        """Draws the game window once the user has read instructions and presses
            a Start button.
            It consists of a launcher, a target, a score display and a list of
            shots that are currently deemed alive."""
        self.welcome()
        pt = self.winB.getMouse()
        if self.start.clicked(pt):
            self.winB.close()
            
        self.win = GraphWin("Targets", 500, 400, autoflush=False)
        self.win.setCoords(-120, -10, 100, 155)
        self.win.setBackground("black")

        self.launcher = Launcher(self.win)
        self.target = Target(self.win)
        self.shots = []
        
        self.score = 0
        self.score_label = Text(Point(-95, 145), f"SCORE: {self.score}").draw(self.win)
        self.score_label.setFill("red")
        self.score_label.setStyle("bold")

    def welcome(self):
        """An additional window that describes the game's rules and controls.
            Contains a Start button the user has to click to proceed to the game."""
        self.winB = GraphWin("Welcome!", 400, 300)
        self.winB.setCoords(0, 0, 40, 30)
        self.winB.setBackground("black")

        top = Rectangle(Point(0, 25), Point(40, 30)).draw(self.winB)
        top.setFill("white")
        welcome = Text(Point(20, 27.5), "SHOOT THE MOONS!").draw(self.winB)
        welcome.setFill("blue2")
        welcome.setStyle("bold")
        welcome.setSize(21)
        welcome.setFace("courier")

        f_key = Text(Point(12, 23), "- Press 'F' to fire a shot.").draw(self.winB)
        q_key = Text(Point(28, 23), "- Press 'Q' to quit.").draw(self.winB)
        rule = Text(Point(17.3, 20), "- You can only score on your way down.").draw(self.winB)
        text = [f_key, q_key, rule]
        for item in text: item.setFill("white")

        controls = Text(Point(8.5, 15), "CONTROLS:").draw(self.winB)
        controls.setStyle("bold")
        controls.setFill(color_rgb(51, 255, 0))
        
        self.start = ButtonView(self.winB, "START", Point(35, 15), 7, 3)
        self.start.activate()

        keys = [(15.5, 4.5, 18.5, 7.5, 17.75, 5.25, 17.75, 6.75, 16.25, 6),
                (18.5, 4.5, 21.5, 7.5, 20, 5.25, 19.25, 6.75, 20.75, 6.75),
                (21.5, 4.5, 24.5, 7.5, 22.25, 5.25,  22.25, 6.75, 23.75, 6),
                (18.5, 7.5, 21.5, 10.5, 19.25, 8.25, 20.75, 8.25, 20, 9.75)]
        
        for (corx1, cory1, corx2, cory2, trix1, triy1, trix2, triy2, trix3, triy3) in keys:
            key = Rectangle(Point(corx1, cory1), Point(corx2, cory2))
            key.setFill("black")
            key.setOutline("white")
            
            arrow = Polygon(Point(trix1, triy1), Point(trix2, triy2), Point(trix3, triy3))
            arrow.setFill("white")
            
            key.draw(self.winB)
            arrow.draw(self.winB)

        key_controls = [("ANGLE -", 11, 6), ("ANGLE +", 29, 6),
                        ("VELOCITY +", 20, 12), ("VELOCITY -", 20, 3)]

        for (label, Px, Py) in key_controls:
            control = Text(Point(Px, Py), label).draw(self.winB)
            control.setFill("gold")
            control.setStyle("bold")

    def run(self):
        """Contains the event/animation loop that maps control keys,
            keeps the target moving, and checks if it has been hit by a shot."""
        while True:
            self.update_shots(1/4)

            key = self.win.checkKey()
            if key in ["q", "Q"]: break
            if key == "Up": self.launcher.adjust_velocity(5)
            elif key == "Down":self.launcher.adjust_velocity(-5)
            elif key == "Left": self.launcher.adjust_angle(5)
            elif key == "Right": self.launcher.adjust_angle(-5)
            elif key in ["f", "F"]: self.shots.append(self.launcher.fire())

            self.target.update()
            self.checkForHit()
            update(30)

        self.win.close()

    def update_shots(self, dt):
        """Adds to a list of alive shots only shots that are within win's boundaries."""
        alive = []
        for shot in self.shots:
            shot.update(dt)
            if 0 <= shot.getY() and -120 <= shot.getX() <= 100:
                alive.append(shot)
            else: shot.undraw()
        self.shots = alive

    def checkForHit(self):
        """If a given target has been hit by a falling shot, both the shot and the target
            are undrawn, a new target is created, and score is updated."""
        for shot in self.shots:
            if self.target.hit_by(shot) and shot.dy < 0:
                shot.undraw()
                self.target.destroy()
                target2 = Target(self.win)
                target2.xvel = -self.target.xvel
                self.target = target2
                
                self.score = self.score + 1
                self.score_label.setText(f"SCORE: {self.score}")
        
    
if __name__ == "__main__": ProjectileApp().run()
