import turtle

def create_tank(color, pos, angle, name):
    t = turtle.Turtle()
    t.shape("turtle")
    t.color(color)
    t.penup()
    t.goto(pos)
    t.setheading(angle)
    t.active = True
    t.name = name
    return t

def create_bullet():
    b = turtle.Turtle()
    b.hideturtle()
    b.penup()
    b.shape("circle")
    b.shapesize(0.3)
    b.color("white")
    b.state = "ready"
    return b

def create_wall_segment(x, y):
    w = turtle.Turtle()
    w.shape("square")
    w.color("#b35900")
    w.shapesize(1.2, 1.2)
    w.penup()
    w.goto(x, y)
    return w