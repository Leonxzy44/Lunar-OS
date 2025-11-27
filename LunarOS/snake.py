# Simple Snake Game

import turtle
import time
import random


def run_snake():
    delay = 0.1
    score = 0
    high_score = 0

    # Set up the screen
    wn = turtle.Screen()
    wn.title("Simple Snake Game")
    wn.bgcolor("black")
    wn.setup(width=600, height=600)
    wn.tracer(0)

    # Snake head
    head = turtle.Turtle()
    head.speed(0)
    head.shape("square")
    head.color("green")
    head.penup()
    head.goto(0, 0)
    head.direction = "stop"

    # Food
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("red")
    food.penup()
    food.goto(0, 100)

    segments = []

    # Scoreboard
    score_pen = turtle.Turtle()
    score_pen.speed(0)
    score_pen.color("white")
    score_pen.penup()
    score_pen.hideturtle()
    score_pen.goto(0, 260)
    score_pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

    # Movement functions
    def go_up():
        if head.direction != "down":
            head.direction = "up"

    def go_down():
        if head.direction != "up":
            head.direction = "down"

    def go_left():
        if head.direction != "right":
            head.direction = "left"

    def go_right():
        if head.direction != "left":
            head.direction = "right"

    def move():
        if head.direction == "up":
            head.sety(head.ycor() + 20)
        elif head.direction == "down":
            head.sety(head.ycor() - 20)
        elif head.direction == "left":
            head.setx(head.xcor() - 20)
        elif head.direction == "right":
            head.setx(head.xcor() + 20)

    # Keyboard controls
    wn.listen()
    wn.onkeypress(go_up, "w")
    wn.onkeypress(go_down, "s")
    wn.onkeypress(go_left, "a")
    wn.onkeypress(go_right, "d")

    # Main game loop
    while True:
        wn.update()

        # Border collision
        if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            # Hide segments
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()

            score = 0
            score_pen.clear()
            score_pen.write(f"Score: {score}  High Score: {high_score}",
                            align="center", font=("Courier", 24, "normal"))

        # Food collision
        if head.distance(food) < 20:
            x = random.randint(-14, 14) * 20
            y = random.randint(-14, 14) * 20
            food.goto(x, y)

            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("green")
            new_segment.penup()
            segments.append(new_segment)

            score += 10
            if score > high_score:
                high_score = score

            score_pen.clear()
            score_pen.write(f"Score: {score}  High Score: {high_score}",
                            align="center", font=("Courier", 24, "normal"))

        # Move segments
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        # Body collision
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"

                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()

                score = 0
                score_pen.clear()
                score_pen.write(f"Score: {score}  High Score: {high_score}",
                                align="center", font=("Courier", 24, "normal"))

        time.sleep(delay)


# ONLY RUN THE GAME IF THE FILE IS OPENED DIRECTLY
if __name__ == "__main__":
    run_snake()

