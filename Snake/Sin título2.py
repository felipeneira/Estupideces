#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from random import randint
import turtle
import time
import streamlit as st
# =============================================================================
# 
# =============================================================================
st.title("Jueguito")
# =============================================================================
# 
# =============================================================================
delay = 0.1
width, height = 600, 600
screen = turtle.Screen()
screen.setup(width=width, height=height, startx=-500, starty= 150)
screen.tracer(0)
screen.bgcolor("white")
screen.bgcolor("black")
# =============================================================================
# propiedades tortuguita y comida
# =============================================================================

# tortuguita
tortuga = turtle.Turtle()
tortuga.shape("turtle")
tortuga.color("white")
tortuga.penup()
tortuga.goto(0, 100)
tortuga.direction = "Stop"
tortuga.setheading(270)
time.sleep(1)
# comida

comida = turtle.Turtle(shape="triangle")
comida.penup()
comida.shapesize(0.5)
comida.color("red")
comida.speed(0)
comida.goto(0, 0)

# =============================================================================
# Movimiento1
# =============================================================================
def process_events():
    events = tuple(sorted(key_events))
    if events and events in key_event_handlers:
        (key_event_handlers[events])()
    key_events.clear()
    screen.ontimer(process_events, 10)
def Up():
    key_events.add('UP')
def Left():
    key_events.add('LEFT')
def Right():
    key_events.add('RIGHT')
def walk():
    running=True
    if running:
        tortuga.forward(15)
        screen.ontimer(walk,250)
        
        
def turnl():
    tortuga.left(25)
def turnr():
    tortuga.right(25)
def walkl():
    tortuga.forward(15)
    tortuga.lt(25)
def walkr():
    tortuga.fd(15)
    tortuga.rt(25)    
key_event_handlers = { \
    ("UP",): walk, \
    ("LEFT",):turnl, \
    ("RIGHT",):turnr, \
    ("LEFT", "UP"):walkl,\
    ("RIGHT", "UP"):walkr,\
}

key_events = set()
screen.ontimer(Up, t=0)
screen.onkeypress(Left, "Left")
screen.onkeypress(Right, "Right")
screen.listen()
process_events()

# =============================================================================
# Movimiento2
# =============================================================================

# =============================================================================
# Reglas juego
# =============================================================================
while True:
    screen.update()
    if tortuga.xcor() > 290 or tortuga.xcor() < -290 or tortuga.ycor() > 290 or tortuga.ycor() < -290:
        time.sleep(1)
        tortuga.goto(0, 100)
        comida.goto(0, 0)
    if tortuga.distance(comida) < 15:
        x = randint(-300,300)
        y = randint(-300,300)
        comida.goto(x,y)


screen.mainloop()
